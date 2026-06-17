#!/usr/bin/env python3
"""
Перевод статей в формат, совместимый с визуальным редактором Keystatic.

Keystatic статически анализирует MDX и НЕ умеет: import-строки, передачу
изображений в компонент пропсом, произвольный сырой HTML. Поэтому скрипт:

  1. удаляет все `import ... ;`;
  2. <Carousel images={[{src, alt}...]}/>  ->  <Carousel> с вложенными markdown
     картинками (Astro всё равно оптимизирует относительные пути, GIF из public/
     остаются анимированными);
  3. одиночные сырые <img ... .gif> -> markdown ![alt](src);
  4. блок скачивания Excel (<a class="pp-download">...) -> <Download .../>;
  5. VK <iframe> -> <Video .../>.

Запуск:  python3 scripts/keystatic_migrate.py
"""
import re
import pathlib

DOCS = pathlib.Path(__file__).resolve().parent.parent / "src" / "content" / "docs"

IMPORT_RE = re.compile(r"^import\s+(\w+)\s+from\s+'([^']+)';\s*$", re.M)
ANY_IMPORT_RE = re.compile(r"^import\s+.*?;\s*$\n?", re.M)
CAROUSEL_RE = re.compile(r"<Carousel\s+images=\{\[(.*?)\]\}\s*/>", re.S)
ITEM_RE = re.compile(r"\{\s*src:\s*([^,]+?),\s*alt:\s*\"((?:[^\"\\]|\\.)*)\"\s*\}")
RAW_IMG_RE = re.compile(r"<img\b[^>]*?/?>", re.S)
SRC_ATTR_RE = re.compile(r'src="([^"]+)"')
ALT_ATTR_RE = re.compile(r'alt="([^"]*)"')
DOWNLOAD_RE = re.compile(
    r'<a\b[^>]*?href="([^"]+)"[^>]*?>\s*<img[^>]*>\s*<span>([^<]*)</span>\s*</a>',
    re.S,
)
IFRAME_RE = re.compile(r'<iframe\b[^>]*?src="([^"]+)"[^>]*?>\s*</iframe>', re.S)


def migrate(text: str) -> str:
    imports = dict(IMPORT_RE.findall(text))  # ident -> path

    # 4. Блок скачивания Excel -> <Download />
    def repl_download(m):
        href, label = m.group(1), m.group(2).strip()
        return f'<Download href="{href}" label="{label}" />'

    text = DOWNLOAD_RE.sub(repl_download, text)

    # 5. VK iframe -> <Video />
    text = IFRAME_RE.sub(lambda m: f'<Video src="{m.group(1)}" />', text)

    # 2. <Carousel images={[...]}/> -> <Carousel> с markdown-картинками
    def repl_carousel(m):
        items = ITEM_RE.findall(m.group(1))
        lines = ["<Carousel>", ""]
        for src, alt in items:
            src = src.strip()
            if src.startswith('"') or src.startswith("'"):
                path = src[1:-1]
            else:
                path = imports.get(src, src)
            lines.append(f"![{alt}]({path})")
            lines.append("")
        lines.append("</Carousel>")
        return "\n".join(lines)

    text = CAROUSEL_RE.sub(repl_carousel, text)

    # 3. Одиночные сырые <img> -> markdown ![alt](src)
    def repl_img(m):
        tag = m.group(0)
        src_m = SRC_ATTR_RE.search(tag)
        if not src_m:
            return tag
        alt_m = ALT_ATTR_RE.search(tag)
        alt = alt_m.group(1) if alt_m else ""
        return f"![{alt}]({src_m.group(1)})"

    text = RAW_IMG_RE.sub(repl_img, text)

    # 1. Удаляем все import-строки
    text = ANY_IMPORT_RE.sub("", text)

    # Подчищаем тройные+ пустые строки, появившиеся после удаления импортов
    text = re.sub(r"\n{3,}", "\n\n", text)
    # Убираем пустые строки сразу после закрытия front-matter
    text = re.sub(r"(^---\n.*?\n---\n)\n+", r"\1\n", text, count=1, flags=re.S)
    return text


def main():
    changed = 0
    for path in sorted(DOCS.glob("*.mdx")):
        src = path.read_text(encoding="utf-8")
        out = migrate(src)
        if out != src:
            path.write_text(out, encoding="utf-8")
            changed += 1
            print(f"  обновлён: {path.name}")
    print(f"Готово. Изменено файлов: {changed}")


if __name__ == "__main__":
    main()

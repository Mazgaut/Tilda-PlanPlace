#!/usr/bin/env python3
"""
Импорт базы знаний PlanPlace (набор пронумерованных .md) в Starlight.

Что делает:
  1. Транслитерирует имена файлов в аккуратные слаги (URL).
  2. Для каждой статьи: title из первого H1, description из первого абзаца,
     тело без дублирующего H1, перекрёстные ссылки -> на новые URL.
  3. Файл 00-Оглавление становится главной страницей (index).
  4. Из оглавления строит боковое меню -> src/sidebar.mjs.

Запуск: python3 scripts/import_kb.py "<папка с md>"
"""
import os, re, sys, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, "src", "content", "docs")
BASE = "/Tilda-PlanPlace"

RU = {
    'а':'a','б':'b','в':'v','г':'g','д':'d','е':'e','ё':'e','ж':'zh','з':'z','и':'i',
    'й':'y','к':'k','л':'l','м':'m','н':'n','о':'o','п':'p','р':'r','с':'s','т':'t',
    'у':'u','ф':'f','х':'h','ц':'c','ч':'ch','ш':'sh','щ':'sch','ъ':'','ы':'y','ь':'',
    'э':'e','ю':'yu','я':'ya',
}


def translit(s):
    s = s.lower()
    out = []
    for ch in s:
        if ch in RU:
            out.append(RU[ch])
        elif ch.isalnum():
            out.append(ch)
        elif ch in ' -_':
            out.append('-')
        # прочее (скобки, запятые, точки) отбрасываем
    slug = re.sub(r'-+', '-', ''.join(out)).strip('-')
    return slug


def name_part(filename):
    """'09-Плитные-материалы.md' -> 'Плитные-материалы'"""
    base = os.path.splitext(os.path.basename(filename))[0]
    m = re.match(r'^(\d+)-(.*)$', base)
    return (m.group(1), m.group(2)) if m else (None, base)


def strip_md(text):
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)   # ссылки -> текст
    text = re.sub(r'[*_`>#]', '', text)                     # разметка
    return re.sub(r'\s+', ' ', text).strip()


def make_description(body_lines):
    for ln in body_lines:
        s = ln.strip()
        if not s or s.startswith(('#', '>', '-', '*', '|', '!', '1.')):
            continue
        d = strip_md(s)
        if len(d) > 40:
            if len(d) > 160:
                d = d[:157].rsplit(' ', 1)[0] + '…'
            return d
    return ""


def yaml_quote(s):
    return '"' + s.replace('\\', '\\\\').replace('"', '\\"') + '"'


def build_slug_map(files):
    """{ '09-...md basename': slug }"""
    m = {}
    for f in files:
        num, name = name_part(f)
        base = os.path.basename(f)
        m[base] = "index" if num == "00" else translit(name)
    return m


def rewrite_links(text, slug_map):
    def repl(mo):
        label, target = mo.group(1), mo.group(2)
        base = target.split('/')[-1]
        slug = slug_map.get(base)
        if not slug:
            return mo.group(0)
        url = f"{BASE}/" if slug == "index" else f"{BASE}/{slug}/"
        return f"[{label}]({url})"
    return re.sub(r'\[([^\]]+)\]\((\d+-[^)]+?\.md)\)', repl, text)


def convert_article(path, slug, slug_map):
    raw = open(path, encoding='utf-8').read()
    lines = raw.split('\n')
    # title из первого H1
    title, body_start = os.path.basename(path), 0
    for i, ln in enumerate(lines):
        if ln.strip().startswith('# '):
            title = ln.strip()[2:].strip()
            body_start = i + 1
            break
    body_lines = lines[body_start:]
    desc = make_description(body_lines)
    body = '\n'.join(body_lines).lstrip('\n')
    body = rewrite_links(body, slug_map)

    fm = ["---", f"title: {yaml_quote(title)}"]
    if desc:
        fm.append(f"description: {yaml_quote(desc)}")
    fm += ["---", "", body, ""]
    return title, '\n'.join(fm)


def parse_toc(toc_path, slug_map):
    """Вернуть [(group_label, [(item_label, slug), ...]), ...]"""
    groups, cur = [], None
    for ln in open(toc_path, encoding='utf-8'):
        s = ln.strip()
        gm = re.match(r'^##\s+(?:Раздел\s+\d+\.\s*)?(.+)$', s)
        if gm and 'Рекомендуемый порядок' not in s:
            cur = (gm.group(1).strip(), [])
            groups.append(cur)
            continue
        lm = re.match(r'^\d+\.\s*\[([^\]]+)\]\((\d+-[^)]+?\.md)\)', s)
        if lm and cur is not None:
            base = lm.group(2).split('/')[-1]
            slug = slug_map.get(base)
            if slug and slug != "index":
                cur[1].append((lm.group(1).strip(), slug))
    return [g for g in groups if g[1]]


def write_sidebar(groups):
    lines = ["// Сгенерировано scripts/import_kb.py из оглавления базы знаний.",
             "export const sidebar = ["]
    for label, items in groups:
        lines.append("  {")
        lines.append(f"    label: {js_str(label)},")
        lines.append("    items: [")
        for ilabel, slug in items:
            lines.append(f"      {{ label: {js_str(ilabel)}, slug: {js_str(slug)} }},")
        lines.append("    ],")
        lines.append("  },")
    lines.append("];")
    open(os.path.join(ROOT, "src", "sidebar.mjs"), 'w', encoding='utf-8').write('\n'.join(lines) + '\n')


def js_str(s):
    return "'" + s.replace('\\', '\\\\').replace("'", "\\'") + "'"


def main():
    src = sys.argv[1] if len(sys.argv) > 1 else None
    if not src or not os.path.isdir(src):
        print("Укажите папку с .md базы знаний"); sys.exit(1)
    files = sorted(glob.glob(os.path.join(src, "*.md")))
    slug_map = build_slug_map(files)

    # чистим текущие docs (старый прототип) — ассеты/компоненты не трогаем
    for old in glob.glob(os.path.join(DOCS, "*.md")) + glob.glob(os.path.join(DOCS, "*.mdx")):
        os.remove(old)

    count = 0
    for f in files:
        num, _ = name_part(f)
        slug = slug_map[os.path.basename(f)]
        title, content = convert_article(f, slug, slug_map)
        out = os.path.join(DOCS, ("index.md" if slug == "index" else f"{slug}.md"))
        open(out, 'w', encoding='utf-8').write(content)
        count += 1

    toc = next((f for f in files if name_part(f)[0] == "00"), None)
    groups = parse_toc(toc, slug_map) if toc else []
    write_sidebar(groups)

    print(f"Импортировано статей: {count}")
    print(f"Разделов меню: {len(groups)}; пунктов: {sum(len(i) for _, i in groups)}")
    for label, items in groups:
        print(f"  • {label}: {len(items)}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Мигратор медиа с Tilda → в репозиторий Starlight.

Для каждой статьи:
  1. Скачивает HTML страницы help.planplace.online/<slug>.
  2. Идёт по блокам Tilda (#allrecords) в порядке документа.
  3. Каждую галерею изображений привязывает к заголовку шага/раздела,
     который ей предшествует.
  4. Скачивает картинки: jpg/png → src/assets/<slug>/ (Astro оптимизирует в WebP),
     gif → public/media/<slug>/ (без оптимизации, чтобы сохранить анимацию).
  5. Вставляет изображения в соответствующие разделы Markdown-файла.

Запуск:  python3 scripts/migrate_media.py
"""
import os, re, ssl, sys, urllib.request, difflib
from bs4 import BeautifulSoup

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, "src", "content", "docs")
ASSETS = os.path.join(ROOT, "src", "assets")
PUBLIC = os.path.join(ROOT, "public", "media")
BASE_URL = "/Tilda-PlanPlace"  # для gif из public/

# upravlenie_plitami уже наполнен вручную — пропускаем
SLUGS = [
    "osnovnie_parametry", "menuap-katalog_elementov", "menuap-globalnye_peremennye",
    "forma_i_pisma", "zyavky_na_raschet", "diler_management", "decors_2",
    "mass_operations_pliti", "upravlenie_kromkami", "materialy_vitrin",
    "configurator_basics", "obb_management", "vychislaemie_znachenia",
    "math_methods", "price_rules", "price-list", "calculation_principles", "fasady",
]

CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE

STOP_MARKERS = ("информация была полезной", "если у вас есть вопросы",
                "предыдущее", "заявка в службу поддержки")
ANCHOR_RE = re.compile(r'^\s*(Шаг|Способ|Вариант|Этап|Блок)\b', re.I)


def norm(s):
    s = re.sub(r'[«»"“”\'`.:?!()№—–-]', ' ', s.lower())
    s = re.sub(r'[^\w\s]', ' ', s)
    return re.sub(r'\s+', ' ', s).strip()


def fetch(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    return urllib.request.urlopen(req, context=CTX, timeout=40).read()


def to_static(url):
    """Привести thumbnail-URL Tilda к полноразмерному static."""
    m = re.match(r'https://thb\.tildacdn\.com/(tild[\w-]+)/-/[^/]+/(.+)', url)
    if m:
        return f"https://static.tildacdn.com/{m.group(1)}/{m.group(2)}"
    return url


def img_url(el):
    u = el.get('data-original') or el.get('src') or ''
    return to_static(u.split('?')[0])


def is_content_img(u):
    return ('tildacdn' in u
            and u.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp'))
            and not re.search(r'Frame|like|dizlike|logo|\.svg', u, re.I))


def extract_galleries(html):
    """Вернуть список (anchor_text, [image_urls]) в порядке документа."""
    soup = BeautifulSoup(html, 'html.parser')
    recs = soup.select('#allrecords > div[id^="rec"]')
    galleries, current_anchor, started, seen = [], None, False, set()
    for r in recs:
        text = re.sub(r'\s+', ' ', r.get_text(' ')).strip()
        low = text.lower()
        headings = [h.get_text(' ', strip=True) for h in r.find_all(['h2', 'h3', 'h4'])]
        if headings and not started:
            started = True
        if not started:
            continue
        if any(m in low for m in STOP_MARKERS):
            break
        # обновляем якорь, если это заголовок раздела или шага
        if headings:
            current_anchor = headings[-1]
        elif ANCHOR_RE.match(text) and len(text) < 140:
            current_anchor = re.split(r'(?<=[.:])\s', text, 1)[0]
        # собираем картинки блока
        urls = []
        for im in r.find_all('img'):
            u = img_url(im)
            if is_content_img(u) and u not in seen:
                seen.add(u)
                urls.append(u)
        if urls:
            galleries.append((current_anchor, urls))
    return galleries


def heading_lines(lines):
    """Список (index, level, normalized_text) для строк-заголовков Markdown."""
    out = []
    for i, ln in enumerate(lines):
        m = re.match(r'^(#{2,4})\s+(.*)', ln)
        if m:
            out.append((i, len(m.group(1)), norm(m.group(2))))
    return out


def best_heading(anchor, headings, min_idx):
    """Лучший заголовок с индексом >= min_idx (монотонность по документу)."""
    if not anchor:
        return None
    a = norm(anchor)
    best, best_ratio = None, 0.0
    for idx, lvl, htext in headings:
        if idx < min_idx:
            continue
        r = difflib.SequenceMatcher(None, a, htext).ratio()
        if a and (a in htext or htext in a):
            r = max(r, 0.85)
        if r > best_ratio:
            best, best_ratio = (idx, lvl), r
    return best if best_ratio >= 0.5 else None


def process(slug):
    md_path = os.path.join(DOCS, slug + ".md")
    if not os.path.exists(md_path):
        print(f"  ! нет файла {slug}.md — пропуск"); return
    html = fetch("https://help.planplace.online/" + slug).decode('utf-8', 'ignore')
    galleries = extract_galleries(html)
    if not galleries:
        print(f"  {slug}: галерей не найдено"); return

    a_dir = os.path.join(ASSETS, slug)
    p_dir = os.path.join(PUBLIC, slug)
    lines = open(md_path, encoding='utf-8').read().split('\n')
    heads = heading_lines(lines)

    # карта: индекс заголовка -> markdown картинок (в порядке документа)
    inserts, unplaced, counter, min_idx = {}, [], 0, 0
    for anchor, urls in galleries:
        target = best_heading(anchor, heads, min_idx)
        if target is None and heads:
            # запасной вариант: текущая секция (последний привязанный заголовок)
            cur = [h for h in heads if h[0] >= min_idx]
            target = (cur[0][0], cur[0][1]) if cur else None
        if target:
            min_idx = target[0]
        snippets = []
        for u in urls:
            counter += 1
            ext = u.lower().rsplit('.', 1)[-1]
            fname = f"{counter:02d}.{ext}"
            alt = (anchor or slug).replace(']', '').replace('[', '')[:80]
            if ext == 'gif':
                os.makedirs(p_dir, exist_ok=True)
                open(os.path.join(p_dir, fname), 'wb').write(fetch(u))
                snippets.append(f'<img src="{BASE_URL}/media/{slug}/{fname}" alt="{alt}" '
                                f'style="max-width:100%;border-radius:8px;" />')
            else:
                os.makedirs(a_dir, exist_ok=True)
                open(os.path.join(a_dir, fname), 'wb').write(fetch(u))
                snippets.append(f'![{alt}](../../assets/{slug}/{fname})')
        block = "\n\n".join(snippets)
        if target:
            inserts.setdefault(target[0], []).append(block)
        else:
            unplaced.append(block)

    # вставка: с конца файла, чтобы не сдвигать индексы
    head_idx = [h[0] for h in heads]
    for hidx in sorted(inserts.keys(), reverse=True):
        # конец секции = следующий заголовок после hidx
        nxt = next((i for i in head_idx if i > hidx), len(lines))
        payload = "\n\n" + "\n\n".join(inserts[hidx]) + "\n"
        lines[nxt:nxt] = payload.split('\n')

    if unplaced:
        lines += ["", "\n\n".join(unplaced), ""]

    open(md_path, 'w', encoding='utf-8').write('\n'.join(lines))
    placed = sum(len(v) for v in inserts.values())
    print(f"  {slug}: галерей={len(galleries)} вставлено_групп={placed} "
          f"без_привязки={len(unplaced)} картинок={counter}")


if __name__ == "__main__":
    targets = sys.argv[1:] or SLUGS
    for s in targets:
        print(f"→ {s}")
        try:
            process(s)
        except Exception as e:
            print(f"  ОШИБКА {s}: {e}")

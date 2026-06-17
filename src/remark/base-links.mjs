// Подгонка внутренних ссылок и путей к картинкам под текущий `base`.
//
// Зачем: в статьях внутренние ссылки и пути к GIF жёстко прописаны с префиксом
// продакшена — `/Tilda-PlanPlace/...`. В вебе base = `/Tilda-PlanPlace`, и они
// верны. Но локально в режиме Keystatic base = `/` (отключён ради работы
// админки), поэтому такие ссылки/картинки не находятся. Плагин заменяет
// фиксированный префикс на актуальный base: в вебе ничего не меняется, локально
// `/Tilda-PlanPlace/foo` -> `/foo`.
import { visit } from 'unist-util-visit';

const PREFIX = '/Tilda-PlanPlace';

export function remarkBaseLinks(base) {
  // norm: '' для base '/', иначе '/Tilda-PlanPlace' (без хвостового слэша).
  const norm = base.endsWith('/') ? base.slice(0, -1) : base;
  if (norm === PREFIX) return () => {}; // в проде заменять нечего

  return (tree) => {
    visit(tree, ['link', 'image', 'definition'], (node) => {
      if (typeof node.url !== 'string') return;
      if (node.url === PREFIX) {
        node.url = norm || '/';
      } else if (node.url.startsWith(PREFIX + '/')) {
        node.url = norm + node.url.slice(PREFIX.length);
      }
    });
  };
}

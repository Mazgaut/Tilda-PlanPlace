// Авто-импорт кастомных компонентов в MDX на этапе сборки.
//
// Зачем: визуальный редактор Keystatic не умеет MDX-`import`, поэтому в самих
// статьях импортов нет. Но сборщику Astro компоненты (Carousel, Video и т. д.)
// нужно «знать». Этот remark-плагин находит используемые в статье компоненты и
// сам подставляет нужные import-строки перед компиляцией — статьи остаются
// чистыми (Keystatic-совместимыми), а прод-сборка получает рабочие компоненты.
import { visit } from 'unist-util-visit';
import { parse } from 'acorn';

// Имя компонента -> путь импорта (root-relative, резолвится Vite).
const COMPONENTS = {
  Carousel: '/src/components/Carousel.astro',
  Bitrix24InlineForm: '/src/components/Bitrix24InlineForm.astro',
  Download: '/src/components/Download.astro',
  Video: '/src/components/Video.astro',
};

export function remarkAutoImportComponents() {
  return (tree) => {
    const used = new Set();
    visit(tree, (node) => {
      if (
        (node.type === 'mdxJsxFlowElement' || node.type === 'mdxJsxTextElement') &&
        node.name &&
        COMPONENTS[node.name]
      ) {
        used.add(node.name);
      }
    });
    if (used.size === 0) return;

    const code = [...used]
      .map((name) => `import ${name} from '${COMPONENTS[name]}';`)
      .join('\n');

    // mdxjsEsm-узлу нужен разобранный estree, иначе MDX не превратит его в импорт.
    const estree = parse(code, { ecmaVersion: 'latest', sourceType: 'module' });

    tree.children.unshift({
      type: 'mdxjsEsm',
      value: code,
      data: { estree },
    });
  };
}

// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import react from '@astrojs/react';
import keystatic from '@keystatic/astro';
import { sidebar } from './src/sidebar.mjs';
import { remarkAutoImportComponents } from './src/remark/auto-import-components.mjs';
import { remarkBaseLinks } from './src/remark/base-links.mjs';

// Админка Keystatic включается только локально (`npm run cms`), чтобы
// прод-сборка для GitHub Pages оставалась полностью статической.
const enableKeystatic = process.env.KEYSTATIC === 'true';

// В режиме Keystatic (локальная админка) base отключаем: иначе API-маршруты
// админки (/api/keystatic/...) не находятся и коллекция статей не загружается
// («Unable to load collection»). Для прод-сборки base берётся из переменной
// окружения BASE_PATH (по умолчанию '/Tilda-PlanPlace' — для GitHub Pages).
// При деплое на свой домен в корень workflow задаёт BASE_PATH='/'.
const base = enableKeystatic ? '/' : (process.env.BASE_PATH || '/Tilda-PlanPlace');

// Адрес публикации. По умолчанию — GitHub Pages. При деплое на свой домен
// workflow задаёт SITE_URL='https://help.вашдомен' (и BASE_PATH='/').
const site = process.env.SITE_URL || 'https://mazgaut.github.io';
export default defineConfig({
  site,
  base,
  // Remark-плагины:
  // - авто-импорт кастомных компонентов (статьи без import — для Keystatic);
  // - подгонка внутренних ссылок и путей к GIF под текущий base (чтобы они
  //   работали и в вебе с /Tilda-PlanPlace, и локально в режиме Keystatic).
  markdown: {
    remarkPlugins: [remarkAutoImportComponents, [remarkBaseLinks, base]],
  },
  integrations: [
    starlight({
      title: 'PlanPlace · Справка',
      description:
        'Справочный центр PlanPlace: настройка материалов, конструктора и работа с системой.',
      customCss: ['./src/styles/theme.css'],
      defaultLocale: 'root',
      locales: {
        root: { label: 'Русский', lang: 'ru' },
      },
      // Сайтовые счётчики и виджеты подключаются через переопределённый
      // компонент Head — он рендерит все коды из src/components/SiteAnalytics.astro.
      components: {
        Head: './src/components/Head.astro',
        Pagination: './src/components/Pagination.astro',
      },
      // SEO: за счёт статической генерации каждая статья отдаётся готовым HTML,
      // sitemap.xml формируется автоматически, meta/canonical/OG проставляются Starlight.
      // Меню генерируется из оглавления базы знаний (src/sidebar.mjs),
      // последним пунктом — страница формы обратной связи.
      sidebar: [...sidebar, { label: 'Связаться с нами', slug: 'forma' }],
    }),
    // Локальная админка Keystatic (только при KEYSTATIC=true)
    ...(enableKeystatic ? [react(), keystatic()] : []),
  ],
});

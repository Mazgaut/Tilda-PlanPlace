// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import react from '@astrojs/react';
import keystatic from '@keystatic/astro';
import { sidebar } from './src/sidebar.mjs';

// Админка Keystatic включается только локально (`npm run cms`), чтобы
// прод-сборка для GitHub Pages оставалась полностью статической.
const enableKeystatic = process.env.KEYSTATIC === 'true';

// Адрес публикации.
// Для GitHub Pages по умолчанию: https://<пользователь>.github.io/<репозиторий>
// При подключении собственного домена (help.planplace.online) — поменяйте site
// на 'https://help.planplace.online' и удалите/очистите base ('/').
export default defineConfig({
  site: 'https://mazgaut.github.io',
  // В режиме Keystatic (локальная админка) base отключаем: иначе API-маршруты
  // админки (/api/keystatic/...) не находятся и коллекция статей не загружается
  // («Unable to load collection»). Для прод-сборки GitHub Pages base обязателен.
  base: enableKeystatic ? '/' : '/Tilda-PlanPlace',
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

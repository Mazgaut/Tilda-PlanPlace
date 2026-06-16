// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import { sidebar } from './src/sidebar.mjs';

// Адрес публикации.
// Для GitHub Pages по умолчанию: https://<пользователь>.github.io/<репозиторий>
// При подключении собственного домена (help.planplace.online) — поменяйте site
// на 'https://help.planplace.online' и удалите/очистите base ('/').
export default defineConfig({
  site: 'https://mazgaut.github.io',
  base: '/Tilda-PlanPlace',
  integrations: [
    starlight({
      title: 'PlanPlace · Справка',
      description:
        'Справочный центр PlanPlace: настройка материалов, конструктора и работа с системой.',
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
      // Меню генерируется из оглавления базы знаний (src/sidebar.mjs).
      sidebar,
    }),
  ],
});

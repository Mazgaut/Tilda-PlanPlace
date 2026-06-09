// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

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
      // SEO: за счёт статической генерации каждая статья отдаётся готовым HTML,
      // sitemap.xml формируется автоматически, meta/canonical/OG проставляются Starlight.
      sidebar: [
        {
          label: 'Версия 2.0. Обзор и настройки',
          items: [
            { label: 'Код конструктора и основные настройки', slug: 'osnovnie_parametry' },
            { label: 'Каталог элементов', slug: 'menuap-katalog_elementov' },
            { label: 'Глобальные переменные', slug: 'menuap-globalnye_peremennye' },
            { label: 'Форма заявки и шаблоны писем', slug: 'forma_i_pisma' },
            { label: 'Заявки на расчёт', slug: 'zyavky_na_raschet' },
            { label: 'Управление дилерами', slug: 'diler_management' },
          ],
        },
        {
          label: 'Версия 2.0. Управление материалами',
          items: [
            { label: 'Декоры и текстуры', slug: 'decors_2' },
            { label: 'Плитные материалы (ЛДСП, ХДФ, ЛМДФ, стекло)', slug: 'upravlenie_plitami' },
            { label: 'Массовое редактирование плит', slug: 'mass_operations_pliti' },
            { label: 'Кромочные ленты', slug: 'upravlenie_kromkami' },
            { label: 'Материалы витрин', slug: 'materialy_vitrin' },
          ],
        },
        {
          label: 'Версия 2.0. Конфигуратор элементов',
          items: [
            { label: 'Основы Конфигуратора элементов', slug: 'configurator_basics' },
            { label: 'Вращение и пересечения моделей', slug: 'obb_management' },
            { label: 'Вычисляемые значения', slug: 'vychislaemie_znachenia' },
            { label: 'Математические вычисления', slug: 'math_methods' },
          ],
        },
        {
          label: 'Версия 2.0. Управление ценами и расчётами',
          items: [
            { label: 'Правила расчёта цен (наценки)', slug: 'price_rules' },
            { label: 'Прайс-листы и способы добавления цен', slug: 'price-list' },
            { label: 'Доступные типы расчётов', slug: 'calculation_principles' },
            { label: 'Настройка цен на фасады', slug: 'fasady' },
          ],
        },
      ],
    }),
  ],
});

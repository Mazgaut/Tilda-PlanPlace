import { config, fields, collection } from '@keystatic/core';
import { wrapper, block } from '@keystatic/core/content-components';

/**
 * Конфигурация Keystatic — визуальная панель управления статьями справки.
 *
 * Режим хранения: local — правки пишутся прямо в файлы репозитория, дальше
 * их нужно закоммитить и запушить (сработает авто-деплой). Админка доступна
 * локально по адресу http://localhost:4321/keystatic при запуске `npm run cms`.
 *
 * Чтобы сделать админку размещённой (без локального запуска), переключите
 * storage на GitHub или Keystatic Cloud — потребуется хостинг с серверным
 * рендерингом (см. README, раздел про Keystatic).
 */
export default config({
  storage: {
    kind: 'local',
    // kind: 'github', repo: 'Mazgaut/Tilda-PlanPlace',
  },
  ui: {
    brand: { name: 'PlanPlace · Справка' },
  },
  collections: {
    docs: collection({
      label: 'Статьи справки',
      path: 'src/content/docs/*',
      slugField: 'title',
      format: { contentField: 'content' },
      entryLayout: 'content',
      schema: {
        title: fields.slug({
          name: { label: 'Заголовок' },
        }),
        description: fields.text({
          label: 'Описание (для SEO и сниппетов)',
          multiline: true,
        }),
        content: fields.mdx({
          label: 'Содержание',
          // Кастомные Astro-компоненты, которые встречаются в статьях.
          // Keystatic не умеет MDX-import, поэтому компоненты регистрируются
          // здесь — это даёт их визуальное редактирование вместо ошибки.
          components: {
            // Карусель: изображения внутри как вложенный markdown (![](...)).
            Carousel: wrapper({
              label: 'Карусель изображений',
              schema: {},
            }),
            // Встроенная форма обратной связи Битрикс24 (без настроек).
            Bitrix24InlineForm: block({
              label: 'Форма Битрикс24',
              schema: {},
            }),
            // Кнопка скачивания файла-примера (например, шаблона Excel).
            Download: block({
              label: 'Кнопка скачивания',
              schema: {
                href: fields.url({ label: 'Ссылка на файл' }),
                label: fields.text({ label: 'Подпись кнопки' }),
              },
            }),
            // Встраиваемое видео (VK Видео, YouTube и т. п.).
            Video: block({
              label: 'Видео',
              schema: {
                src: fields.url({ label: 'Ссылка на плеер (src у iframe)' }),
              },
            }),
          },
        }),
      },
    }),
  },
});

import { config, fields, collection } from '@keystatic/core';

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
        }),
      },
    }),
  },
});

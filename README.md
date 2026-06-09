# Справочный центр PlanPlace

Документация PlanPlace на [Astro Starlight](https://starlight.astro.build/) —
статический сайт справки с авто-деплоем на GitHub Pages.

Почему так: каждая статья генерируется в готовый HTML, поэтому страницы
индексируются поисковиками и читаются ИИ-поисковиками, а меню и оформление
управляются централизованно из одного места.

## Как добавить новую статью

1. Создайте файл `src/content/docs/<slug>.md`.
2. В начале файла укажите «паспорт» статьи (front-matter):

   ```markdown
   ---
   title: Заголовок статьи
   description: Краткое описание для поисковиков и ИИ (140–160 символов).
   ---

   Текст статьи в Markdown…
   ```

3. Добавьте статью в меню в `astro.config.mjs` (массив `sidebar`).
4. Закоммитьте и запушьте в ветку `main` — сайт пересоберётся и опубликуется сам.

Готовый HTML вручную писать не нужно — его собирает сборщик.

## Локальный запуск

```bash
npm install      # установить зависимости (один раз)
npm run dev      # локальный предпросмотр на http://localhost:4321
npm run build    # собрать статику в ./dist
npm run preview  # посмотреть собранную статику
```

## Публикация (GitHub Pages)

Деплой настроен в `.github/workflows/deploy.yml` и срабатывает при пуше в `main`.

Разовая настройка в репозитории на GitHub:

1. **Settings → Pages → Build and deployment → Source → GitHub Actions**.
2. Запушьте в `main` (или запустите workflow вручную во вкладке **Actions**).

Адрес сайта задаётся в `astro.config.mjs`:

- GitHub Pages по умолчанию: `site: 'https://<пользователь>.github.io'`,
  `base: '/<репозиторий>'`.
- Свой домен (например, `help.planplace.online`): `site: 'https://help.planplace.online'`,
  `base: '/'`, плюс файл `public/CNAME` с доменом и DNS-запись на GitHub Pages.

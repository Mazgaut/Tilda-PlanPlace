# Справочный центр PlanPlace

Документация PlanPlace на [Astro Starlight](https://starlight.astro.build/) —
статический сайт справки с авто-деплоем на GitHub Pages.

Почему так: каждая статья генерируется в готовый HTML, поэтому страницы
индексируются поисковиками и читаются ИИ-поисковиками, а меню и оформление
управляются централизованно из одного места.

## Как добавить новую статью

1. Создайте файл `src/content/docs/<slug>.mdx`.
2. В начале файла укажите «паспорт» статьи (front-matter):

   ```markdown
   ---
   title: Заголовок статьи
   description: Краткое описание для поисковиков и ИИ (140–160 символов).
   ---

   Текст статьи в Markdown…
   ```

3. Добавьте статью в меню в `src/sidebar.mjs`.
4. Закоммитьте и запушьте в ветку `main` — сайт пересоберётся и опубликуется сам.

Готовый HTML вручную писать не нужно — его собирает сборщик.

### Компоненты в статьях

Статьи — формата `.mdx`, но **`import`-строки писать не нужно** (их не понимает
визуальный редактор Keystatic). Нужные компоненты сборщик подключает сам
(remark-плагин `src/remark/auto-import-components.mjs`). Доступны:

```mdx
<Carousel>

![Подпись 1](../../assets/<slug>/02.jpg)
![Подпись 2](/Tilda-PlanPlace/media/<slug>/03.gif)

</Carousel>

<Video src="https://vkvideo.ru/video_ext.php?oid=...&id=..." />

<Download href="https://.../primer.xlsx" label="Скачать пример в формате Excel" />

<Bitrix24InlineForm />
```

- **Carousel** — галерея: изображения внутри обычным markdown (`![](...)`).
  Относительные пути Astro оптимизирует в WebP, GIF из `public/media` остаются
  анимированными.
- **Video** — адаптивное видео 16:9 (VK Видео, YouTube и т. п.).
- **Download** — кнопка скачивания файла-примера.
- **Bitrix24InlineForm** — встроенная форма обратной связи.

Эти же компоненты доступны как блоки в редакторе Keystatic. Если добавляете
новый компонент — пропишите его в `src/remark/auto-import-components.mjs`
(для сборки) и в `keystatic.config.ts` → `components` (для админки).

## Визуальная панель управления (Keystatic)

Для редактирования статей без работы с файлами есть админка **Keystatic**.

```bash
npm run cms      # запускает локальную админку на http://localhost:4321/keystatic
```

- Режим хранения — **локальный**: правки пишутся прямо в файлы `src/content/docs`,
  после чего их нужно закоммитить и запушить (сработает авто-деплой).
- Прод-сборка для GitHub Pages остаётся полностью **статической**: админка
  включается только локально (флаг `KEYSTATIC=true`, уже зашит в команду `cms`).

Конфигурация — в `keystatic.config.ts`.

**Размещённая (онлайн) админка.** Чтобы редактировать без локального запуска,
Keystatic нужно переключить на хранилище GitHub или Keystatic Cloud и разместить
на хостинге с серверным рендерингом (Netlify/Vercel/Cloudflare). GitHub Pages
для этого не подходит, так как отдаёт только статику. Сам сайт справки при этом
может остаться на GitHub Pages.

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

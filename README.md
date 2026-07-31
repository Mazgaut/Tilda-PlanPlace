# Справочный центр PlanPlace

Документация PlanPlace на [Astro Starlight](https://starlight.astro.build/) —
статический сайт справки с production-деплоем через GitVerse на
[help.planplace.online](https://help.planplace.online/).

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

<Img src="/Tilda-PlanPlace/media/<slug>/icon.png" alt="иконка" />            {/* в строку текста */}
<Img src="/Tilda-PlanPlace/media/<slug>/screen.png" alt="скрин" inline={false} />  {/* на отдельной строке */}

<Video src="https://vkvideo.ru/video_ext.php?oid=...&id=..." />

<Download href="https://.../primer.xlsx" label="Скачать пример в формате Excel" />

<Bitrix24InlineForm />
```

- **Carousel** — галерея: изображения внутри обычным markdown (`![](...)`).
  Относительные пути Astro оптимизирует в WebP, GIF из `public/media` остаются
  анимированными.
- **Img** — картинка с выбором отображения: встроить в строку текста (по
  умолчанию, удобно для иконок внутри предложения) или вынести на отдельную
  строку (`inline={false}`). Путь к картинке — как обычно, с префиксом
  `/Tilda-PlanPlace/...` (подгоняется под `base` автоматически).
- **Video** — адаптивное видео 16:9 (VK Видео, YouTube и т. п.).
- **Download** — кнопка скачивания файла-примера; тип файла (Excel или архив/3D)
  определяется по расширению в ссылке.
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

## Публикация и production-деплой

Актуальная цепочка публикации:

1. Исходный репозиторий —
   [Mazgaut/Tilda-PlanPlace](https://github.com/Mazgaut/Tilda-PlanPlace) на
   GitHub. Изменения коммитятся и отправляются сюда.
2. Workflow `.github/workflows/mirror-gitverse.yml` при каждом push зеркалирует
   текущий `HEAD` в ветку `master` репозитория
   [max41125/PlanPlace-information](https://gitverse.ru/max41125/PlanPlace-information)
   на GitVerse.
3. GitVerse является источником production-деплоя. Из его ветки `master`
   запускается обновление приложения на целевом сервере.
4. Публичный production-сайт — [help.planplace.online](https://help.planplace.online/).

> **Обязательное правило для следующих изменений:** GitHub Pages не входит в
> актуальную цепочку production-деплоя. Не нужно обновлять, запускать или
> настраивать деплой GitHub Pages, если отдельная задача явно этого не требует.
> Проверять результат следует локально и на `help.planplace.online` после
> прохождения зеркалирования и production-деплоя.

`npm run build` собирает статику в `./dist`. Для production сайт собирается в
корне домена: `SITE_URL=https://help.planplace.online`, `BASE_PATH=/`.

Внутренние ссылки и пути к картинкам с префиксом `/Tilda-PlanPlace/...`
автоматически подгоняются под текущий `base` (remark-плагин
`src/remark/base-links.mjs`), поэтому при смене `BASE_PATH` переписывать статьи
не нужно. Значения настраиваются в `astro.config.mjs`.

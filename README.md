# tg-artifacts

Артефакты Claude как Telegram Mini App. Сайт: https://asanalish.github.io/tg-artifacts/

- `index.html` — хаб и роутер: `t.me/AsanaliPages_bot/app?startapp=g37` открывает `g37/`
- `tg.js` — подключение к Telegram: полная высота, тема, цвета шапки, без сворачивания при прокрутке
- `pages.json` — список страниц для хаба
- `add_page.py` — добавить или обновить артефакт
- `post_to_channel.py` — пост в канал с кнопкой «Открыть»

## Добавить новый артефакт

```bash
python3 add_page.py nets ~/Downloads/nets.html "Сети с нуля" "Курс по сетям"
git add -A && git commit -m "add nets" && git push
```

Ссылка для канала: `https://t.me/AsanaliPages_bot/app?startapp=nets`

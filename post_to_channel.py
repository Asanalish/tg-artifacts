#!/usr/bin/env python3
"""Post a message with an "Открыть" button to your channel.

The button opens the Mini App right over the channel (no bot chat).
The bot must be an admin of the channel with the "Post messages" right.

Usage:
  BOT_TOKEN=123:abc python3 post_to_channel.py @my_channel g37 "Текст поста"
Optional env: BOT_USERNAME (default read from the token), APP_NAME (default "app"),
              BUTTON (default "Открыть"), MODE ("fullscreen" / "compact", default none).
"""
import json, os, sys, urllib.request, urllib.parse

token = os.environ.get('BOT_TOKEN') or sys.exit('set BOT_TOKEN')
if len(sys.argv) != 4:
    sys.exit(__doc__)
channel, slug, text = sys.argv[1:]

def api(method, **params):
    data = urllib.parse.urlencode({k: v for k, v in params.items() if v is not None}).encode()
    with urllib.request.urlopen(f'https://api.telegram.org/bot{token}/{method}', data) as r:
        res = json.load(r)
    if not res.get('ok'):
        sys.exit(res)
    return res['result']

bot = os.environ.get('BOT_USERNAME') or api('getMe')['username']
url = f"https://t.me/{bot}/{os.environ.get('APP_NAME', 'app')}?startapp={slug}"
if os.environ.get('MODE'):
    url += f"&mode={os.environ['MODE']}"

# Channels don't accept web_app buttons, only url buttons; a t.me/<bot>/<app>
# link in a url button still opens the Mini App in place.
kb = {'inline_keyboard': [[{'text': os.environ.get('BUTTON', 'Открыть'), 'url': url}]]}
msg = api('sendMessage', chat_id=channel, text=text, reply_markup=json.dumps(kb))
print('posted:', msg['message_id'], url)

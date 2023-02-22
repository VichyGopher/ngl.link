import httpx, threading, uuid, time, itertools
from httpx_socks import SyncProxyTransport

__proxies__, __i__ = itertools.cycle(open('./proxies.txt', 'r+').read().splitlines()), 0

user = input('user: ')

headers = {
    'authority': 'ngl.link',
    'accept': '*/*',
    'accept-language': 'fr-FR,fr;q=0.7',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'origin': 'https://ngl.link',
    'referer': f'https://ngl.link/{user}',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sec-gpc': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
}

data = {
    'username': user,
    'question': str(uuid.uuid4()),
    'deviceId': str(uuid.uuid4()),
    'gameSlug': '',
    'referrer': '',
}

def send():
    global __i__
    transport = SyncProxyTransport.from_url(next(__proxies__))

    c = httpx.Client(transport= transport, timeout=5000)
    while True:
        response = c.post('https://ngl.link/api/submit', headers=headers, data=data)
        if response.status_code == 429:
            time.sleep(5)
            print('ratelimit')
        else:
            __i__ += 1
            print(__i__, response.status_code, response.text)

for _ in range(100):
    threading.Thread(target=send).start()
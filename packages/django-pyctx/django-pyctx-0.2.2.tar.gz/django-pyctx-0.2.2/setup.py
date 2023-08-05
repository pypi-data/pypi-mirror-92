# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_pyctx', 'django_pyctx.migrations']

package_data = \
{'': ['*']}

install_requires = \
['Django>2.2', 'pyctx>0.1.7']

setup_kwargs = {
    'name': 'django-pyctx',
    'version': '0.2.2',
    'description': 'Context package to use data between function calls, use timers and log it for Django.',
    'long_description': 'PyCTX for Django\n================\n\n**django-pyctx** is a context package to use data between function calls, use timers and log it.\n\nFor detailed documentation please visit [Wiki](https://github.com/molcay/django-pyctx/wiki).\n\nQuick Start\n-----------\n\n1. Add **django_pyctx** to your ``INSTALLED_APPS``\xa0 setting like this:\n\n   ```python\n   INSTALLED_APPS = [\n    #...,\n    "django_pyctx",\n   ]\n   ```\n\n2. Add **django_pyctx.middlewares.RequestCTXMiddleware** to your ``MIDDLEWARE`` setting like this:\n\n   ```python\n   MIDDLEWARE = [\n     "django_pyctx.middlewares.RequestCTXMiddleware",\n     # ...,\n   ]\n   ```\n\n> Please add "django_pyctx.middlewares.RequestCTXMiddleware" to at the beginning of the MIDDLEWARE list.\n\n3. Start the development server and enjoy :)\n\nSample Usage\n------------\n\n- You can reach `RequestContext` instance in **views** from `request`: `request.ctx`\n\n- Example django function-based `view`:\n\n    ```python\n  from django.http import JsonResponse\n  \n  \n  def index(request):\n        y = 5\n        with request.ctx.log.timeit(\'index_timer\'):\n            request.ctx.log.set_data(\'isEven\', y % 2)\n            request.ctx.log.set_data(\'y\', y)\n            request.ctx.log.start_timer(\'timer1\')\n            import time\n            time.sleep(0.3)\n            request.ctx.log.stop_timer(\'timer1\')\n            time.sleep(0.8)\n            return JsonResponse({})\n    ```\n\nYou can see the stdout. You are probably seeing something like this:\n\n```json\n{\n  "type": "REQ",\n  "ctxId": "a9b66113-aa96-4419-b9ec-961ce0ebf3ae",\n  "startTime": "2019-08-23 13:47:46.146172",\n  "endTime": "2019-08-23 13:47:47.258287",\n  "data": {\n    "isEven": 1,\n    "y": 5\n  },\n  "timers": {\n    "ALL": 1.112128,\n    "request": 1.112115,\n    "index_timer": 1.107513,\n    "timer1": 0.302767\n  },\n  "http": {\n    "request": {\n      "method": "GET",\n      "path": "/ctxtest",\n      "qs": "",\n      "full_path": "/ctxtest",\n      "is_secure": false,\n      "is_xhr": false,\n      "headers": {\n        "Content-Length": "",\n        "Content-Type": "text/plain",\n        "Host": "localhost:8000",\n        "Connection": "keep-alive",\n        "Cache-Control": "max-age=0",\n        "Upgrade-Insecure-Requests": "1",\n        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36",\n        "Sec-Fetch-Mode": "navigate",\n        "Sec-Fetch-User": "?1",\n        "Dnt": "1",\n        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",\n        "Sec-Fetch-Site": "none",\n        "Accept-Encoding": "gzip, deflate, br",\n        "Accept-Language": "tr,en-GB;q=0.9,en;q=0.8,en-US;q=0.7",\n        "Cookie": "Pycharm-358d8f24=40efd37d-3767-43c2-8704-8abdbc8e441c; hblid=2S0d7GIKtYrYxbaF3m39N0M07TEBJbrW; olfsk=olfsk09308937734654421; Pycharm-358d92e3=f744a971-3d23-48a3-8188-7818d8efeb90; jenkins-timestamper-offset=-10800000; Pycharm-358d92e4=39469e28-3138-45a1-8133-16b05a158037; __test=1; csrftoken=qAbZmh519QGb6c1h702qe3YOtL8Q0ADakbXqqj4o5G5UznTybJVPigGG1mDBTtgP; Idea-535a2bcb=d87ec75d-65c5-46dd-a04b-6e914b434b5a; lang=en-US; iconSize=32x32; JSESSIONID.3e560a2e=node015mpq963ev6tulzcbplgyu8i1438.node0"\n      }\n    },\n    "client": {\n      "ip": "127.0.0.1",\n      "host": "",\n      "agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36"\n    },\n    "status": {\n      "code": 200,\n      "phrase": "OK"\n    },\n    "server": {\n      "name": "1.0.0.127.in-addr.arpa",\n      "port": "8000"\n    },\n    "view": "run"\n  }\n}\n```\n> NOTE: this output formatted\n',
    'author': 'M. Olcay TERCANLI',
    'author_email': 'molcay@mail.com',
    'maintainer': 'M. Olcay TERCANLI',
    'maintainer_email': 'molcay@mail.com',
    'url': 'https://github.com/molcay/django-pyctx',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>3.7.0',
}


setup(**setup_kwargs)

import asyncio
import aiohttp
import socket
from aiohttp.resolver import AsyncResolver
from urllib.parse import urlparse


class DownloadError(Exception):
    def __init__(self, msg, url=None):
        super().__init__(msg)
        self.url = url


async def start_download(urls):
    tasks = set()
    loop = asyncio.get_event_loop()
    for i in range(0, len(urls)):
        if len(tasks) >= 10:
            _done, tasks = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
        tasks.add(loop.create_task(download_article(urls[i])))
    result, pending = await asyncio.wait(tasks)
    data = list()
    for future in result:
        try:
            data.append(future.result())
        except DownloadError:
            data.append(future.exception())
    return data


async def download_article(url):
    try:
        url = url.strip()
        parsed = list(urlparse(url))
        if not parsed[0]:
            parsed[0] = 'http'
        host = parsed[1].lower()
        if not host:
            raise DownloadError('Невалидный URL', url=url)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3886.0 Safari/537.36',
            'Host': host
        }
        loop = asyncio.get_event_loop()
        resolver = AsyncResolver()
        conn = aiohttp.TCPConnector(
            resolver=resolver, family=socket.AF_INET, verify_ssl=True, ttl_dns_cache=None, loop=loop)
        async with aiohttp.ClientSession(connector=conn, loop=loop) as http_session:
            timeout = aiohttp.ClientTimeout(sock_connect=60)
            async with http_session.get(url, raise_for_status=True, headers=headers,
                                        timeout=timeout) as response:
                buff = await response.text()
    except (aiohttp.ClientConnectionError, aiohttp.ClientResponseError, aiohttp.ClientPayloadError) as exc:
        raise DownloadError(f'Сетевая ошибка: {str(exc)}', url=url)
    except aiohttp.InvalidURL as exc:
        raise DownloadError(f'Невалидный URL статьи: {str(exc)}', url=url)
    except asyncio.TimeoutError:
        raise DownloadError('Не удалось скачать статью за отведенное время', url=url)
    except AssertionError as exc:
        raise DownloadError(f'Не удалось скачать статью: {exc}', url=url)

    return url, buff

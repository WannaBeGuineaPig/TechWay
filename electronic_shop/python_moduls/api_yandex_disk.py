import aiohttp.client_exceptions
import requests, aiohttp

URL = 'https://cloud-api.yandex.net/v1/disk/resources' # path url api yandex disk
TOKEN = 'y0__xC6nY7_BRjblgMg08nKvhKjPXyvOQKRvoPOJtzgmZ3qeF2XFw' # token my app for api
HEADERS = {
    'Content-Type': 'application/json', 
    'Accept': 'application/json', 
    'Authorization': f'OAuth {TOKEN}'
}

__all__ = [
    'create_folder',
    'get_images_product'
]

def create_folder(path):
    """
    Создание папки.\n
    path: Путь к создаваемой папке.
    """
    requests.put(f'{URL}?path=images_product/{path}', headers=HEADERS)

async def get_images_product(path):
    """
    """
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f'{URL}?path=images_product/{path}', headers=HEADERS) as response:
                text = await response.json()
                return text['_embedded']['items']
    except aiohttp.client_exceptions.ClientConnectionError:
        return ""

# def get_images_product():
#     """
#     """
#     return requests.get(f'{URL}/files/?path=images_product', headers=HEADERS)
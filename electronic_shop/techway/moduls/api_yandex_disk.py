import requests

URL = 'https://cloud-api.yandex.net/v1/disk/resources' # path url api yandex disk
TOKEN = 'y0__xC6nY7_BRjblgMg08nKvhKjPXyvOQKRvoPOJtzgmZ3qeF2XFw' # token my app for api
HEADERS = {
    'Content-Type': 'application/json', 
    'Accept': 'application/json', 
    'Authorization': f'OAuth {TOKEN}'
}

__all__ = [
    'create_folder',
    'get_all_items'
]

def create_folder(path):
    """
    Создание папки.\n
    path: Путь к создаваемой папке.
    """
    requests.put(f'{URL}?path=images_product/{path}', headers=HEADERS)

def get_all_items(path):
    """
    """
    return requests.get(f'{URL}?path=images_product/{path}', headers=HEADERS)

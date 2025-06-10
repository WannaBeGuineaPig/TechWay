import hashlib, asyncio, httpx, string
from googletrans import Translator
from random import choices

__all__ = [
    'hash_password',
    'translate_text',
    'create_hash',
]

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

async def output_translate_text(text: str) -> str:
    async with Translator() as translator:
        try:
            new_text = await translator.translate(text, dest='ru')
            return new_text.text
        except httpx.ConnectError:
            return text
    
def translate_text(text: str) -> str:
    text = asyncio.run(output_translate_text(text))
    return text

def create_hash(length_hash: int = 1):
    chars = string.ascii_letters + string.digits
    return ''.join(choices(chars, k=length_hash))
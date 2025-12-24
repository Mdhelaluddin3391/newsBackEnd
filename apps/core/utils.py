from django.utils.text import slugify
import uuid

def unique_slug(text: str) -> str:
    return f"{slugify(text)}-{uuid.uuid4().hex[:6]}"

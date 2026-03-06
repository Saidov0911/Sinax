from PIL import Image

ALLOWED_LANGS = ['uz', 'ru', 'en']


def get_lang(request, default='uz'):
    if request is None:
        return default
    lang = request.query_params.get('lang', default)
    return lang if lang in ALLOWED_LANGS else default


def resize_image(path, max_width, max_height, quality=85):
    with Image.open(path) as img:
        img_format = img.format if img.format else 'JPEG'

        if img_format == 'JPEG' and img.mode in ('RGBA', 'P'):
            img = img.convert('RGB')

        img.thumbnail((max_width, max_height), Image.LANCZOS)

        save_kwargs = {'format': img_format, 'optimize': True}
        if img_format == 'JPEG':
            save_kwargs['quality'] = quality

        img.save(path, **save_kwargs)
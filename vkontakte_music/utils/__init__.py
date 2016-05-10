from vkontakte_music import settings


def apply(call):
    def decorator(func):
        def wrapper(*args, **kwargs):
            return call(func(*args, **kwargs))
        return wrapper
    return decorator


def filter_text(text):
    """Remove invalid symbols from string"""
    return ''.join(c if c in settings.VALID_CHARS else settings.REPLACE_CHAR for c in text.strip())


def get_audio_filename(audio, ext='.mp3'):
    """
    :param dict audio:
    :rtype: str
    """
    filename = filter_text(u'{0[artist]} - {0[title]}'.format(audio))
    if ext:
        filename += ext
    return filename


def get_artist(audio):
    artist = filter_text(audio['artist'])
    chars = ['&', 'vs', 'ft', 'feat']
    for ch in chars:
        index = artist.find(ch)
        if index > 0:
            artist = artist[:index].strip()
    return artist
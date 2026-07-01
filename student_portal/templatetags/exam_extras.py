from django import template

register = template.Library()

@register.filter
def get_option_media(media_files, media_type):
    """Return the QuestionMedia object matching media_type, or None."""
    for media in media_files:
        if media.media_type == media_type:
            return media
    return None
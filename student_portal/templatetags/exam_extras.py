import re
from django import template
from django.utils.safestring import mark_safe
import bleach

register = template.Library()

ALLOWED_TAGS = ['sup', 'sub', 'b', 'i', 'em', 'strong', 'br', 'u']


@register.filter
def get_option_media(media_files, media_type):
    """Return the QuestionMedia object matching media_type, or None."""
    for media in media_files:
        if media.media_type == media_type:
            return media
    return None


@register.filter
def safe_math(value):
    if not value:
        return value

    value = str(value)

    # Normalize line breaks: any run of blank/newline whitespace -> ONE <br>
    value = value.replace('\r\n', '\n')
    value = re.sub(r'\s*\n\s*', '<br>', value.strip())

    # Explicit superscript markup: 10^23 -> 10<sup>23</sup>, mol^-1 -> mol<sup>-1</sup>
    value = re.sub(r'\^([A-Za-z0-9+\-]+)', r'<sup>\1</sup>', value)

    # Explicit subscript markup: H_2O -> H<sub>2</sub>O
    value = re.sub(r'_([A-Za-z0-9]+)', r'<sub>\1</sub>', value)

    # Scientific notation WITHOUT a caret: "x 10" or "× 10" followed
    # directly by digits is unambiguous (unlike a bare letter+digit),
    # so it's safe to auto-superscript even without explicit "^" markup.
    # Matches: "x 106" / "× 106" / "x10^6" already-caret'd (skipped, since
    # the <sup> above would already have consumed it) -> 10<sup>6</sup>
    value = re.sub(
        r'([x×])\s*10(\d+)\b',
        r'\1 10<sup>\2</sup>',
        value
    )

    # Ionic/charge notation BEFORE the generic subscript rule below
    # Matches: Fe3+(aq), H+(aq), I-(aq), Mg2+(aq)
    value = re.sub(r'(\d*)([+\-])(?=\()', r'<sup>\1\2</sup>', value)

    # Auto-subscript numbers directly adjacent to a letter/bracket
    value = re.sub(r'(?<=[A-Za-z\)\]])(\d+)', r'<sub>\1</sub>', value)

    cleaned = bleach.clean(value, tags=ALLOWED_TAGS, strip=True)
    return mark_safe(cleaned)
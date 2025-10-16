import re

from rest_framework.exceptions import ValidationError


class UrlValidator:

    def __init__(self):
        self.pattern = re.compile(r"https?://(www\.|m\.)?youtube\.com/.*")

    def __call__(self, value, *args, **kwargs):
        if not self.pattern.match(value):
            raise ValidationError(
                "Ссылка должна вести на ресурс YouTube. Использование других видео-хостингов запрещено."
            )

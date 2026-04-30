from rest_framework.validators import ValidationError
import re


class CheckingVideoLink:
    """Проверка, что видео расположено на видеохостинге youtube.com"""
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        pattern = re.compile(r'youtube.com')
        sentence = dict(value).get(self.field)
        matches = pattern.search(sentence)
        if not matches:
            raise ValidationError("Ссылка на видео материал должен вести только на хостинг YouTube!")

from django.utils import timezone

current_datetime = timezone.localtime(timezone.now()).date()

print(current_datetime)
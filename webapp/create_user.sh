
manage.py shell
from django.contrib.auth.models import User
user=User.objects.create_user('$1', password='$2')
user.is_superuser=True
user.is_staff=True
user.save()


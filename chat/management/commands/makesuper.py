from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    def handle(self, *args, **options):
        User = get_user_model()
        if not User.objects.filter(is_superuser = True):
            host = settings.ROOT_URLCONF.split('.')[0]
            User.objects.create_superuser(
                'admin', f'admin@{host}.com' , 'admin'
            )
            self.stdout.write(self.style.SUCCESS("***Admin User Created***"))
        else:
            self.stdout.write(self.style.ERROR("***Admin User already exists***"))

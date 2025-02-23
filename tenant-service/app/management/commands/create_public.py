from django.core.management.base import BaseCommand
from app.models import UserCache , Tenants



class Command(BaseCommand):
    help = "Creating the public tenant"
    def handle(self,*args, **kwargs):
        user = UserCache.objects.get(username = "admin")
        if not Tenants.objects.filter(subdomain="public").exists():
            Tenants.objects.create(name="Public", subdomain="public", admin=user)
            self.stdout.write(self.style.SUCCESS('Public tenant created successfully'))
        else:
            self.stdout.write(self.style.WARNING('Public tenant already exists'))
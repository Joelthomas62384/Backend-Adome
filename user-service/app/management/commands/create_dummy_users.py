from django.core.management.base import BaseCommand
from app.models import Tenants, User, TenantUsers
from faker import Faker

fake = Faker()

class Command(BaseCommand):
    help = "Creating dummy users for each tenant"

    def add_arguments(self, parser):
        parser.add_argument('count', type=int, help='Total number of users to be created.',default=50 , nargs='?')

    def handle(self, *args, **options):
        count = options.get('count', 50)
        tenant = Tenants.objects.get(subdomain='brototype')

        for _ in range(count):
            email = fake.email()
            username = fake.user_name()
            full_name = fake.name()

            print(f"Creating User - Email: {email}, Username: {username}, Full Name: {full_name}")

            user = User.objects.create(
                email=email,
                username=username,
                full_name=full_name
            )

            if user is None or user.email is None:
                print("[ERROR] User creation failed!")
                continue  

            print(f"[SUCCESS] Created User - {user}")

            tenant_user = TenantUsers.objects.create(tenant=tenant, user=user)
            print(f"[SUCCESS] Assigned {user} to {tenant}")

        self.stdout.write(self.style.SUCCESS(f'{count} dummy users created for tenant brototype'))

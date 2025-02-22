from . models import *

from django.db.models.signals import post_save , pre_delete
from django.dispatch import receiver
from .producers import Publisher
from .serializers import TenantSerializer






@receiver(post_save, sender=Tenants)
def send_tenant_data(sender, instance, created, **kwargs):
    serializer = TenantSerializer(instance)
    if created :
        Publisher(serializer.data , "tenant" , "created")
    else:
        Publisher(serializer.data , "tenant" , "updated")
    print("Data published successfully")


@receiver(pre_delete, sender=Tenants)
def send_tenant_delete_data(sender, instance, **kwargs):
    serializer = TenantSerializer(instance)
    Publisher(serializer.data , "tenant" , "deleted")
    print("Data published successfully")
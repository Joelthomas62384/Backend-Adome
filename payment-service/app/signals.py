from django.db.models.signals import post_save , pre_delete
from django.dispatch import receiver
from .models import Tenants
from . serializers import PaymentSerializer
from.producers import Publisher


@receiver(post_save, sender=Tenants)
def send_tenant_data(sender, instance, created, **kwargs):
    if not created:
        serializer = PaymentSerializer(instance)
        Publisher(serializer.data ,"subscription" , "updated" )
        print("Subscription update sent")
        

from django.db.models.signals import post_save , pre_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from . serializers import *
from . producer import Publisher
User = get_user_model()
from .models import TenantUsers



@receiver(post_save, sender=User)
def send_user_data(sender, instance, created, **kwargs):
    serializer = UserSerializer(instance)
    
    if created :
        Publisher(serializer.data , "user" , "created")
    else:
        Publisher(serializer.data , "user" , "updated")
    print("Data published successfully")



@receiver(pre_delete, sender=User)
def send_deleted_user_data(sender, instance, **kwargs):
    serializer = UserSerializer(instance)
    Publisher(serializer.data , "user" , "deleted")
    print("Data published successfully")


@receiver(post_save, sender=TenantUsers)
def send_tenantusers_data(sender,  instance, created, **kwargs):
    serializer = TenantUserSerializer(instance)
    if created :
        Publisher(serializer.data , "tenantuser" , "created")
    else:
        Publisher(serializer.data , "tenantuser" , "updated")
    print("Data published successfully")



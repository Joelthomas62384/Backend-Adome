from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete
from . models import Course
from .producer import Publisher
from mysite.serializers import PublishCourseSerializer








@receiver(post_save , sender=Course)
def create_tenant_wallet(sender, instance, created, **kwargs):
    if created:
        serializer  = PublishCourseSerializer(instance)
        Publisher(serializer.data , "course" , "created")
    else:
        serializer  = PublishCourseSerializer(instance)
        Publisher(serializer.data , "course" , "updated")


@receiver(pre_delete, sender=Course)
def send_deleted_user_data(sender, instance, **kwargs):
    serializer = PublishCourseSerializer(instance)
    Publisher(serializer.data , "course" , "deleted")
    print("Data published successfully")
        


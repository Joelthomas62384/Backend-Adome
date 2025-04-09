from rest_framework import serializers
from app.models import Course

class CourseSerializer(serializers.ModelSerializer):
    """
    class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    tenant = models.ForeignKey(Tenants, on_delete=models.CASCADE)
    thumbnail = models.TextField()
    price = models.FloatField()
    published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    """

    class Meta:
        model = Course
        fields = "__all__"
        read_only_fields = [
            'created_at' , 'tenant' , 'updated_at' , 
        ]
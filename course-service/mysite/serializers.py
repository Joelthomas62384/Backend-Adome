from rest_framework import serializers
from app.models import Course

class CourseSerializer(serializers.ModelSerializer):
    """
    title = models.CharField(max_length=200)
    tenant = models.ForeignKey(Tenants, on_delete=models.CASCADE)
    thumbnail = models.TextField()
    content = models.TextField()
    htmlContent = models.TextField(null=True , blank=True)
    JsonContent = models.JSONField(null=True , blank=True)
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
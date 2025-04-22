from rest_framework import serializers
from app.models import Course, Module , Chapter

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


class ModuleSerializer(serializers.ModelSerializer):
    """
    title = models.CharField(max_length=200)
    description = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    """
    class Meta:
        model = Module
        fields = "__all__"
        read_only_fields = [
            'created_at' , 'updated_at'
        ]

class ChapterSerializer(serializers.ModelSerializer):
    """
    title = models.CharField(max_length=200)
    module = models.ForeignKey(Module, on_delete=models.CASCADE , null=True ,blank=True)
    has_video = models.BooleanField(default=True)
    content = models.TextField()
    htmlContent = models.TextField(null=True , blank=True)
    JsonContent = models.JSONField(null=True , blank=True)
    video = models.TextField(null=True , blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    preview = models.BooleanField(default=False)
    
    """

    class Meta:
        model = Chapter
        fields = "__all__"
        read_only_fields = [
            'created_at' , 'updated_at' ,'id'
        ]
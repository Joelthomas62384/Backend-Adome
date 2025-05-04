from rest_framework import serializers
from app.models import Course, Module , Chapter, OwnedCourse

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
    owned = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = "__all__"
        read_only_fields = [
            'created_at' , 'tenant' , 'updated_at' , 'owned'
        ]
    def get_owned(self, obj):
        try:
            tenantuser = self.context['request'].tenantuser
            return OwnedCourse.objects.filter(course=obj, user=tenantuser).exists()
        except AttributeError:
            return False
        # return False
        

class PublishCourseSerializer(serializers.ModelSerializer):
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
            'created_at' , 'tenant' , 'updated_at'
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
            'created_at' , 'updated_at' 
        ]







class ChapterPreviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = ['title']


class ModulePreviewSerializer(serializers.ModelSerializer):
    chapters = ChapterPreviewSerializer(many=True, source='chapter_set')

    class Meta:
        model = Module
        fields = ['title', 'chapters']


class CoursePreviewSerializer(serializers.ModelSerializer):
    owned = serializers.SerializerMethodField()
    preview_video = serializers.SerializerMethodField()
    modules = ModulePreviewSerializer(many=True, source='module_set')

    class Meta:
        model = Course
        fields = ['title', 'content', 'modules', "htmlContent" , "JsonContent","thumbnail" , "preview_video" ,'price' , 'owned']  
    def get_owned(self, obj):
        try:
            tenantuser = self.context['request'].tenantuser
            return OwnedCourse.objects.filter(course=obj, user=tenantuser).exists()
        except AttributeError:
            return False




    
    def get_preview_video(self, obj):
        first_module = obj.module_set.order_by('id').first()
        if not first_module:
            return None

        first_chapter = first_module.chapter_set.order_by('id').first()
        if not first_chapter:
            return None

        return first_chapter.video if first_chapter.video else None



class ChapterWatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = [
            'id', 'title', 'content', 'htmlContent', 'JsonContent', 'preview', 'created_at', 'video'
        ]


class ModuleWatchSerializer(serializers.ModelSerializer):
    chapters = ChapterWatchSerializer(many=True, read_only=True, source='chapter_set')

    class Meta:
        model = Module
        fields = ['id', 'title', 'description', 'chapters', 'created_at']



class CourseWatchSerializer(serializers.ModelSerializer):
    modules = ModuleWatchSerializer(many=True, read_only=True, source='module_set')
    owned = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = [
            'id', 'title', 'price', 'published', 'modules', 'created_at', 'owned'
        ]
    def get_owned(self, obj):
        try:
            tenantuser = self.context['request'].tenantuser
            return OwnedCourse.objects.filter(course=obj, user=tenantuser).exists()
        except AttributeError:
            return False





class OwnedCourseSerializer(serializers.ModelSerializer):
    course = serializers.SerializerMethodField()

    class Meta:
        model = OwnedCourse
        fields = ['course']

    def get_course(self, obj):
        serializer = CourseSerializer(obj.course, context=self.context)
        return serializer.data
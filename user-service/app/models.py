from django.db import models
from django.contrib.auth.models import AbstractBaseUser , PermissionsMixin , BaseUserManager

from django.contrib.auth.models import AbstractUser, Group, Permission

class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        if not username:
            raise ValueError("The Username field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        """Create and return a superuser with specific properties."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, username, password, **extra_fields)



class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=100 , null=True)
    username = models.CharField(max_length=250, unique=True)
    profile_pic = models.TextField(null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = CustomUserManager()
    groups = models.ManyToManyField(Group, related_name="custom_user_groups", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="custom_user_permissions", blank=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'full_name']

    def __str__(self):
        return self.username
    
    


class Tenants(models.Model):
    name = models.CharField(max_length=100 , unique=True)
    subdomain = models.CharField(max_length=100,unique=True)

    def __str__(self):
        return self.subdomain
    
    class Meta:
        verbose_name = 'Tenant'
        verbose_name_plural = 'Tenants'
    

class TenantUsers(models.Model):
    tenant = models.ForeignKey(Tenants, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    blocked = models.BooleanField(default=False)
    banned = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    designation = models.CharField(max_length=100,default='' , null=True , blank=True)
    hasStaffPermission = models.BooleanField(default=False)
    hasBlogPermission = models.BooleanField(default=False)
    hasCommunityPermission = models.BooleanField(default=False)
    hasNewsletterPermission = models.BooleanField(default=False)
    hasCoursesPermission = models.BooleanField(default=False)
    hasBuilderPermission = models.BooleanField(default=False)
    

    def __str__(self):
        return f"{self.user.username} in {self.tenant.name}"
    
    class Meta:
        unique_together = ('tenant', 'user')
        verbose_name = 'Tenant User'
        verbose_name_plural = 'Tenant Users'
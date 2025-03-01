from django.db import models

class UserCache(models.Model):
    username = models.CharField(max_length=150, unique=True )
    is_active = models.BooleanField(default=True)

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


class LogoImages(models.Model):
    file = models.ImageField(upload_to='logos/')
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(UserCache, on_delete=models.CASCADE)
    def __str__(self):
        return f"Logo of {self.user.username}"
    
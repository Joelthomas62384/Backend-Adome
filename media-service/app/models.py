from django.db import models

class UserCache(models.Model):
    username = models.CharField(max_length=150, unique=True )

    def __str__(self):
        return self.username
    



class LogoImages(models.Model):
    logo = models.ImageField(upload_to='logos/')
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(UserCache, on_delete=models.CASCADE)
    def __str__(self):
        return f"Logo of {self.user.username}"
    
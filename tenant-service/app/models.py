from django.db import models







class UserCache(models.Model):
    username = models.CharField(max_length=150,unique=True )
    is_active = models.BooleanField(default=True,)
    
    def __str__(self):
        return self.username
    



class Tenants(models.Model):
    sub_choices = (
        
        ('1', 'Free'),
        ('2', 'Premium'),
    )
    name = models.CharField(max_length=100,unique=True)
    subscription_plan = models.CharField(choices=sub_choices , max_length=100 , default="1")
    logo = models.TextField(null=True,blank=True)
    domain = models.CharField(max_length=250,null=True)
    contact_email = models.EmailField(null=True,blank=True)
    location = models.CharField(max_length=100 , blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    blog =models.BooleanField(default=True)
    community = models.BooleanField(default=False)
    newsletter = models.BooleanField(default=False)
    subdomain = models.CharField(max_length=150 ,unique=True)
    courses = models.BooleanField(default=False)
    admin = models.ForeignKey(UserCache, on_delete=models.CASCADE)



    created_on = models.DateField(auto_now_add=True)
    auto_create_schema = True
    auto_drop_schema = True

    def __str__(self):
        return self.name
    



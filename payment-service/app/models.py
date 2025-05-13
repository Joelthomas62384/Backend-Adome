from django.db import models
from cryptography.fernet import Fernet
from django.conf import settings


fernet = Fernet(settings.ENCRYPTION_KEY)
class UserCache(models.Model):
    """
    [ id, name , email , full_name , username , profile_pic , is_staff , is_active , is_superuser , created_at , updated_at]
    """
    username = models.CharField(max_length=150, unique=True )
    full_name = models.CharField(max_length=100 , null=True)
    profile_pic = models.TextField(null=True)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.username



class Tenants(models.Model):
    sub_choices = (
        
        ('1', 'Free'),
        ('2', 'Premium'),
    )
    name = models.CharField(max_length=100,unique=True)
    subscription_plan = models.CharField(choices=sub_choices , max_length=100 , default="1")
    subdomain = models.CharField(max_length=150 ,unique=True)

    def __str__(self):
        return self.name


class TenantUsers(models.Model):
    user = models.ForeignKey(UserCache , on_delete=models.CASCADE)
    tenant = models.ForeignKey(Tenants , on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    blocked = models.BooleanField(default=False)
    banned = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.user.username + ' in ' + self.tenant.name
    
    class Meta:
        unique_together = ('tenant', 'user')
        verbose_name = 'Tenant User'
        verbose_name_plural = 'Tenant Users'
class TenantPayments(models.Model):
    tenant = models.OneToOneField(Tenants, on_delete=models.CASCADE)
    razorpay_account_id = models.CharField(max_length=100, null=True, blank=True)
    encrypted_email = models.TextField(null=True, blank=True)
    encrypted_name = models.TextField(null=True, blank=True)
    encrypted_bank_account_number = models.TextField(null=True, blank=True)
    encrypted_bank_ifsc = models.TextField(null=True, blank=True)
    encrypted_pan_number = models.TextField(null=True, blank=True)
    encrypted_phone_number = models.CharField(max_length=100 , null=True , blank=True)

    def __str__(self):
        return self.tenant.name

    def encrypt_value(self, value):
        if value:
            return fernet.encrypt(value.encode()).decode()
        return None

    def decrypt_value(self, value):
        if value:
            return fernet.decrypt(value.encode()).decode()
        return None

    @property
    def email(self):
        return self.decrypt_value(self.encrypted_email)

    @email.setter
    def email(self, value):
        self.encrypted_email = self.encrypt_value(value)

    @property
    def name(self):
        return self.decrypt_value(self.encrypted_name)

    @name.setter
    def name(self, value):
        self.encrypted_name = self.encrypt_value(value)

    @property
    def bank_account_number(self):
        return self.decrypt_value(self.encrypted_bank_account_number)

    @bank_account_number.setter
    def bank_account_number(self, value):
        self.encrypted_bank_account_number = self.encrypt_value(value)

    @property
    def bank_ifsc(self):
        return self.decrypt_value(self.encrypted_bank_ifsc)

    @bank_ifsc.setter
    def bank_ifsc(self, value):
        self.encrypted_bank_ifsc = self.encrypt_value(value)

    @property
    def pan_number(self):
        return self.decrypt_value(self.encrypted_pan_number)

    @pan_number.setter
    def pan_number(self, value):
        self.encrypted_pan_number = self.encrypt_value(value)

    @property
    def phone(self):
        return self.decrypt_value(self.encrypted_phone_number)

    @phone.setter
    def phone(self, value):
        self.encrypted_phone_number = self.encrypt_value(value)

    def save(self, *args, **kwargs):
        # Automatically encrypt the fields before saving
        if self.email:
            self.encrypted_email = self.encrypt_value(self.email)
        if self.name:
            self.encrypted_name = self.encrypt_value(self.name)
        if self.bank_account_number:
            self.encrypted_bank_account_number = self.encrypt_value(self.bank_account_number)
        if self.bank_ifsc:
            self.encrypted_bank_ifsc = self.encrypt_value(self.bank_ifsc)
        if self.pan_number:
            self.encrypted_pan_number = self.encrypt_value(self.pan_number)
        if self.phone:
            self.encrypted_phone_number = self.encrypt_value(self.phone)

        super().save(*args, **kwargs)


class CourseCache(models.Model):
    title = models.CharField(max_length=200 , null=True , blank=True)
    price = models.FloatField()

class TenantWallet(models.Model):
    tenant = models.OneToOneField(Tenants , on_delete=models.CASCADE)
    total_amount = models.DecimalField(default=0 , decimal_places=2, max_digits=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return self.tenant.name
    



class Order(models.Model):
    user = models.ForeignKey(TenantUsers , on_delete=models.CASCADE , null=True ,blank=True)
    course = models.ForeignKey(CourseCache, on_delete=models.CASCADE)
    tenant = models.ForeignKey(Tenants, on_delete=models.CASCADE , null=True , blank=True)
    course_title = models.CharField(max_length=255)
    order_product = models.CharField(max_length=100)
    order_amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default="INR")
    razorpay_order_id = models.CharField(max_length=100, unique=True)
    order_payment_id = models.CharField(max_length=100, unique=True, blank=True, null=True)
    order_signature = models.CharField(max_length=256, blank=True, null=True)
    is_paid = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    order_status = models.CharField(max_length=20, default="created")
    payment_method = models.CharField(max_length=50, blank=True, null=True)
    payment_time = models.DateTimeField(blank=True, null=True , auto_now=True)
    order_date = models.DateTimeField(auto_now_add=True)



    def __str__(self):
        return f"{self.user_id} - {self.course_id} - ₹{self.order_amount}"

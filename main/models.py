from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin
)
from django_jalali import models as jmodels
import jdatetime
from . import managers
from django.core.validators import RegexValidator

# Create your models here.

# Create custom User model for this application
# this user model inheritence from AbstractBaseUser model
# that have their abstract behavior and attributes 
class User(AbstractBaseUser, PermissionsMixin):

    username = models.CharField(
        db_index=True, max_length=100, null=False, blank=False, 
        unique=True, verbose_name="نام کاربری"
    )

    email = models.EmailField(
        db_index=True, max_length=255, null=True, blank=True,
        unique=True, verbose_name="آدرس ایمیل"
    )

    is_active = models.BooleanField(
        default=True, null=False, blank=True, verbose_name="وضعیت"
    )

    is_admin = models.BooleanField(
        default=False, null=False, blank=True, verbose_name="ادمین"
    )

    USER_TYPE_CHOICES = (
        (1, "customer"),
        (2, "manager"),
        (3, "branchManager"),
        (4, "branchCashier"),
        (5, "admin")
    )

    user_type = models.PositiveSmallIntegerField(
        choices=USER_TYPE_CHOICES, null=False, blank=True, 
        verbose_name="نوع کاربری"
    )

    person = models.OneToOneField(
        "Person", on_delete=models.CASCADE, null=True, blank=True, 
        verbose_name="فرد مربوطه"
    )

    objects = jmodels.JManager()

    date_joined = jmodels.jDateField(
        auto_now_add=True, editable=False,  
        null=False, blank=True, verbose_name="تاریخ ثبت"
    )

    last_login = jmodels.JDateTimeField(
        defualt=jdatetime.datetime.now, 
        null=False, blank=True, verbose_name="اخرین ورود"
    )

    USERNAME_FIELD = "username"

    Email_Field = "email"

    REQUIRED_FIELDS = [user_type]

    # relating to custom user manager
    # that is in the managers majule
    objects = managers.UserManager()

    # Is the user a member of staff?
    # Simplest possible answer: All admins are staff
    @property
    def is_staff(self):
        return self.is_admin

    def __str__(self):
        return self.username

    class Meta:
        
        verbose_name = "کاربر"

        verbose_name_plural = "کاربران"
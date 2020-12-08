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

# Define the customer user model that has several specific field
class Customer(models.Model):
    
    user = models.OneToOneField(
        "User", on_delete=models.CASCADE , primary_key=True, 
        null=False, blank=False, verbose_name="کاربری"
    )

    phone_number = models.CharField(
        db_index=True, max_length=9, null=True, blank=True, 
        validators=[
            RegexValidator(
                regex=r"^\d{9}$", 
                message="شماره تماس را به صورت صحیح وارد نمایید", 
                code="شماره تماس نادرست"
            )
        ], 
        unique=True, verbose_name="شماره تماس"
    )

    province = models.CharField(
        db_index=True, max_length=50, null=True, blank=True, 
        validators=[
            RegexValidator(
                regex=r("^[\s\u0621-\u0628\u062A-\u063A"
                "\u0641-\u0642\u0644-\u0648"
                "\u064E-\u0651\u0655\u067E\u0686\u0698"
                "\u06A9\u06AF\u06BE\u06CC]{3, 50}$"), 
                message="استان را به صورت صحیح وارد نمایید", 
                code="استان نامعتبر", 
            )
        ], 
        verbose_name="استان"
    )

    city = models.CharField(
        db_index=True, max_length=50, null=True, blank=True, 
        validators=[
            RegexValidator(
                regex=r("^[\s\u0621-\u0628\u062A-\u063A"
                "\u0641-\u0642\u0644-\u0648"
                "\u064E-\u0651\u0655\u067E\u0686\u0698"
                "\u06A9\u06AF\u06BE\u06CC]{3, 50}$"), 
                message="شهر را به صورت صحیح وارد نمایید", 
                code="شهر نامعتبر", 
            )
        ],
        verbose_name="شهر"
    )

    def __str__(self):
        return self.user.username

    class Meta:

        verbose_name = "مشتری"

        verbose_name_plural = "مشتریان"
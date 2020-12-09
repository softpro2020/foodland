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

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.email

    def has_perm(sels, perm, obj=None):
        return True

    def has_madule_perms(self, app_lable):
        return True

    def __str__(self):
        return self.username

    class Meta:

        verbose_name = "کاربر"

        verbose_name_plural = "کاربران"

# Define the customer user model that has several specific field


class Customer(models.Model):

    user = models.OneToOneField(
        "User", on_delete=models.CASCADE, primary_key=True,
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

# Define the Person model related to everybody in system


class Person(models.Model):

    first_name = models.CharField(
        db_index=True, max_length=50, null=False, blank=False,
        verbose_name="نام"
    )

    last_name = models.CharField(
        db_index=True, max_length=50, null=False, blank=False,
        verbose_name="نام خانوادگی"
    )

    national_code = models.CharField(
        db_index=True, max_length=10, null=False,
        blank=False, unique=True,
        validators=[
            RegexValidator(
                regex=r"^\d{10}$",
                message="کد ملی باید به صورت ۱۰ رقمی وارد گردد",
                code="کد ملی نادرست"
            )
        ],
        verbose_name="کد ملی"
    )

    GENDER_CHOICES = (
        ('مرد', 'man'),
        ('زن', 'woman')
    )

    gender = models.CharField(
        db_index=True, max_length=3, choices=GENDER_CHOICES,
        null=False, blank=False, verbose_name="جنسیت"
    )

    def __str__(self):
        return (self.first_name, self.last_name)

    class Meta:

        verbose_name = "فرد"

        verbose_name_plural = "افراد"

# Define a model for Food Collection
# Food Collections serve to customers


class FoodCollection(models.Model):

    full_name = models.CharField(
        db_index=True, max_length=100, null=False, blank=False,
        verbose_name="نام مجموعه"
    )

    guild_id = models.CharField(
        db_index=True, max_length=12, null=False, blank=False,
        validators=[
            RegexValidator(
                regex=r"^\d{12}$",
                message="شناسه صنفی را بصورت درست وارد نمایید",
                code="شناسه صنفی نامعتبر"
            )
        ],
        verbose_name="شناسه صنفی"
    )

    objects = jmodels.JManager()

    expiration_date = jmodels.JDateField(
        null=False, blank=False, verbose_name="تاریخ انقضا پروانه کسب"
    )

    collaborationRequest = models.OneToOneField(
        "CollaborationRequest", on_delete=models.CASCADE,
        null=False, blank=False, verbose_name="درخواست مربوطه"
    )

    manager = models.OneToOneField(
        "User", on_delete=models.CASCADE, null=False, blank=False,
        verbose_name="مدیر مجموعه"
    )

    def __str__(self):
        return self.full_name

    class Meta:

        verbose_name = "مجموعه غذایی"

        verbose_name_plural = "مجموعه های غذایی"

# Create the Collaboration Requests model
# this model is records from every request


class CollaborationRequest(models.Model):

    objects = jmodels.JManager()

    date = jmodels.JDateField(
        auto_now_add=True, editable=False,
        null=False, blank=True,
        verbose_name="تاریخ درخواست"
    )

    applicant_firstname = models.CharField(
        db_index=True, max_length=50,
        null=False, blank=False,
        verbose_name="نام متقاضی"
    )

    applicant_lastname = models.CharField(
        db_index=True, max_length=50,
        null=False, blank=False,
        verbose_name="نام خانوادگی متقاضی"
    )

    applicant_nationalcode = models.CharField(
        db_index=True, max_length=10,
        null=False, blank=False, unique=True,
        validators=[
            RegexValidator(
                regex=r"^\d{10}$",
                message="کد ملی متقاضی به صورت صحیح وارد شود",
                code="کد ملی نادرست"
            )
        ],
        verbose_name="کد ملی"
    )

    text = models.TextField(
        max_length=2000, null=True, blank=True,
        verbose_name="متن درخواست"
    )

    fc_name = models.CharField(
        db_index=True, max_length=50,
        null=False, blank=False,
        verbose_name="نام مجموعه غذایی"
    )

    guild_id = models.CharField(
        db_index=True, max_length=12, null=False, blank=False,
        validators=[
            RegexValidator(
                regex=r"^\d{12}$",
                message="شناسه صنفی را بصورت درست وارد نمایید",
                code="شناسه صنفی نامعتبر"
            )
        ],
        verbose_name="شناسه صنفی"
    )

    job_category = models.CharField(
        max_length=100, null=False, blank=False,
        verbose_name="رسته صنفی"
    )

    def __str__(self):

        return self.fc_name

    class Meta:

        verbose_name = "درخواست همکاری"

        verbose_name_plural = "درخواست های همکاری"

# Create the Branch model that every Food Collection can-
# has one or more brnches


class Branch(models.Model):

    name = models.CharField(
        db_index=True, max_length=100, null=False, blank=False,
        verbose_name="نام شعبه"
    )

    foodCollection = models.ForeignKey(
        "FoodCollection", on_delete=models.CASCADE,
        null=False, blank=False, verbose_name="مجموعه غذایی"
    )

    def __str__(self):
        return self.name

    class Meta:

        verbose_name = "شعبه"

        verbose_name_plural = "شعب"

# Create the Call Contact model
# Call Contact is for record the contacts from every branch


class CallContact(models.Model):

    branch = models.OneToOneField(
        "Branch", on_delete=models.CASCADE,
        null=False, blank=False, unique=True,
        verbose_name="شعبه مورد نظر"
    )

    phoneNumber1 = models.CharField(
        db_index=True, max_length=8, null=False, blank=False,
        validators=[
            RegexValidator(
                regex=r"^\d{8}$",
                message="شماره تماس به صورت صحیح وارد گردد",
                code="شماره تماس نامعتبر"
            )
        ],
        unique=True, verbose_name="شماره تماس ۱"
    )

    phoneNumber2 = models.CharField(
        db_index=True, max_length=8, null=True, blank=True,
        validators=[
            RegexValidator(
                regex=r"^\d{8}$",
                message="شماره تماس به صورت صحیح وارد گردد",
                code="شماره تماس نامعتبر"
            )
        ],
        unique=True, verbose_name="شماره تماس 2"
    )

    mobileNumber = models.CharField(
        db_index=True, max_length=9, null=True, blank=True,
        validators=[
            RegexValidator(
                regex=r"^\d{9}$",
                message="شماره موبایل را به صورت صحیح وارد نمایید",
                code="شماره موبایل نادرست"
            )
        ],
        unique=True, verbose_name="شماره موبایل"
    )

    def __str__(self):
        return self.branch.name

    class Meta:

        verbose_name = "اطلاعات تماس"

        verbose_name_plural = "اطلاعات تماس"

# Create the Address model
# Address model is for record the address information-
# from every branch of Food Collection


class Location(models.Model):

    branch = models.OneToOneField(
        "Branch", on_delete=models.CASCADE, null=False, blank=False,
        unique=True, verbose_name="شعبه"
    )

    province = models.OneToOneField(
        "Province", on_delete=models.CASCADE, null=False, blank=False,
        verbose_name="استان"
    )

    city = models.OneToOneField(
        "City", on_delete=models.CASCADE, null=False, blank=False,
        verbose_name="شهر"
    )

    address = models.CharField(
        db_index=True, max_length=300, null=False, blank=False,
        verbose_name="آدرس"
    )

    def __str__(self):
        return self.branch.name

    class Meta:

        verbose_name = "موقعیت مکانی"

        verbose_name_plural = "موقعیت های مکانی"

        unique_together = ["province", "city", "address"]
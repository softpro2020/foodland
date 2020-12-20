from django.contrib import admin
from . import models
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

# Register the custom User model
# it inherit from the internal creation UserAdmin model


@admin.register(models.User)
class UserAdmin(BaseUserAdmin):

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = (
        'username', 'related_person', 'lastLogin',
        'dateJoined','user_type', 'is_active'
    )

    list_filter = ('is_active', 'date_joined', 'user_type')

    fieldsets = (
        ('اطلاعات کاربری', {'fields': ('username', 'email', 'password')}),
        (None, {'fields': (
            ('user_type', 'is_active'), ('date_joined', 'last_login'),
            ('person'),
            )}),
    )

    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        ('اطلاعات کاربری', {
        'classes': ('wide','extrapretty'),
        'fields': (('username', 'user_type'), 'password1', 'password2'),
        }),
    )

    search_fields = ('username', 'person__first_name', 'person__last_name')
    ordering = ('username', 'date_joined', 'last_login')
    filter_horizontal = ()
    actions = ('activate', 'deactivate')
    date_hierarchy = 'last_login'
    readonly_fields = ('last_login', 'date_joined')

    # Define this method to return the person first_name and family_name
    def related_person(self, obj):
        if obj.person:
            return obj.person.first_name, obj.person.last_name
    related_person.short_description ='نام و نام خانوادگی'
    related_person.admin_order_field = 'person__last_name'
    related_person.empty_value_display = 'تعریف نشده'

    # Define this method to return the last_login data in a custom form
    def lastLogin(self, obj):
        return obj.last_login.strftime("%Y/%m/%d - %H:%M:%S")
    lastLogin.short_description = 'آخرین بازدید'

    # Define this method to return the date_joied data in a custom form
    def dateJoined(self, obj):
        return obj.date_joined.strftime("%Y/%m/%d")
    dateJoined.short_description = 'تاریخ ثبت نام'

    # for set an action to the change list page
    # this action is for activating the user
    def activate(self, request, queryset):
        queryset.update(is_active=True)
    activate.short_description = "فعال کردن"

    # for set an action to the change list page
    # this action is for deactivating the user
    def deactivate(self, request, queryset):
        queryset.update(is_active=False)
    deactivate.short_description = "غیر فعال کردن"

# Unregister the Group model from admin
admin.site.unregister(Group)

# Register the Customer model
# every Customer is a type of User


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):

    list_display = (
        'related_user', 'related_address', 'lastLogin', 'dateJoined'
    )

    fields = (
        ('user'),('phone_number', 'province', 'city')
    )

    list_filter = ('user__is_active', 'province__name')
    actions = ('activate', 'deactivate')

    # this method return the username of related User
    def related_user(self, obj):
        return obj.user.username

    # Define this method to return the last_login data in a custom form
    def lastLogin(self, obj):
        return obj.user.last_login.strftime("%Y/%m/%d - %H:%M:%S")

    # Define this method to return the date_joied data in a custom form
    def dateJoined(self, obj):
        return obj.user.date_joined.strftime("%Y/%m/%d")

    # return the related province name 
    def related_address(self, obj):
        return str(obj.province.name, obj.city.name)

    # for set an action to the change list page
    # this action is for activating the related user
    def activate(self, request, queryset):
        queryset.update(user__is_active=True)
    activate.short_description = "فعال کردن"

    # for set an action to the change list page
    # this action is for deactivating the related user
    def deactivate(self, request, queryset):
        queryset.update(user__is_active=False)
    deactivate.short_description = "غیر فعال کردن"

# Register the Person Model there


@admin.register(models.Person)
class PersonAdmin(admin.ModelAdmin):

    list_display = ('first_name', 'last_name', 'national_code', 'gender')
    list_filter = ('gender',)
    fields = (
        ('first_name', 'last_name'), ('national_code', 'gender')
    )

    search_fields = ('first_name', 'last_name', 'national_code')

# Define the Branch inline for show the Branches of every FoodCollection


class BranchInline(admin.StackedInline):
    model = models.Branch
    extra = 2

# Register the FoodCollection model


@admin.register(models.FoodCollection)
class FoodCollectionAdmin(admin.ModelAdmin):

    list_display = ('full_name', 'manager', 'guild_id', 'expiration_date')
    list_filter = ('expiration_date',)
    search_fields = ('full_name', 'guild_id')
    fields = (
        ('full_name', 'guild_id'),
        ('expiration_date', 'collaborationRequest'),
        ('manager'),
    )

    inlines = [
        BranchInline,
    ]

# Register the CollaborationRequest model


@admin.register(models.CollaborationRequest)
class CollaborationRequestAdmin(admin.ModelAdmin):

    list_display = ('date', 'applicant_name', 'applicant_nationalcode')
    list_filter = ('date',)
    search_fields = (
        'applicant_firstname', 'aplicant_lastname', 'guild_id'
    )

    fields = (
        ('date', 'applicant_firstname', 'applicant_lastname'),
        ('text'),
        ('fc_name', 'guild_id', 'job_category'),
    )

    readonly_fields = (
        'date', 'applicant_firstname', 'applicant_lastname',
        'text', 'fc_name', 'guild_id', 'job_category'
    )

    # this method return the applicant fullname
    def applicant_name(self, obj):
        return "{} {}".format(obj.applicant_firstname, obj.applicant_lastname)
    applicant_name.short_description = "درخواست کننده"

# Register the Branch model


@admin.register(models.Branch)
class BranchAdmin(admin.ModelAdmin):

    list_display = (
        'name', 'foodCollection', 'branchManager', 'branchCashier'
    )

    list_filter = (
        'foodCollection',
        'branchManager__user_type', 'branchCashier__user_type'
    )

    search_fields = ('name', 'foodCollection__full_name')
    fieldsets = (
        (None, {'fields':
        ('name', 'foodCollection', 'branchManager', 'branchCashier'),
        }),
    )
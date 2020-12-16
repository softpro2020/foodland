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
            ('user_type', 'is_active'), ('date_joined', 'last_login')
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

    # Define this method to return the date_joied data in a custom form
    def dateJoined(self, obj):
        return obj.date_joined.strftime("%Y/%m/%d")

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
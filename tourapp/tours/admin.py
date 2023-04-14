from django.contrib import admin
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.contrib.admin.sites import NotRegistered
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import Permission, Group
from django.core.exceptions import PermissionDenied
from django.db.models import Count, Sum
from django.db.models.functions import TruncMonth
from django.template.response import TemplateResponse
from django.utils.safestring import mark_safe
from django import forms
# from . import cloud_path
from .models import *
from django.urls import path
from datetime import date


# class AttractionsForm(forms.ModelForm):
#     description = forms.CharField(widget=CKEditorUploadingWidget)
#
#     class Meta:
#         model = Attraction
#         fields = '__all__'


class TourForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget)

    class Meta:
        model = Tour
        fields = '__all__'


class MyUserAdmin(UserAdmin):
    model = User
    search_fields = ('username', 'first_name', 'last_name')
    exclude = ('group',)
    list_display = ('pk', 'username',)
    list_display_links = ('username',)
    list_filter = ('is_staff', 'is_superuser', 'is_customer')
    readonly_fields = ('last_login', 'date_joined', 'avatar_view')

    def avatar_view(self, user):
        if (user.avatar):
            return mark_safe(
                '<img src="/{url}" width="120" />'.format(url=user.avatar.name)
            )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('avatar', 'username', 'password1', 'password2', 'email')}
         ),
    )

    form = UserChangeForm
    add_form = UserCreationForm

    try:
        admin.site.unregister(User)
    except NotRegistered:
        pass

    # fieldsets = (
    #     ('Login info', {
    #         'fields': ('avatar_view', 'avatar', 'username', 'password')
    #     }),
    #     ('Personal info', {
    #         'fields': ('first_name', 'last_name', 'gender', 'home_town', 'date_of_birth', 'email', 'phone')
    #     }),
    #     ('Customer', {
    #         'fields': (
    #             'is_customer',
    #         ),
    #         'description': '<div class="help">%s</div>' % "Designates whether this user is a customer or not",
    #     }),
    #     ('Permissions', {
    #         'fields': (
    #             'is_staff', 'is_superuser',
    #             'groups', 'user_permissions'
    #         )
    #     }),
    #     ('Other info', {
    #         'fields': ('is_active', 'last_login', 'date_joined')
    #     })
    # )


class AttractionAdmin(admin.ModelAdmin):
    search_fields = ('location',)



class TourAdmin(admin.ModelAdmin):
    model = Tour
    exclude = ('tag',)
    list_display = ('pk', 'name', 'attraction', 'image_view')
    list_display_links = ('name',)
    search_fields = ('name',)
    form = TourForm

    def image_view(self, new):
        if (new.image):
            return mark_safe(
                '<img src="/{url}" width="120" />'.format(url=new.image.name)
            )


# Register your models here.

admin.site.register(User, MyUserAdmin)
admin.site.register(Tour, TourAdmin)
admin.site.register(Attraction)
admin.site.register(Rate)
admin.site.register(Comment)

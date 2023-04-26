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


class AttractionsForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget)

    class Meta:
        model = Attraction
        fields = '__all__'


class AttractionAdmin(admin.ModelAdmin):
    search_fields = ('location',)
    list_display = ('pk', 'location', 'active')
    list_display_links = ('pk', 'location', 'active')
    # form = AttractionsForm


class TourForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget)

    class Meta:
        model = Tour
        fields = '__all__'


class TourAdmin(admin.ModelAdmin):

    list_display = ('pk', 'name', 'attraction', 'departure_date', 'end_date', 'avatar')
    list_display_links = ('name',)
    search_fields = ('name',)
    form = TourForm

    def avatar(self, new):
        if (new.image):
            return mark_safe(
                '<img src="/{url}" width="120" />'.format(url=new.image.name)
            )


class ImageTourAdmin(admin.ModelAdmin):
    list_display = ('pk', 'view_image', 'tour', 'active')
    search_fields = ('descriptions',)
    def view_image(self, obj):
        if (obj.image):
            return mark_safe(
                '<img src="/{url}" width="120" />'.format(url=obj.image.name)
            )



class BookingTourAdmin(admin.ModelAdmin):
    list_display = ('pk', 'booking_information', 'created_date', 'updated_date', 'active')
    list_display_links = ('pk', 'booking_information', 'created_date', 'updated_date', 'active')
    def booking_information(self, obj):
        return obj.__str__()


class MyUserAdmin(UserAdmin):
    model = User
    search_fields = ('username', 'first_name', 'last_name')
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


class TagAdmin(admin.ModelAdmin):
    model = Tag
    search_fields = ('name',)


# Register your models here.

admin.site.register(User, MyUserAdmin)
admin.site.register(Tour, TourAdmin)
admin.site.register(Attraction, AttractionAdmin)
admin.site.register(Rate)
admin.site.register(Comment)
admin.site.register(Tag)
admin.site.register(Bill)
admin.site.register(Like)
admin.site.register(BookTour, BookingTourAdmin)
admin.site.register(ImageTour, ImageTourAdmin)

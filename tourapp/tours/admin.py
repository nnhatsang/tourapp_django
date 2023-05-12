from django.contrib import admin
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.contrib.admin.sites import NotRegistered
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import Permission, Group

from django.utils.safestring import mark_safe
from django import forms
from . import cloud_path
from .models import *



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
    list_display = ('pk', 'name', 'attraction', 'departure_date', 'end_date', 'view_image')
    list_display_links = ('name',)
    search_fields = ('name',)
    form = TourForm

    def view_image(self, new):
        if (new.image):
            return mark_safe(
                # '<img src="http://127.0.0.1:8000/static/{url}" width="120" />'.format(url=new.image.name)
                "<img src='{cloud_path}{url}' alt='image' width='50' />".format(cloud_path=cloud_path, url=new.image)

            )


class ImageTourAdmin(admin.ModelAdmin):
    list_display = ('pk', 'view_image', 'tour', 'active')
    search_fields = ('descriptions',)

    def view_image(self, obj):
        if (obj.image):
            return mark_safe(
                # '<img src="http://127.0.0.1:8000/static/{url}" width="120" />'.format(url=obj.image.name)
                "<img src='{cloud_path}{url}' alt='image' width='50' />".format(cloud_path=cloud_path, url=obj.image)

            )


class BookingTourAdmin(admin.ModelAdmin):
    list_display = ('pk', 'booking_information', 'created_date', 'updated_date', 'active')
    list_display_links = ('pk', 'booking_information', 'created_date', 'updated_date', 'active')

    def booking_information(self, obj):
        return obj.__str__()


class MyUserAdmin(UserAdmin):
    model = User
    search_fields = ('username', 'first_name', 'last_name')
    list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'is_staff', 'last_login',
                    'avatar_view')
    list_display_links = ('username',)
    list_filter = ('is_staff', 'is_superuser', 'is_customer')
    readonly_fields = ('last_login', 'date_joined', 'avatar_view')

    def avatar_view(self, user):
        if (user.avatar):
            return mark_safe(
                # '<img src="http://127.0.0.1:8000/static/{url}" width="120" />'.format(url=user.avatar.name)
                "<img src='{cloud_path}{url}' alt='image' width='50' />".format(cloud_path=cloud_path, url=user.avatar)

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


class PermissionAdmin(admin.ModelAdmin):
    search_fields = ('name',)


class BlogAdmin(admin.ModelAdmin):
    model = Blog
    search_fields = ('title',)
    list_display = ('title', 'image_view', 'user')
    list_filter = ('user', 'created_date', 'updated_date')

    def image_view(self, new):
        if new.image:
            return mark_safe(
                # '<img src="http://127.0.0.1:8000/static/{url}" width="120" />'.format(url=new.image.name)
                "<img src='{cloud_path}{url}' alt='image' width='50' />".format(cloud_path=cloud_path, url=new.image)

            )


# Register your models here.

admin.site.register(Permission, PermissionAdmin)

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
admin.site.register(CommentBlog)
admin.site.register(LikeBlog)
admin.site.register(Blog, BlogAdmin)
admin.site.register(PaymentMethod)

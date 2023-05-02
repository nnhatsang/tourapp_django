from django.db import models
from django.contrib.auth.models import AbstractUser
from ckeditor.fields import RichTextField
from datetime import datetime


# Create your models here.
class User(AbstractUser):
    avatar = models.ImageField(null=True, upload_to='images/users/%Y/%m')
    is_customer = models.BooleanField(default=False, verbose_name='Customer status')
    home_town = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if self.avatar:
            super(AbstractUser, self).save(*args, **kwargs)
            self.avatar.name = "static/{avt_name}".format(avt_name=self.avatar.name)
            super(AbstractUser, self).save(*args, **kwargs)


class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True


# tag
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


# tour
class Tour(BaseModel):
    name = models.CharField(max_length=100, null=False, default="none")
    price_for_adults = models.FloatField(default=0)
    price_for_children = models.FloatField(default=0)
    departure_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    attraction = models.ForeignKey('Attraction', on_delete=models.PROTECT, related_name='tours', null=True)
    customers = models.ManyToManyField('User', through='BookTour', related_name='tours')
    tag = models.ManyToManyField('Tag', related_name='tours')
    description = RichTextField(null=True)
    image = models.ImageField(upload_to='images/tours/%Y/%m/', null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.image:
            super(BaseModel, self).save(*args, **kwargs)
            self.image.name = "static/{img_name}".format(img_name=self.image.name)
            super(BaseModel, self).save(*args, **kwargs)


class ImageTour(BaseModel):
    image = models.ImageField(upload_to='images/tours/%Y/%m/', null=True)
    tour = models.ForeignKey('Tour', on_delete=models.CASCADE, related_name='images', null=True)
    descriptions = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.tour


class Attraction(BaseModel):
    location = models.CharField(max_length=50, default="none")

    def __str__(self):
        return self.location


class BookTour(BaseModel):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    tour = models.ForeignKey('Tour', on_delete=models.CASCADE)
    num_of_adults = models.IntegerField(default=0)
    num_of_children = models.IntegerField(default=0)
    send_mail = models.BooleanField(default=False)

    def __str__(self):
        return " User: \"{0}\" Booking tour : \"{1}\" ".format(self.user.__str__(), self.tour.__str__())


# user like cmt rating
class Comment(BaseModel):
    tour = models.ForeignKey('Tour', on_delete=models.CASCADE, related_name='comments', null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    content = models.CharField(max_length=255, blank=True)

    class Meta:
        abstract: True

    def __str__(self):
        updated_date = self.updated_date.strftime('%d/%m/%Y, time: %H:%M:%S')
        return f"User: {self.user} - Tour: {self.tour} - Content: {self.content} on: {updated_date}"


class Like(BaseModel):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    state = models.BooleanField(default=False)
    tour = models.ForeignKey('Tour', on_delete=models.CASCADE, related_name='likes', null=True)

    def __str__(self):
        state = "liked" if self.state else "not liked"
        return f"\"{self.user}\" --- {state} Blog \"{self.tour}\""

    class Meta:
        unique_together = ('user', 'tour')


class Rate(BaseModel):
    user = models.ForeignKey('User', on_delete=models.SET_NULL, null=True)
    star_rate = models.IntegerField(default=5)
    tour = models.ForeignKey('Tour', on_delete=models.CASCADE, related_name='rate', null=True)

    def __str__(self):
        stars = "⭐" * self.star_rate
        return f"{self.user}'s rating for {self.tour}: {stars}"

    class Meta:
        unique_together = ('user', 'tour')


# bill
class Bill(BaseModel):
    book_tour = models.OneToOneField('BookTour', on_delete=models.CASCADE, primary_key=True)
    payment_state = models.BooleanField(default=False)
    total_price = models.FloatField(default=0)
    payment_method = models.ForeignKey('PaymentMethod', on_delete=models.PROTECT, null=True,
                                       default=None)

    def __str__(self):
        formatted_price = f"{self.total_price:,.0f}".replace(",", ".") + " VNĐ"
        return f"Bill for booking {self.book_tour}, total price: {formatted_price}"


##Update blogtour
class Blog(BaseModel):
    title = models.CharField(max_length=255, null=False, default="none")
    content = RichTextField()
    image = models.ImageField(null=True, upload_to='images/blogs/%Y/%m')
    user = models.ForeignKey('User', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title


class CommentBlog(BaseModel):
    blog = models.ForeignKey('Blog', on_delete=models.CASCADE, related_name='comments', null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    content = models.CharField(max_length=255, blank=True)

    def __str__(self):
        updated_date = self.updated_date.strftime('%d/%m/%Y, time: %H:%M:%S')
        return f"User: {self.user} - Tour: {self.blog} - Content: {self.content} on: {updated_date}"


class LikeBlog(BaseModel):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    state = models.BooleanField(default=False)
    blog = models.ForeignKey('Blog', on_delete=models.CASCADE, related_name='likes', null=True)

    def __str__(self):
        state = "liked" if self.state else "not liked"
        return f"\"{self.user}\" --- {state} Blog \"{self.blog}\""

    class Meta:
        unique_together = ('user', 'blog')


##method_payment
class PaymentMethod(BaseModel):
    payment_type = models.CharField(max_length=50, null=False)

    def __str__(self):
        return self.payment_type

from django.db import models
from django.contrib.auth.models import AbstractUser
from ckeditor.fields import RichTextField


# Create your models here.
class User(AbstractUser):
    avatar = models.ImageField(null=True, upload_to='images/users/%Y/%m')
    is_customer = models.BooleanField(default=False, verbose_name='Customer status')
    home_town = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.username


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
    image = models.ImageField(upload_to='image/tours/%Y/%m/', null=True)
    name = models.CharField(max_length=100, null=False, default="none")
    price_for_adults = models.FloatField(default=0)
    price_for_children = models.FloatField(default=0)
    departure_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    attraction = models.ForeignKey('Attraction', on_delete=models.PROTECT, related_name='tours', null=True)
    customers = models.ManyToManyField('User', through='BookTour', related_name='tours')
    tag = models.ManyToManyField('Tag', related_name='tours')
    description = RichTextField(null=True)

    def __str__(self):
        return self.name


class Attraction(BaseModel):
    location = models.CharField(max_length=50, default="none")
    # description = RichTextField(null=True)

    def __str__(self):
        return self.location


class BookTour(BaseModel):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    tour = models.ForeignKey('Tour', on_delete=models.CASCADE)
    num_of_adults = models.IntegerField(default=0)
    num_of_children = models.IntegerField(default=0)

    def __str__(self):
        return " \"{0}\" --- \"{1}\" ".format(self.user.__str__(), self.tour.__str__())

    class Meta:
        unique_together = ('user', 'tour')


# user like cmt rating
class Comment(BaseModel):
    tour = models.ForeignKey(Tour, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    content = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.content


class Like(BaseModel):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    state = models.BooleanField(default=False)
    tour = models.ForeignKey('Tour', on_delete=models.CASCADE, related_name='likes', null=True)

    class Meta:
        unique_together = ('user', 'tour')


class Rate(BaseModel):
    user = models.ForeignKey('User', on_delete=models.SET_NULL, null=True)
    star_rate = models.IntegerField(default=5)
    tour = models.ForeignKey('Tour', on_delete=models.CASCADE, related_name='rate', null=True)

    def __str__(self):
        return " \"{0}\" --- \"{1}\" ".format(self.user.__str__(), self.tour.__str__())

    class Meta:
        unique_together = ('user', 'tour')


# bill
class Bill(BaseModel):
    book_tour = models.OneToOneField('BookTour', on_delete=models.CASCADE, primary_key=True)
    payment_state = models.BooleanField(default=False)

    total_price = models.FloatField(default=0)

    def __str__(self):
        return "Bill --- {}".format(self.book_tour.__str__())

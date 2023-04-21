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

    # def save(self, *args, **kwargs):
    #     if self.image:
    #         super(AbstractUser, self).save(*args, **kwargs)
    #         self.image.name = "static/{avt_name}".format(avt_name=self.avatar.name)
    #         super(AbstractUser, self).save(*args, **kwargs)


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

    # def save(self, *args, **kwargs):
    #     if self.image:
    #         super(BaseModel, self).save(*args, **kwargs)
    #         self.image.name = "static/{img_name}".format(img_name=self.image.name)
    #         super(BaseModel, self).save(*args, **kwargs)


class ImageTour(BaseModel):
    image = models.ImageField(upload_to='images/tours/%Y/%m/', null=True)
    tour = models.ForeignKey('Tour', on_delete=models.SET_NULL, null=True)
    descriptions = models.CharField(max_length=255, null=True)

    class Meta:
        verbose_name = 'Image of tour'

    def __str__(self):
        return self.tour

    def save(self, *args, **kwargs):
        if self.image:
            super(BaseModel, self).save(*args, **kwargs)
            self.image.name = "static/{img_name}".format(img_name=self.image.name)
            super(BaseModel, self).save(*args, **kwargs)


class Attraction(BaseModel):
    location = models.CharField(max_length=50, default="none")

    def __str__(self):
        return self.location


class BookTour(BaseModel):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    tour = models.ForeignKey('Tour', on_delete=models.CASCADE)
    num_of_adults = models.IntegerField(default=0)
    num_of_children = models.IntegerField(default=0)

    def __str__(self):
        return " User: \"{0}\" Booking tour : \"{1}\" ".format(self.user.__str__(), self.tour.__str__())


# user like cmt rating
class Comment(BaseModel):
    tour = models.ForeignKey('Tour', on_delete=models.CASCADE, related_name='comments', null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    content = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return "User: \"{0}\" --- \"{1}\" content: \"{2}\" ".format(self.user.__str__(), self.tour.__str__(),
                                                                    self.content.__str__())


class Like(BaseModel):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    state = models.BooleanField(default=False)
    tour = models.ForeignKey('Tour', on_delete=models.CASCADE, related_name='likes', null=True)

    def __str__(self):
        return " \"{0}\" --- Like (\"{1}\") Tour \"{2}\"".format(self.user.__str__(), self.state.__str__(),
                                                                 self.tour.__str__())
    # class Meta:
    #     unique_together = ('user', 'tour')


class Rate(BaseModel):
    user = models.ForeignKey('User', on_delete=models.SET_NULL, null=True)
    star_rate = models.IntegerField(default=5)
    tour = models.ForeignKey('Tour', on_delete=models.CASCADE, related_name='rate', null=True)

    def __str__(self):
        return " User \"{0}\" Rating tour: \"{1}\" : \"{2}\" *".format(self.user.__str__(), self.tour.__str__(),
                                                                       self.star_rate.__str__())
    # class Meta:
    #     unique_together = ('user', 'tour')


# bill
class Bill(BaseModel):
    book_tour = models.OneToOneField('BookTour', on_delete=models.CASCADE, primary_key=True)
    payment_state = models.BooleanField(default=False)
    total_price = models.FloatField(default=0)

    def __str__(self):
        return "Bill --- {}".format(self.book_tour.__str__())

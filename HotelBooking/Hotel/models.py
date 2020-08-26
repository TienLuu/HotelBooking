from django.db import models

from django.contrib.auth.models import AbstractUser
from datetime import datetime, timezone
import json
from django.template.defaultfilters import slugify
import locale


class User(AbstractUser):
    avatar = models.ImageField(upload_to="user/avatar/%Y/%m/%D/")

# country category and its image path


class Country(models.Model):
    name = models.CharField(max_length=100)


def country_directory_path(instance, filename):
    return 'category/country/{0}/{0}_{2}_{1}'.format(instance.country.name, filename, datetime.now().strftime("%b-%d-%Y"))


class CountryTheme(models.Model):
    country = models.OneToOneField(
        Country, on_delete=models.CASCADE, related_name="contry_image")
    theme = models.ImageField(
        upload_to=country_directory_path)


# local category and its image path
class Local(models.Model):
    country = models.ForeignKey(
        Country, on_delete=models.CASCADE, related_name="locals")
    name = models.CharField(max_length=150)


def local_directory_path(instance, filename):
    return 'category/country/{0}/local/{1}/{1}_{3}_{2}'.format(instance.local.country.name, instance.local.name, filename, datetime.now().strftime("%b-%d-%Y"))


class LocalTheme(models.Model):
    local = models.ForeignKey(
        Local, on_delete=models.CASCADE, related_name='local_image')
    theme = models.ImageField(upload_to=local_directory_path)


class Utility(models.Model):
    name = models.CharField(max_length=50)


class Tag(models.Model):
    name = models.CharField(max_length=50)


class SuperTag(models.Model):
    name = models.CharField(max_length=50)


class Type(models.Model):
    name = models.CharField(max_length=50)
    vn_name = models.CharField(blank=True, max_length=50)


class Hotel(models.Model):
    name = models.CharField(max_length=225)
    hotel_type = models.ForeignKey(
        Type, on_delete=models.PROTECT, related_name="same_type")
    address = models.CharField(max_length=255)
    star = models.IntegerField()
    # price = models.PositiveBigIntegerField()
    utilities = models.ManyToManyField(Utility, related_name="same_utility")
    tags = models.ManyToManyField(Tag, related_name="same_tag")
    superTags = models.ManyToManyField(SuperTag, related_name="same_supertag")
    # promotes = models.ManyToManyField(Promote,  related_name="same_promote")
    # availability = models.BooleanField(default=True)

    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longtitude = models.DecimalField(max_digits=9, decimal_places=6)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(star__gte=0) & models.Q(star__lte=5),
                name="A star value is valid between 0 and 5",
            )
        ]

    def serialize(self):
        if self.hotel_images:
            pic_urls = [image.image.url for image in self.hotel_images.all()]
        else:
            pic_url = None

        ratings = [rating.serialize()
                   for rating in self.ratings.order_by("-timestamp").all()]
        rooms = [room.serialize() for room in self.rooms.all()]
        return {
            "id": self.id,
            "name": self.name,
            "hotel_type": self.hotel_type.name,
            "address": self.address,
            "star": self.star,
            "utilities": [utility.name for utility in self.utilities.all()],
            "tags": [tag.name for tag in self.tags.all()],
            "superTags": [superTag.name for superTag in self.superTags.all()],
            "images": pic_urls,
            "timestamp": self.timestamp.strftime("%b-%d-%Y, %I:%M %p"),
            "latitude": self.latitude,
            "longtitude": self.longtitude,
            "combo": self.combo.serialize(),
            "rooms": rooms,
            "ratings": ratings,
        }


def hotel_directory_path(instance, filename):
    name = instance.hotel.name
    slug = slugify(name)
    return "hotel/{0}/{0}_{2}_{1}".format(slug, filename, datetime.now().strftime("%b-%d-%Y"))


class HotelImage(models.Model):
    hotel = models.ForeignKey(
        Hotel, on_delete=models.CASCADE, default=None, related_name="hotel_images")
    image = models.ImageField(
        upload_to=hotel_directory_path, verbose_name='Image')


class Room(models.Model):
    hotel = models.ForeignKey(
        Hotel, on_delete=models.CASCADE, related_name="rooms")
    name = models.CharField(max_length=225)
    price = models.PositiveBigIntegerField()
    avaiability = models.BooleanField(default=True)

    class Meta:
        unique_together = (("hotel", "name"),)

    def serialize(self):
        locale.setlocale(locale.LC_ALL, 'de_DE.utf-8')
        price = locale.format('%d', self.price, 1)
        return {
            "id": self.id,
            "hotel_id": self.hotel.id,
            "name": self.name,
            "price": f'{price} VND',
            "avaiability": self.avaiability,
        }


class Promote(models.Model):
    name = models.CharField(max_length=50)


class Combo(models.Model):
    hotel = models.OneToOneField(
        Hotel, on_delete=models.CASCADE, related_name="combo")
    promotes = models.ManyToManyField(Promote, related_name="same_promote")
    price = models.PositiveBigIntegerField(blank=True)
    expire = models.DateTimeField(auto_now_add=False, blank=True)

    def serialize(self):
        expire = self.expire - datetime.now(timezone.utc)

        return {
            "id": self.id,
            "hotel_id": self.hotel.id,
            "promotes": [promote.name for promote in self.promotes.all()],
            "price": self.price,
            "expire": f"{expire.days} days left",
        }


class Rating(models.Model):
    user = models.ForeignKey(User, default="Anonymous",
                             on_delete=models.SET_DEFAULT, related_name="ratted_hotels")
    rating_hotel = models.ForeignKey(
        Hotel, on_delete=models.CASCADE, related_name="ratings")
    score = models.FloatField()
    comment = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(score__gte=0) & models.Q(score__lte=10),
                name="A score value is valid between 0 and 10",
            )
        ]

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.username,
            "rating_hotel_id": self.rating_hotel.id,
            "score": self.score,
            "comment": self.comment,
            "timestamp": self.timestamp.strftime("%b-%d-%Y, %I:%M %p"),
        }

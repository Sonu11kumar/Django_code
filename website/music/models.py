from __future__ import unicode_literals
from django.db import models
from django.conf import settings
#from django.contrib.auth import get_user_model
from django.urls import reverse
from django.db.models.signals import post_save


class Product(models.Model):
    name = models.CharField(max_length=120)
    price = models.IntegerField()
    image = models.ImageField(null=True, blank=True, height_field="height_field", width_field="width_field")
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)

    def __str__(self):
        if self.name is None:
            return "Product name is not present"
        return self.name


class Album (models.Model):
    artist = models.CharField(max_length=250)
    album_title = models.CharField(max_length=200)
    genre = models.CharField(max_length=1000)

    def __str__(self):
        return self.album_title + ' - ' + self.artist


class Post (models.Model):
    title = models.CharField(max_length=120)
    image = models.ImageField(
                              null=True, blank=True,
                              height_field="height_field",
                              width_field="width_field")
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("music:single", args=(self.pk,))

    class Meta:
        ordering = ["-timestamp", "-updated"]


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ebook = models.ManyToManyField(Product, blank=True)

    def __str__(self):
        if self.user.username is None:
            return "User name is null"
        return self.user.username


def post_save_profile_create(sender, instance, created, *args, **kwargs):
        if created:
            Profile.objects.get_or_create(user=instance)


post_save.connect(post_save_profile_create, sender=settings.AUTH_USER_MODEL)


class OrderItem(models.Model):
    product = models.OneToOneField(Product, on_delete=models.SET_NULL, null=True)
    is_ordered = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now=True)
    date_ordered = models.DateTimeField(null=True)

    def __str__(self):
        if self.product.name is None:
            return "ERROR-PRODUCT NAME IS NULL"
        return self.product.name

    def get_delete_url(self):
        return "/music/{}/delete".format(self.pk)


class Order(models.Model):
    ref_code = models.CharField(max_length=15)
    owner = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    is_ordered = models.BooleanField(default=False)
    items = models.ManyToManyField(OrderItem)
    date_ordered = models.DateTimeField(auto_now=True)

    def get_cart_items(self):
        return self.items.all()

    def get_cart_total(self):
        return sum([item.product.price for item in self.items.all()])

    def __str__(self):
        return '{0}-{1}'.format(self.owner, self.ref_code)


class Transaction(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    token = models.CharField(max_length=120)
    order_id = models.CharField(max_length=120)
    amount = models.DecimalField(max_digits=100, decimal_places=2)
    success = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return self.order_id

    class Meta:
        ordering = ['-timestamp']

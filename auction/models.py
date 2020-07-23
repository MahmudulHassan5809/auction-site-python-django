from django.db import models
from taggit.managers import TaggableManager
from taggit.models import Tag
from smart_selects.db_fields import GroupedForeignKey
from django.contrib.auth import get_user_model
from django.urls import reverse
# Create your models here.


class AuctionDate(models.Model):
    auction_date = models.DateField()

    class Meta:
        verbose_name = 'AuctionDate'
        verbose_name_plural = '1. AuctionDate'

    def __str__(self):
        return str(self.auction_date)


class AuctionSession(models.Model):
    auction_date = models.ForeignKey(
        AuctionDate, on_delete=models.CASCADE, related_name='auction_date_session')
    auction_start_time = models.TimeField()
    auction_end_time = models.TimeField()

    def save(self, *args, **kwargs):

        self.auction_end_time = self.auction_start_time.replace(
            hour=(self.auction_start_time.hour + 1) % 24)

        super(AuctionSession, self).save(*args, **kwargs)

    def __str__(self):
        return f"Start Time {self.auction_start_time} -- End Time {self.auction_end_time}"


class Category(models.Model):
    category_name = models.CharField(max_length=150, unique=True)

    class Meta():
        ordering = ['-id']
        verbose_name_plural = "2.Categories"

    def __str__(self):
        return self.category_name


class SubCategory(models.Model):
    category = models.ForeignKey(
        Category, related_name='subcategories', on_delete=models.CASCADE, blank=True, null=True,)
    sub_category_name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.sub_category_name

    class Meta:
        ordering = ['-id']
        verbose_name_plural = "3.SubCategory"


class Product(models.Model):
    owner = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name='user_product')
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='category_product')
    sub_category = GroupedForeignKey(
        SubCategory, "category", on_delete=models.CASCADE, related_name='subcategory_product')
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to="product")
    active = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)
    created = models.DateField(auto_now_add=True, auto_now=False)
    auction_date = models.ForeignKey(
        AuctionDate, on_delete=models.CASCADE, related_name='auction_date_product')
    auction_session = models.ForeignKey(
        AuctionSession, on_delete=models.CASCADE, related_name='auction_session_product')

    tags = TaggableManager()

    def get_absolute_url(self):
        return reverse('auction:product_list')

    class Meta:
        ordering = ['-id']
        verbose_name_plural = "4.Products"

    def __str__(self):
        return self.title

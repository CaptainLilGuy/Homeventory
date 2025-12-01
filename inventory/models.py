from django.db import models
from account.models import Household

class Unit(models.Model):
    name = models.CharField(max_length=50)     # e.g. Kilogram
    symbol = models.CharField(max_length=10)   # e.g. kg

    def __str__(self):
        return self.symbol

class Category(models.Model):
    category_name = models.CharField(max_length=100)
    household = models.ForeignKey(Household, on_delete=models.CASCADE)
    def __str__(self): return self.category_name

class Tag(models.Model):
    tag_name = models.CharField(max_length=100)
    household = models.ForeignKey(Household, on_delete=models.CASCADE)
    def __str__(self): return self.tag_name

class Inventory(models.Model):
    item_id = models.CharField(max_length=50,primary_key=True, unique=True)
    item_name = models.CharField(max_length=100)
    item_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    quantity = models.IntegerField()
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    note = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    household = models.ForeignKey(Household, on_delete=models.CASCADE)

    def __str__(self): return self.item_name

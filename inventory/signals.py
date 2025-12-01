from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Household, Category, Tag, Unit

@receiver(post_save, sender=Household)
def create_default_category_and_tags(sender, instance, created, **kwargs):
    if not created:
        return

    default_categories = [
            'Food',
            'Drinks',
            'Cleaning Supplies',
            'Bathroom Items',
            'Kitchen Items'
    ]

    default_tags = [
            "Urgent",
            "Frequently Used",
            "Bulk",
            "Fragile",
     ]
    
    default_units= [
        ('Kilogram', 'kg'),
        ('Liter', 'L'),
        ('Piece', 'pc'),
        ('Pound', 'lb'),
        ('Ounce', 'oz'),
    ]
    
    for name in default_categories:
        Category.objects.create(category_name=name, household=instance)
    
    for name in default_tags:
        Tag.objects.create(tag_name=name, household=instance)
    
    for name, symbol in default_units:
        Unit.objects.create(name=name, symbol=symbol)
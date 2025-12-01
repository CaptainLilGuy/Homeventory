from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Household, HouseholdMember

@receiver(post_save, sender=Household)
def add_owner_as_member(sender, instance, created, **kwargs):
    if not created:
        return

    HouseholdMember.objects.create(
        user=instance.owner,
        household=instance,
        role='owner'
    )
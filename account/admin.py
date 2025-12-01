from django.contrib import admin
from .models import Household, HouseholdMember

admin.site.register(Household)
admin.site.register(HouseholdMember)
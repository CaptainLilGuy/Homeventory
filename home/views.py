from django.shortcuts import redirect, render
from inventory.models import Inventory
from account.models import HouseholdMember
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.decorators import login_required


@login_required
def index(request):

    membership = HouseholdMember.objects.filter(user=request.user).first()

    if not membership:
        return render(request, 'home/no_household.html', {
            'message': "You currently don't have a household. Please create one."
        })
    
    household = membership.household

    soon_expiring = Inventory.objects.filter(
        household=household,
        expiry_date__lte=timezone.now() + timedelta(days=7)
        ).order_by('expiry_date')
    
    low_stock = Inventory.objects.filter(
        household=household,
        quantity__lte=3
        ).order_by('quantity')
    
    return render(request, 'home/index.html', {
        'soon_expiring': soon_expiring,
        'low_stock': low_stock
    })

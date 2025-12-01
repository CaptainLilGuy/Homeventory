from django.shortcuts import render
from django.db.models import Sum, F
from django.db.models.functions import TruncMonth
from inventory.models import Inventory
from account.models import HouseholdMember
from datetime import datetime
from django.contrib.auth.decorators import login_required

def get_user_household(user):
    membership = HouseholdMember.objects.filter(user=user).first()
    return membership.household if membership else None


@login_required
def dashboard(request):

    household = get_user_household(request.user)

    current_month = datetime.now().month
    current_year = datetime.now().year

    # Items created this month
    monthly_items = Inventory.objects.filter(
        household=household,
        created_at__year=current_year,
        created_at__month=current_month
    ).annotate(total=F('item_price') * F('quantity'))

    total_this_month = monthly_items.aggregate(
        total_sum=Sum('total')
    )['total_sum'] or 0

    # All household items
    all_items = Inventory.objects.filter(
        household=household
    ).annotate(total=F('item_price') * F('quantity'))

    total_all_time = all_items.aggregate(
        total_sum=Sum('total')
    )['total_sum'] or 0

    # Category Chart data
    category_spending = (
        all_items.values('category__category_name')
        .annotate(total=Sum('total'))
        .order_by('-total')
    )

    category_labels = [c['category__category_name'] for c in category_spending]
    category_totals = [float(c['total']) for c in category_spending]

    # Monthly Trend Chart data
    monthly_trend = (
        all_items
        .annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(sum=Sum('total'))
        .order_by('month')
    )

    month_labels = [m['month'].strftime('%b %Y') for m in monthly_trend]
    month_totals = [float(m['sum']) for m in monthly_trend]

    context = {
        'total_this_month': total_this_month,
        'total_all_time': total_all_time,
        'category_labels': category_labels,
        'category_totals': category_totals,
        'month_labels': month_labels,
        'month_totals': month_totals,
        'recent_items': monthly_items[:10],
    }

    return render(request, 'expense/dashboard.html', context)

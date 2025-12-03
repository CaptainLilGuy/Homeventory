from django.shortcuts import render, redirect, get_object_or_404
from .models import Inventory
from .forms import InventoryForm
from django.utils import timezone
from django.db.models import Max
from django.contrib.auth.decorators import login_required
from account.models import Household
from django.contrib import messages

def get_user_households(user):
    return Household.objects.filter(
        householdmember__user=user
    ).distinct()

@login_required
def item_list(request):
    households = get_user_households(request.user)
    household = households.first()  # Assuming user is part of at least one household

    items = Inventory.objects.filter(household=household)
    return render(request, 'inventory/item_list.html', {'items': items, 'household': household})

def generate_id(household_id, catagory_id):
    today = timezone.now().date().strftime("%Y%m%d")

    household_part = str(household_id).zfill(4)

    category_part = str(catagory_id).zfill(2)

    prefix = f"{household_part}{today}{category_part}"

    last_item = Inventory.objects.filter(item_id__startswith=prefix).aggregate(Max('item_id'))["item_id__max"]

    if last_item:
        last_sequence = int(last_item[-3:])
        new_sequence = last_sequence + 1
    else:
        new_sequence = 1
    
    sequence_part = str(new_sequence).zfill(3)

    return f"{prefix}{sequence_part}"

@login_required
def item_create(request):
    form = InventoryForm(request.POST or None)
    if form.is_valid():
        item = form.save(commit=False)

        household_id = item.household.household_id
        category_id = item.category.id

        generated_id = generate_id(household_id, category_id)

        item.item_id = generated_id

        item.save()

        form.save_m2m()
        messages.success(request, "Item created successfully!")
        return redirect('inventory_list')
    return render(request, 'inventory/item_form.html', {'form': form})

@login_required
def item_edit(request, pk):
    item = get_object_or_404(Inventory, pk=pk)
    form = InventoryForm(request.POST or None, instance=item)
    if form.is_valid():
        item = form.save(commit=False) 
        item.save()
        form.save_m2m()
        messages.info(request, "Item updated successfully!")
        return redirect('inventory_list')
    return render(request, 'inventory/item_form.html', {'form': form})

@login_required
def item_delete(request, pk):
    item = get_object_or_404(Inventory, pk=pk)
    if request.method == 'POST':
        item.delete()
        messages.warning(request, "Item deleted successfully!")
        return redirect('inventory_list')
    return render(request, 'inventory/item_confirm_delete.html', {'item': item})

@login_required
def item_detail(request, pk):
    print("DEBUG PK:", pk)
    item = get_object_or_404(Inventory, pk=pk)
    return render(request, 'inventory/item_detail.html', {'item': item})

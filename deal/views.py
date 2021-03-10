from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView
from .models import Deals, Adress, ComputeDeals, AssetTypes
from django import forms
from .forms import DealAddressForm, DealAssetTypeForm, DealComputeDealForm, DealsForm
from django.contrib.auth.decorators import login_required

def index(request):
    """
    This view is to display the landing page
    """
    return render(request, 'deal/index.html')

@login_required
def create_deal(request):
    """
    This view will present the forms the user will fill inorder to get create a deal request.
    If the forms(Adress, Asset properties, Compute Deals and Deals) are valid,the forms will be saved in their corresponding
    model classes.The class will also be added to the user so as to get deal per user 
    """
    if request.method == 'POST':
        form_deal = DealsForm(request.POST)
        form_adress = DealAddressForm(request.POST)
        form_compute = DealComputeDealForm(request.POST)
        form_asset = DealAssetTypeForm(request.POST)
        if form_adress.is_valid() and form_asset.is_valid() and form_compute.is_valid() and form_deal.is_valid():
            name = form_deal.cleaned_data['name']
            property_status = form_deal.cleaned_data['property_status']
            form_adress.save()
            form_asset.save()
            form_compute.save()
            address = Adress.objects.latest('id')
            asset = AssetTypes.objects.latest('id')
            compute = ComputeDeals.objects.latest('id')
            de = Deals.objects.create(name=name, property_status=property_status, adress=address,assets=asset,computeDeal=compute)
            request.user.Deals.add(de)
            return redirect('display')
    else:
        form_deal = DealsForm()
        form_adress = DealAddressForm()
        form_compute = DealComputeDealForm()
        form_asset = DealAssetTypeForm()
    return render(request, 'deal/deal-form.html', {'deal': form_deal,'adress':form_adress, 'compute':form_compute, 'asset':form_asset})
@login_required
def deal_diaply_on_search(request):
    """
    This view is for displaying the result of creating a deal.It presents the user with form whose intance values corresponds to what the user 
    entered as initial data. The view will also display the result of the deal created.The form can be updated 
    If the forms(Adress, Asset properties, Compute Deals and Deals) are valid,the forms will be saved in their corresponding
    model classes.The class will also be added to the user so as to get deal per user 
    """

    deal = Deals.objects.latest('id')
    address = Adress.objects.latest('id')
    asset = AssetTypes.objects.latest('id')
    compute = ComputeDeals.objects.latest('id')
    if request.method == 'POST':
        form_deal = DealsForm(request.POST, instance=deal)
        form_adress = DealAddressForm(request.POST, instance=address)
        form_compute = DealComputeDealForm(request.POST, instance=compute)
        form_asset = DealAssetTypeForm(request.POST, instance=asset)
        if form_adress.is_valid() and form_asset.is_valid() and form_compute.is_valid() and form_deal.is_valid():
            name = form_deal.cleaned_data['name']
            property_status = form_deal.cleaned_data['property_status']
            form_adress.save()
            form_asset.save()
            form_compute.save()
            address = Adress.objects.latest('id')
            asset = AssetTypes.objects.latest('id')
            compute = ComputeDeals.objects.latest('id')
            deal_update = Deals.objects.latest('id')
            #update(name=name, property_status=property_status, adress=address,assets=asset,computeDeal=compute)
            deal_update.name = name
            deal_update.property_status = property_status
            deal_update.adress = address
            deal_update.assets= asset
            deal_update.computeDeal = compute
            deal_update.save()
            deal = Deals.objects.latest('id')

    else:

        

        form_deal = DealsForm(instance = deal)
        form_adress = DealAddressForm(instance=address)
        form_compute = DealComputeDealForm(instance=compute)
        form_asset = DealAssetTypeForm(instance= asset)
        deal = Deals.objects.last()
        
    return render(request, 'deal/display.html', {'deal':deal,'deal_form': form_deal,'adress':form_adress, 'compute':form_compute, 'asset':form_asset})

@login_required
def manage_subscriptions(request):
    """
    Thie view is to display the subcriptions(saved deals) a user has made
    """
    
    #deal = Deals.objects.all()
    return render(request, 'deal/subscriptions.html')

@login_required      
def edit(request, pk):
    """
    Edit view is to saved deal. The user is presented with a form with instance values corresponding to the data 
    the user saved. The user can edit the form and save. The page will be redirected to the page to view saved subscriptions upon save
    """
    deal = Deals.objects.get(pk = pk)
    if request.method == 'POST':
        deal_form = DealsForm(request.POST, instance = deal)
        if deal_form.is_valid():
            deal_form.save()
            return redirect('subscriptions')
    else:
        deal_form = DealsForm( instance=deal)
    return render(request, 'deal/edit.html', {'edit_form':deal_form, 'deal':deal})

@login_required   
def delete(request, pk):
    """
    delete view is to saved deal. The user is presented to delete page upon request. 
    The deal is deleted upon confirmtion. The page will be redirected to the page to view saved subscriptions upon delete
    """

    deal = Deals.objects.get(pk = pk) 
    if request.method =='POST':
        deal.delete()
        return redirect('subscriptions')
    return render(request, 'deal/delete.html', {'deal':deal})

@login_required
def deal_diaplay_specific_search_id(request, pk):
    """
    This view is to view a saved deal.It presents the user with form whose intance values corresponds to what the user 
    entered as initial data. The view will also display the result of the deal created.The form can be updated 
    If the forms(Adress, Asset properties, Compute Deals and Deals) are valid,the forms will be saved in their corresponding
    model classes.The class will also be added to the user so as to get deal per user 
    """

    deal = Deals.objects.get(pk = pk) 
    address = Adress.objects.get(pk = pk) 
    asset = AssetTypes.objects.get(pk = pk) 
    compute = ComputeDeals.objects.get(pk = pk) 
    if request.method == 'POST':
        form_deal = DealsForm(request.POST, instance=deal)
        form_adress = DealAddressForm(request.POST, instance=address)
        form_compute = DealComputeDealForm(request.POST, instance=compute)
        form_asset = DealAssetTypeForm(request.POST, instance=asset)
        if form_adress.is_valid() and form_asset.is_valid() and form_compute.is_valid() and form_deal.is_valid():
            name = form_deal.cleaned_data['name']
            property_status = form_deal.cleaned_data['property_status']
            form_adress.save()
            form_asset.save()
            form_compute.save()
            address = Adress.objects.get(pk = pk) 
            asset = AssetTypes.objects.get(pk = pk) 
            compute = ComputeDeals.objects.get(pk = pk) 
            Deals.objects.filter(pk=pk).update(name=name, property_status=property_status, adress=address,assets=asset,computeDeal=compute)
            deal = Deals.objects.get(pk = pk) 

    else:

        

        form_deal = DealsForm(instance = deal)
        form_adress = DealAddressForm(instance=address)
        form_compute = DealComputeDealForm(instance=compute)
        form_asset = DealAssetTypeForm(instance= asset)
        deal = Deals.objects.get(pk = pk) 
        
    return render(request, 'deal/display_specific.html', {'deal':deal,'deal_form': form_deal,'adress':form_adress, 'compute':form_compute, 'asset':form_asset})

    




from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView
from .models import Deals, Adress, ComputeDeals, AssetTypes
from django import forms
from .forms import DealAddressForm, DealAssetTypeForm, DealComputeDealForm, DealsForm
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request, 'deal/index.html')

@login_required
def create_deal(request):
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
            address = Adress.objects.all().last()
            asset = AssetTypes.objects.all().last()
            compute = ComputeDeals.objects.all().last()
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

    deal = Deals.objects.all().last()
    address = Adress.objects.all().last()
    asset = AssetTypes.objects.all().last()
    compute = ComputeDeals.objects.all().last()
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
            address = Adress.objects.all().last()
            asset = AssetTypes.objects.all().last()
            compute = ComputeDeals.objects.all().last()
            Deals.objects.filter(pk=-1).update(name=name, property_status=property_status, adress=address,assets=asset,computeDeal=compute)
            deal = Deals.objects.last()

    else:

        

        form_deal = DealsForm(instance = deal)
        form_adress = DealAddressForm(instance=address)
        form_compute = DealComputeDealForm(instance=compute)
        form_asset = DealAssetTypeForm(instance= asset)
        deal = Deals.objects.last()
        
    return render(request, 'deal/display.html', {'deal':deal,'deal_form': form_deal,'adress':form_adress, 'compute':form_compute, 'asset':form_asset})

#@login_required
def manage_subscriptions(request):
    
    #deal = Deals.objects.all()
    return render(request, 'deal/subscriptions.html')
        
def edit(request, pk):
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

    deal = Deals.objects.get(pk = pk) 
    if request.method =='POST':
        deal.delete()
        return redirect('subscriptions')
    return render(request, 'deal/delete.html', {'deal':deal})

@login_required
def deal_diaplay_specific_search_id(request, pk):

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

    

class DealListView(ListView):
    queryset = Deals.objects.all().last()
    context_object_name = "Deals"
    template_name = "deal/deals.html"

class SubscriptionsView(ListView):
    queryset = Deals.objects.all()
    context_object_name = "Deals"
    template_name = "deal/subscriptions.html"


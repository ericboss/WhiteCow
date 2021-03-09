from django.urls import path
from . import views
#from .views import DealListView, SubscriptionsView

urlpatterns = [
    path('', views.index, name= 'index'),
    #path('deals/', DealListView.as_view(), name = 'deals'),
    path('deals/subscriptions', views.manage_subscriptions, name = 'subscriptions'),
    path('deals/display', views.deal_diaply_on_search, name = 'display'),
    path('deals/new', views.create_deal, name = 'deals-new'),
     path('deals/edit/<int:pk>/', views.edit, name = 'edit'),
     path('deals/delete/<int:pk>/', views.delete, name = 'delete'),
     path('deals/deal/<int:pk>/', views.deal_diaplay_specific_search_id, name = 'display_specific'),

   

]
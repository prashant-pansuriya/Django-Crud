from django.urls import path
from . import views

urlpatterns = [
   path('', views.home, name = "Home"),
   path('home/', views.home, name = "Home"),
   path('report/', views.GenerateReport.as_view(), name = "Report"),
   path('customer/list/', views.CustomerListView.as_view(), name = "customer"),
   path('customer/create/', views.CustomerCreateView.as_view(), name = "customer-create"),
   path('customer/update/<int:pk>', views.CustomerUpdateView.as_view(), name="customer-update"),
   path('customer/delete/<int:pk>', views.CustomerDeleteView.as_view(), name="customer-delete"),
   path('graph/', views.graph, name = "Graph"),
]
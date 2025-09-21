from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'clients', views.ClientViewSet, basename='client')
router.register(r'products', views.ProductViewSet, basename='product')
router.register(r'invoices', views.InvoiceViewSet, basename='invoice')
router.register(r'payments', views.PaymentViewSet, basename='payment')

urlpatterns = [
    path('', views.BillingView.as_view(), name='billing_view'),
    path('activity-logs/', views.ActivityLogAPIView.as_view(), name='activity_log_view'),
]
urlpatterns += router.urls

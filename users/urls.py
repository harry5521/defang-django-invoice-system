from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    # Auth Urls
    path('login/', TokenObtainPairView.as_view(), name='login_view'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', views.RegisterApiView.as_view(), name='register_view'),
    path('logout/', views.LogoutApiView.as_view(), name='logout_view'),

]

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from shop import views as shop_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('shop.urls')),
    path('accounts/login/', shop_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', shop_views.LogoutView.as_view(), name='logout'),
    path('register/', shop_views.register, name='register'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

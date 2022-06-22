from django.urls import path
from .views import StartPage, RegisterUser, CompanyPage, CompanyFinAnPage, DeleteCompany
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', StartPage.as_view(), name='start'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('<str:user>/<str:company>', CompanyPage.as_view(), name='company'),
    path('<str:user>/<str:company>/analist', CompanyFinAnPage.as_view(), name='finance'),
    path('delete/<str:user>/<str:company>', DeleteCompany.as_view(), name='delete-company')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

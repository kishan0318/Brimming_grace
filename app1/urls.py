from django.urls import path
# from rest_framework_simplejwt import views as jwt_views
from app1.views import *

urlpatterns = [
    
    path('Login',Login.as_view()),
    path('create',StudentsCRUD.as_view()),
    path('getAll',StudentsCRUD.as_view()),
    path('UpDel/<int:pk>',StudentsCRUD.as_view()),
    # path('delete/<int:pk>',StudentsCRUD.as_view())

    
] 
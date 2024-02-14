"""
URL configuration for movie_collection project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from movie_api.views import movie_list, register_user, login_user, create_collection, get_collections, retrieve_collection, update_collection, delete_collection, request_count, reset_request_count

urlpatterns = [
    path('admin/', admin.site.urls),
    path('movies/', movie_list, name='movie_list'),
    path('register/', register_user, name='register_user'),
    path('login/', login_user, name='login_user'),
    path('collection/', create_collection, name='collection-list'),
    path('collections/', get_collections, name='get_collections'),
    path('collection/<str:collection_uuid>/', retrieve_collection, name='retrieve_collection'),
    path('collection/<str:collection_uuid>/update/', update_collection, name='update_collection'),
    path('collection/<str:collection_uuid>/delete/', delete_collection, name='delete_collection'),
    path('request-count/', request_count, name='request_count'),
    path('request-count/reset/', reset_request_count, name='reset_request_count'),
]

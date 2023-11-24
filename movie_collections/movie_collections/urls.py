"""
URL configuration for movie_collections project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from movies import views as movie_views
from accounts import views as account_views
from middleware_tasks import views as middleware_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('movies/', movie_views.MovieList.as_view(), name='movie-list'),
    path('register/', account_views.Register.as_view(), name='register'),
    path('collection/', movie_views.MovieCollection.as_view(), name='collection'),
    path('collection/<str:uuid>/', movie_views.UpdateDeleteMovieCollection.as_view(), name='update-delete-collection'),
    path('request-count/', middleware_views.RequestCount.as_view(), name='request-count'),
    path('request-count/reset/', middleware_views.RequestCountReset.as_view(), name='request-count-reset'),
]

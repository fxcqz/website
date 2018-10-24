from django.contrib.auth import views as auth_views
from django.urls import include, path
from . import views
from .constants import CONFIG


urlpatterns = [
	path('', views.front_page, name='front_page'),
	path('post/<slug:post>/', views.view_post, name='view_post'),
	path('accounts/', include('django.contrib.auth.urls')),
	path('accounts/profile/', views.profile, name='profile'),
	path('accounts/add/items/', views.add_items, name='add_items'),
	path('accounts/edit/items/<slug:section>/', views.add_items, name='add_items'),
]

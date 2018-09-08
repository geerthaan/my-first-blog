from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    url(r'^$', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    # name is used to generate an url in html template, e.g.
    # <a href="{% url 'post_new' %}" class="top-menu">new post </a>
    # will generate 127.0.0.0.1/8000/post/new/
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
]

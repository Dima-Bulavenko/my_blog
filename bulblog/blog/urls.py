from django.urls import path
from django.views.decorators.cache import cache_page

from .views import *


urlpatterns = [
    path('', IndexViews.as_view(), name='index'),
    path('post/<slug:post_slug>/', ShowPostView.as_view(), name='post'),
    path('cat/', cache_page(60)(ShowCatView.as_view()), name="cat"),
    path("add-post/", AddPostViews.as_view(), name="add_post"),
    path("cat/<slug:cat_slug>/", ShowPostsByCat.as_view(), name="show_posts_by_cat"),
    path("register/", RegisterUser.as_view(), name="register"),
    path("login/", LoginUser.as_view(), name="login"),
    path("logout/", logout_user, name="logout"),
]

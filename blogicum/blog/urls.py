from django.urls import path
from django.conf.urls.static import static
from . import views
from django.conf import settings


app_name = "blog"
urlpatterns = [
    path("", views.index, name="index"),
    path("posts/<int:post_id>/", views.post_detail, name="post_detail"),
    path("category/<slug:category_slug>/", views.category_posts, name="category_posts"),
    path("post/create/", views.create_post, name="create_post"),
    path("profile/<str:username>/", views.profile, name="profile"),
    path(
        "posts/<int:pk>/comment/",
        views.add_comment,
        name="add_comment",
    ),
     path(
        "posts/<int:pk>/delete/",
        views.post_delete,
        name="delete_post",
    ),
     path(
        "posts/<int:pk>/edit",
        views.post_detail,
        name="edit_post",
    ),
     
      path(
        "posts/<int:pk>/comment/delete/<int:comment_pk>/",
        views.comment_delete,
        name="delete_comment",
    ),
     path(
        "posts/<int:pk>/edit_comment/<int:comment_pk>/",
        views.comment,
        name="edit_comment",
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

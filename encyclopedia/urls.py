from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    # adds a new entry
    path("add_article/", views.add_article, name="add"),
    # search article
    path("search", views.search_article, name="search"),
    # directs user to desired article.
    path("wiki/<str:article>", views.article, name="article"),
    # edit article
    path("wiki/<str:article>/edit", views.edit_article, name="edit"),
    # get a random article
    path("random_article", views.random_article, name="random"),

]

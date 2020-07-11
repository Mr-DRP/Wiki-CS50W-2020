from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>", views.content, name="content"),
    path("create", views.create,name="create"),
    path("random", views.random, name="random"),
    path("edit/<str:title>",views.edit, name="edit"),
    path("edit/<str:title>/save",views.editsave, name="editsave")
]

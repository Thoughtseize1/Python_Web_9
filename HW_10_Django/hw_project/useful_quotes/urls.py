from django.contrib import admin
from django.urls import path
from . import views

app_name = "useful_quotes"
urlpatterns = [
    path("", views.main, name="root"),
    path("<int:page>", views.main, name="root_paginate"),
    path("author/<str:author>", views.author_page, name="author"),
    path("new_quote/", views.create_quote, name="create_quote"),
    path("new_author/", views.create_author, name="create_author"),

]

from django.urls import path
from . import views

urlpatterns=[
    path("api_all_category/", views.api_all_category, name="api_all_category"),
    path('api_add_category/', views.api_add_category, name='api_add_category'),
    # path("edit/<int:pk>/", views.api_update_stream, name="edit_stream"),
    # path("delete/<int:stream_id>/", views.api_delete_stream, name="delete_stream"),
]
from django.urls import path

from . import views

urlpatterns = [
    path("", views.ProductoList.as_view(), name="producto_list"),
    path("nuevo/", views.ProductoCreate.as_view(), name="producto_create"),
    path("<int:pk>/", views.ProductoDetail.as_view(), name="producto_detail"),
    path("<int:pk>/editar/", views.ProductoUpdate.as_view(), name="producto_update"),
    path("<int:pk>/eliminar/", views.ProductoDelete.as_view(), name="producto_delete"),
]

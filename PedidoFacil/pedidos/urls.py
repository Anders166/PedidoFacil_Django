from django.urls import path

from . import views

urlpatterns = [
    path("", views.PedidoList.as_view(), name="pedido_list"),
    path("nuevo/", views.PedidoCreate.as_view(), name="pedido_create"),
    path("<int:pk>/", views.PedidoDetail.as_view(), name="pedido_detail"),
    path("<int:pk>/editar/", views.PedidoUpdate.as_view(), name="pedido_update"),
    path("<int:pk>/eliminar/", views.PedidoDelete.as_view(), name="pedido_delete"),
    path("<int:pk>/estado/", views.PedidoCambiarEstado.as_view(), name="pedido_estado"),
]

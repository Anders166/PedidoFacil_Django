from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import ProductoForm
from .models import Producto


class ProductoList(LoginRequiredMixin, ListView):
    model = Producto
    template_name = "productos/lista.html"
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get("q", "").strip()
        return qs.filter(nombre__icontains=q) if q else qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["q"] = self.request.GET.get("q", "")
        return ctx


class ProductoDetail(LoginRequiredMixin, DetailView):
    model = Producto
    template_name = "productos/detalle.html"


class ProductoCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = "productos/form.html"
    success_url = reverse_lazy("producto_list")
    success_message = "Producto creado correctamente."


class ProductoUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Producto
    form_class = ProductoForm
    template_name = "productos/form.html"
    success_url = reverse_lazy("producto_list")
    success_message = "Producto actualizado correctamente."


class ProductoDelete(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Producto
    template_name = "productos/confirmar_eliminar.html"
    success_url = reverse_lazy("producto_list")
    success_message = "Producto eliminado correctamente."

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import EstadoForm, PedidoForm
from .models import Pedido


class PedidoList(LoginRequiredMixin, ListView):
    model = Pedido
    template_name = "pedidos/lista.html"
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset().select_related("usuario")
        q = self.request.GET.get("q", "").strip()
        return qs.filter(cliente__icontains=q) if q else qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["q"] = self.request.GET.get("q", "")
        return ctx


class PedidoDetail(LoginRequiredMixin, DetailView):
    model = Pedido
    template_name = "pedidos/detalle.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["estado_form"] = EstadoForm(initial={"estado": self.object.estado})
        return ctx


class PedidoCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Pedido
    form_class = PedidoForm
    template_name = "pedidos/form.html"
    success_url = reverse_lazy("pedido_list")
    success_message = "Pedido registrado correctamente."

    def form_valid(self, form):
        form.instance.usuario = self.request.user  # el usuario autenticado queda asociado
        return super().form_valid(form)


class PedidoUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Pedido
    form_class = PedidoForm
    template_name = "pedidos/form.html"
    success_url = reverse_lazy("pedido_list")
    success_message = "Pedido actualizado correctamente."


class PedidoDelete(LoginRequiredMixin, DeleteView):
    model = Pedido
    template_name = "pedidos/confirmar_eliminar.html"
    success_url = reverse_lazy("pedido_list")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            pedido = self.get_object()
            if not pedido.se_puede_eliminar:
                messages.error(request, "No se puede eliminar un pedido confirmado. Cancélalo primero.")
                return redirect("pedido_detail", pk=pedido.pk)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, "Pedido eliminado correctamente.")
        return super().form_valid(form)


class PedidoCambiarEstado(LoginRequiredMixin, View):
    http_method_names = ["post"]

    def post(self, request, pk):
        pedido = get_object_or_404(Pedido, pk=pk)
        form = EstadoForm(request.POST)
        if form.is_valid():
            pedido.estado = form.cleaned_data["estado"]
            pedido.save(update_fields=["estado"])
            messages.success(request, f"Estado cambiado a «{pedido.get_estado_display()}».")
        else:
            messages.error(request, "Estado no válido.")
        return redirect("pedido_detail", pk=pk)

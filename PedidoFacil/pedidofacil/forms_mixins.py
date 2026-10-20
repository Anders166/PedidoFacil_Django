from django import forms


class BootstrapFormMixin:
    """Agrega clases de Bootstrap a los campos y marca en rojo los que tienen error del servidor."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            clase = "form-select" if isinstance(field.widget, forms.Select) else "form-control"
            field.widget.attrs["class"] = clase
            if self.is_bound and name in self.errors:
                field.widget.attrs["class"] += " is-invalid"

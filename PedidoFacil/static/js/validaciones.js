/* Validaciones del lado del cliente para los formularios de productos y pedidos.
   Las validaciones reales siguen estando en Django (forms.py y models.py). */
document.addEventListener("DOMContentLoaded", () => {
  const ESTADOS = ["pendiente", "confirmado", "cancelado"];
  const esNumero = v => v.trim() !== "" && !isNaN(v);

  const REGLAS = {
    "form-producto": {
      nombre: v => v.trim().length >= 3 || (v.trim() === "" ? "El nombre es obligatorio." : "El nombre debe tener al menos 3 caracteres."),
      precio: v => (esNumero(v) && parseFloat(v) > 0) || "El precio debe ser un número mayor que cero.",
      cantidad_disponible: v => /^\d+$/.test(v.trim()) || "La cantidad debe ser un número entero igual o mayor que cero.",
      descripcion: (v, el) => v.length <= (el.maxLength > 0 ? el.maxLength : 500) || `La descripción no puede superar ${el.maxLength} caracteres.`,
    },
    "form-pedido": {
      numero_pedido: v => v.trim() !== "" || "El número del pedido es obligatorio.",
      cliente: v => v.trim() !== "" || "El nombre del cliente es obligatorio.",
      descripcion: v => v.trim() !== "" || "La descripción del pedido es obligatoria.",
      valor_total: v => (esNumero(v) && parseFloat(v) > 0) || "El valor total debe ser un número mayor que cero.",
      estado: v => ESTADOS.includes(v) || "Seleccione un estado válido.",
    },
  };

  const form = Object.keys(REGLAS).map(id => document.getElementById(id)).find(Boolean);
  if (!form) return;
  const reglas = REGLAS[form.id];

  function validar(nombre) {
    const input = form.elements[nombre];
    const resultado = reglas[nombre](input.value, input);
    const ok = resultado === true;

    input.classList.toggle("is-invalid", !ok);
    input.classList.toggle("is-valid", ok);

    // Si el usuario corrige el campo, desaparece el error que vino del servidor.
    input.parentElement.querySelectorAll(".server-error").forEach(e => e.remove());

    let fb = input.parentElement.querySelector(".js-feedback");
    if (!fb) {
      fb = document.createElement("div");
      fb.className = "invalid-feedback js-feedback";
      input.parentElement.appendChild(fb);
    }
    fb.textContent = ok ? "" : resultado;
    return ok;
  }

  Object.keys(reglas).forEach(nombre => {
    const input = form.elements[nombre];
    input.addEventListener("input", () => validar(nombre));   // vuelve a validar al corregir
    input.addEventListener("change", () => validar(nombre));
  });

  form.addEventListener("submit", e => {
    const resultados = Object.keys(reglas).map(validar);       // muestra todos los errores a la vez
    if (!resultados.every(Boolean)) {
      e.preventDefault();
      form.querySelector(".is-invalid")?.focus();
    }
  });
});

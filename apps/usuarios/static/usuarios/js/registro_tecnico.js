/* ===========================
            Animaciones
   =========================== */
document.addEventListener("DOMContentLoaded", () => {
  const form = document.querySelector(".form-container");
  if (form) {
    setTimeout(() => {
      form.classList.add("show");
    }, 200);
  }

  const messages = document.querySelectorAll(".messages div");
  messages.forEach((msg, index) => {
    msg.style.animationDelay = `${index * 0.2}s`;
  });

  // Partículas
  const canvas = document.getElementById("particles");
  const ctx = canvas.getContext("2d");
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;

  const particlesArray = [];
  const numParticles = 60; // cantidad de partículas

  class Particle {
    constructor() {
      this.x = Math.random() * canvas.width;
      this.y = Math.random() * canvas.height;
      this.size = Math.random() * 3 + 1;
      this.speedX = Math.random() * 1 - 0.5;
      this.speedY = Math.random() * 1 - 0.5;
    }
    update() {
      this.x += this.speedX;
      this.y += this.speedY;

      // Rebote
      if (this.x < 0 || this.x > canvas.width) this.speedX *= -1;
      if (this.y < 0 || this.y > canvas.height) this.speedY *= -1;
    }
    draw() {
      ctx.fillStyle = "rgba(255, 255, 255, 0.8)";
      ctx.beginPath();
      ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
      ctx.fill();
    }
  }

  function init() {
    for (let i = 0; i < numParticles; i++) {
      particlesArray.push(new Particle());
    }
  }

  function animate() {
    ctx.clearRect(0, 0, canvas.width, canvas.height); // limpia pero deja transparente
    particlesArray.forEach(p => {
        p.update();
        p.draw();
    });
    requestAnimationFrame(animate);
  }


  init();
  animate();

  window.addEventListener("resize", () => {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
  });
});
/* ===========================
        Validaciones
   =========================== */
document.addEventListener("DOMContentLoaded", () => {

  // Función para mostrar error
  function showError(input, message) {
    let errorEl = input.nextElementSibling;
    if (!errorEl || !errorEl.classList.contains("error-message")) {
      errorEl = document.createElement("div");
      errorEl.classList.add("error-message");
      errorEl.style.color = "red";
      errorEl.style.fontSize = "0.85em";
      input.parentNode.insertBefore(errorEl, input.nextSibling);
    }
    errorEl.textContent = "❌ " + message;
  }

  function clearError(input) {
    const errorEl = input.nextElementSibling;
    if (errorEl && errorEl.classList.contains("error-message")) {
      errorEl.remove();
    }
  }

  // Conversión de números a romanos (1-10)
  function numberToRoman(num) {
    const romanMap = {1:"I",2:"II",3:"III",4:"IV",5:"V",6:"VI",7:"VII",8:"VIII",9:"IX",10:"X"};
    return romanMap[num] || num;
  }

  // Validación nombres/apellidos (máx palabras)
  function validateName(input, maxWords) {
    const val = input.value.trim();

    if (/^\s|\s$/.test(val)) {
      showError(input, "No se permiten espacios al inicio o al final");
      return false;
    }

    const words = val.split(/\s+/);

    if (words.length > maxWords) {
      showError(input, `Máximo ${maxWords} palabras`);
      return false;
    }

    for (let w of words) {
      if (w.length < 3) {
        showError(input, "Cada palabra debe tener al menos 3 letras");
        return false;
      }
      if (/[^A-Za-zÀ-ÿ]/.test(w)) {
        if (/^[1-9]$|10/.test(w)) {
          input.value = input.value.replace(w, numberToRoman(parseInt(w)));
        } else {
          showError(input, "Solo letras, sin números ni símbolos");
          return false;
        }
      }
    }

    clearError(input);
    return true;
  }

  // Validación CI
  function validateCI(input) {
    let val = input.value.trim();
    input.value = val.replace(/\D/g, ""); // elimina no numérico
    if (!/^\d{7,8}$/.test(input.value)) {
      showError(input, "CI debe tener 7 u 8 dígitos");
      return false;
    }
    clearError(input);
    return true;
  }

// Validación fecha nacimiento en tiempo real (para estudiante técnico)
function validateBirthDate(input) {
  const today = new Date();
  const val = new Date(input.value);

  if (isNaN(val.getTime())) {
    showError(input, "❌ Fecha inválida");
    return false;
  }

  // Edad mínima 18 y máxima 90
  const maxDate = new Date(today.getFullYear() - 18, today.getMonth(), today.getDate());
  const minDate = new Date(today.getFullYear() - 90, today.getMonth(), today.getDate());

  if (val < minDate || val > maxDate) {
    showError(
      input,
      `❌ La fecha debe estar entre ${minDate.toLocaleDateString()} y ${maxDate.toLocaleDateString()}`
    );
    return false;
  }

  clearError(input);
  return true;
}


  // Validación teléfono Bolivia
  function validatePhone(input) {
    let val = input.value.trim();
    input.value = val.replace(/\D/g, ""); // solo números
    if (!/^(6\d{7}|7\d{7}|2\d{6})$/.test(input.value) && val !== "") {
      showError(input, "Número inválido (solo Bolivia)");
      return false;
    }
    clearError(input);
    return true;
  }

  // Dirección, Universidad, Ocupación (texto libre, solo limpiar)
  function validateAddress(input) {
    input.value = input.value.trim();
    clearError(input);
    return true;
  }

  // Validación usuario
  function validateUser(input) {
    let val = input.value.trim();
    input.value = val;
    if (!/^[A-Za-z0-9_]+$/.test(val)) {
      showError(input, "Solo letras, números y _");
      return false;
    }
    clearError(input);
    return true;
  }

  // Validación contraseña
  function validatePassword(input) {
    let val = input.value.trim();
    input.value = val;
    if (val.length < 8) {
      showError(input, "Mínimo 8 caracteres");
      return false;
    }
    if (!/[A-Z]/.test(val) || !/[a-z]/.test(val) || !/[0-9]/.test(val) || !/[^A-Za-z0-9]/.test(val)) {
      showError(input, "Debe tener mayúscula, minúscula, número y símbolo");
      return false;
    }
    clearError(input);
    return true;
  }

  // Confirmación contraseña
  function validatePassword2(input, originalInput) {
    if (input.value !== originalInput.value) {
      showError(input, "Las contraseñas no coinciden");
      return false;
    }
    clearError(input);
    return true;
  }

  // === Elementos del formulario ===
  const estNombres = document.getElementById("est-nombres");
  const estApellidos = document.getElementById("est-apellidos");
  const estCI = document.getElementById("est-ci");
  const estFecha = document.getElementById("est-fecha_nacimiento");
  const estDireccion = document.getElementById("est-direccion");
  const estTelefono = document.getElementById("est-telefono");
  const estColegio = document.getElementById("est-colegio_universidad");
  const estOcupacion = document.getElementById("est-ocupacion");

  const usuario = document.getElementById("cuenta-nombre_usuario");
  const contrasena = document.getElementById("cuenta-contrasena");
  const contrasena2 = document.getElementById("cuenta-contrasena2");

  // === Validaciones en tiempo real ===
  estNombres.addEventListener("input", () => validateName(estNombres, 3));
  estApellidos.addEventListener("input", () => validateName(estApellidos, 2));
  estCI.addEventListener("input", () => validateCI(estCI));
  estFecha.addEventListener("blur", () => validateBirthDate(estFecha));
  estDireccion.addEventListener("input", () => validateAddress(estDireccion));
  estTelefono.addEventListener("input", () => validatePhone(estTelefono));
  estColegio.addEventListener("input", () => validateAddress(estColegio));
  estOcupacion.addEventListener("input", () => validateAddress(estOcupacion));

  usuario.addEventListener("input", () => validateUser(usuario));
  contrasena.addEventListener("input", () => validatePassword(contrasena));
  contrasena2.addEventListener("input", () => validatePassword2(contrasena2, contrasena));

  // Validación final al enviar
  const form = document.querySelector("form");
  form.addEventListener("submit", (e) => {
    let valid = true;
    valid &= validateName(estNombres, 3);
    valid &= validateName(estApellidos, 2);
    valid &= validateCI(estCI);
    valid &= validateBirthDate(estFecha);
    valid &= validateAddress(estDireccion);
    valid &= validatePhone(estTelefono);
    valid &= validateAddress(estColegio);
    valid &= validateAddress(estOcupacion);

    valid &= validateUser(usuario);
    valid &= validatePassword(contrasena);
    valid &= validatePassword2(contrasena2, contrasena);

    if (!valid) e.preventDefault();
  });
});

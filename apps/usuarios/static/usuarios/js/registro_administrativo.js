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
  // === FUNCIONES DE ERROR ===
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

  // === VALIDACIONES ===
  function validateName(input, maxWords) {
    const val = input.value.trim();
    if (/^\s|\s$/.test(val)) {
      showError(input, "No se permiten espacios al inicio ni al final");
      return false;
    }
    const words = val.split(/\s+/);
    if (words.length > maxWords) {
      showError(input, `Solo se permiten máximo ${maxWords} palabras`);
      return false;
    }
    for (let w of words) {
      if (w.length < 3) {
        showError(input, "Cada palabra debe tener al menos 3 letras");
        return false;
      }
      if (/[^A-Za-zÀ-ÿ]/.test(w)) {
        showError(input, "No se permiten números ni caracteres especiales");
        return false;
      }
    }
    clearError(input);
    return true;
  }

  function validateLastName(input) {
    return validateName(input, 2);
  }

  function validateCI(input) {
    let val = input.value.trim();
    input.value = val.replace(/\s+/g, "");
    if (!/^\d{7,8}$/.test(input.value)) {
      showError(input, "CI debe tener 7 u 8 dígitos y solo números");
      return false;
    }
    clearError(input);
    return true;
  }

  function validatePhone(input) {
    let val = input.value.trim();
    input.value = val.replace(/\s+/g, "");
    if (!/^(6\d{7}|7\d{7}|2\d{6})$/.test(input.value) && val !== "") {
      showError(input, "Número de teléfono inválido (solo Bolivia)");
      return false;
    }
    clearError(input);
    return true;
  }

  function validateAddress(input) {
    let val = input.value.trim();
    input.value = val;
    if (val.length < 5) {
      showError(input, "La dirección debe tener mínimo 5 caracteres");
      return false;
    }
    clearError(input);
    return true;
  }

  function validateUser(input) {
    let val = input.value.trim();
    input.value = val;
    if (!/^[A-Za-z0-9_]+$/.test(val)) {
      showError(input, "Solo letras, números y _ permitidos");
      return false;
    }
    clearError(input);
    return true;
  }

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

  function validatePassword2(input, originalInput) {
    if (input.value !== originalInput.value) {
      showError(input, "Las contraseñas no coinciden");
      return false;
    }
    clearError(input);
    return true;
  }

  function validateBirthDate(input) {
    const today = new Date();
    const val = new Date(input.value);
    if (isNaN(val.getTime())) {
      showError(input, "Fecha inválida");
      return false;
    }
    const maxDate = new Date(today.getFullYear() - 18, today.getMonth(), today.getDate());
    const minDate = new Date(today.getFullYear() - 70, today.getMonth(), today.getDate());
    if (val < minDate || val > maxDate) {
      showError(input, `La fecha debe estar entre ${minDate.toLocaleDateString()} y ${maxDate.toLocaleDateString()}`);
      return false;
    }
    clearError(input);
    return true;
  }
  // Validación correo electrónico
function validateEmail(input) {
  let val = input.value.trim();
  input.value = val;

  // Regex sencillo para validar correos
  const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

  if (!regex.test(val)) {
    showError(input, "Correo electrónico inválido");
    return false;
  }

  clearError(input);
  return true;
}


  // === ELEMENTOS DEL FORMULARIO ===
  const nombres = document.getElementById("id_adm-nombres");
  const apellidos = document.getElementById("id_adm-apellidos");
  const ci = document.getElementById("id_adm-ci");
  const direccion = document.getElementById("id_adm-direccion");
  const telefono = document.getElementById("id_adm-telefono");
  const fechaNacimiento = document.getElementById("id_adm-fecha_nacimiento");

  const username = document.getElementById("id_cuenta-username");
  const correo = document.getElementById("id_cuenta-correo");
  const password = document.getElementById("id_cuenta-password");
  const password2 = document.getElementById("id_cuenta-password2");
  

  // === EVENTOS EN TIEMPO REAL ===
  nombres.addEventListener("input", () => validateName(nombres, 3));
  apellidos.addEventListener("input", () => validateLastName(apellidos));
  ci.addEventListener("input", () => validateCI(ci));
  direccion.addEventListener("input", () => validateAddress(direccion));
  telefono.addEventListener("input", () => validatePhone(telefono));
  fechaNacimiento.addEventListener("blur", () => validateBirthDate(fechaNacimiento));

  username.addEventListener("input", () => validateUser(username));
  password.addEventListener("input", () => validatePassword(password));
  password2.addEventListener("input", () => validatePassword2(password2, password));
  correo.addEventListener("input", () => validateEmail(correo));
  // === VALIDACIÓN FINAL ===
  const form = document.querySelector("form");
  form.addEventListener("submit", (e) => {
    let valid = true;
    valid &= validateName(nombres, 3);
    valid &= validateLastName(apellidos);
    valid &= validateCI(ci);
    valid &= validateAddress(direccion);
    valid &= validatePhone(telefono);
    valid &= validateBirthDate(fechaNacimiento);
    valid &= validateUser(username);
    valid &= validatePassword(password);
    valid &= validatePassword2(password2, password);
    valid &= validateEmail(correo);

    if (!valid) e.preventDefault();
  });
});

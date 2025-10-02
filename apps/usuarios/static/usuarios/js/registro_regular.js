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
    errorEl.textContent = " ❌ " + message;
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

  // Validación nombres (padre o estudiante)
  function validateName(input, maxWords) {
    const val = input.value;
  
    // Revisar espacios al inicio o final
    if (/^\s|\s$/.test(val)) {
      showError(input, "No se permiten espacios al inicio ni al final");
      return false;
    }

    const words = val.split(/\s+/); // separar palabras por espacio

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
        // revisa si hay números del 1-10
        if (/^[1-9]$|10/.test(w)) {
          input.value = input.value.replace(w, numberToRoman(parseInt(w)));
        } else {
          showError(input, "No se permiten números ni caracteres especiales");
          return false;
        }
      }
    }

    clearError(input);
    return true;
  }

  // Validación apellido (padre o estudiante)
  function validateLastName(input, maxWords = 2) {
    const val = input.value;

    // Revisar espacios al inicio o final
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

  // Validación CI
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

  // Validación teléfono Bolivia
  function validatePhone(input) {
    let val = input.value.trim();
    input.value = val.replace(/\s+/g, "");
    if (!/^7|6|2\d{7}$/.test(input.value) && val !== "") { // opcional permitir vacío
      showError(input, "Número de teléfono inválido (solo Bolivia)");
      return false;
    }
    clearError(input);
    return true;
  }

  // Validación dirección
  function validateAddress(input) {
    let val = input.value.trim();
    input.value = val;
    clearError(input);
    return true;
  }

  // Validación usuario
  function validateUser(input) {
    let val = input.value.trim();
    input.value = val;
    if (!/^[A-Za-z0-9_]+$/.test(val)) {
      showError(input, "Solo letras y _ permitidas");
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

  // Repetir contraseña
  function validatePassword2(input, originalInput) {
    if (input.value !== originalInput.value) {
      showError(input, "Las contraseñas no coinciden");
      return false;
    }
    clearError(input);
    return true;
  }

  // Validación fecha nacimiento en tiempo real
  function validateBirthDate(input, type) {
    const today = new Date();
    const val = new Date(input.value);

    if (isNaN(val.getTime())) {
      showError(input, "❌ Fecha inválida");
      return false;
    }

    let minDate, maxDate;

    if (type === "padre") {
      maxDate = new Date(today.getFullYear() - 20, today.getMonth(), today.getDate());
      minDate = new Date(today.getFullYear() - 90, today.getMonth(), today.getDate());
    } else if (type === "estudiante") {
      maxDate = new Date(today.getFullYear() - 4, today.getMonth(), today.getDate());
      minDate = new Date(today.getFullYear() - 20, today.getMonth(), today.getDate());
    } else {
      showError(input, "❌ Tipo desconocido");
      return false;
    }

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

  // Validación grupo
  function validateGroup(input) {
    if (!input.value) {
      showError(input, "Debes seleccionar un grupo");
      return false;
    }
    clearError(input);
    return true;
  }

  // Elementos del formulario
  const padreNombres = document.getElementById("padre-nombres");
  const padreApellidos = document.getElementById("padre-apellidos");
  const padreCI = document.getElementById("padre-ci");
  const padreFecha = document.getElementById("padre-fecha_nacimiento");
  const padreTelefono = document.getElementById("padre-telefono");
  const padreDireccion = document.getElementById("padre-direccion");

  const usuario = document.getElementById("cuenta-nombre_usuario");
  const contrasena = document.getElementById("cuenta-contrasena");
  const contrasena2 = document.getElementById("cuenta-contrasena2");

  const estNombres = document.getElementById("est-nombres");
  const estApellidos = document.getElementById("est-apellidos");
  const estCI = document.getElementById("est-ci");
  const estFecha = document.getElementById("est-fecha_nacimiento");
  const estTelefono = document.getElementById("est-telefono");
  const estDireccion = document.getElementById("est-direccion");
  const estColegio = document.getElementById("est-colegio_universidad");
  const estGrupo = document.getElementById("est-grupo");

  // Aplicando validaciones en tiempo real
  padreNombres.addEventListener("input", () => validateName(padreNombres, 3));
  padreApellidos.addEventListener("input", () => validateLastName(padreApellidos, 2));
  padreCI.addEventListener("input", () => validateCI(padreCI));
  padreTelefono.addEventListener("input", () => validatePhone(padreTelefono));
  padreDireccion.addEventListener("input", () => validateAddress(padreDireccion));

  usuario.addEventListener("input", () => validateUser(usuario));
  contrasena.addEventListener("input", () => validatePassword(contrasena));
  contrasena2.addEventListener("input", () => validatePassword2(contrasena2, contrasena));

  estNombres.addEventListener("input", () => validateName(estNombres, 3));
  estApellidos.addEventListener("input", () => validateLastName(estApellidos, 2));
  estCI.addEventListener("input", () => validateCI(estCI));
  estTelefono.addEventListener("input", () => validatePhone(estTelefono));
  estDireccion.addEventListener("input", () => validateAddress(estDireccion));
  estColegio.addEventListener("input", () => validateAddress(estColegio));
  estGrupo.addEventListener("change", () => validateGroup(estGrupo));
  // Eventos de fecha
  padreFecha.addEventListener("blur", () => validateBirthDate(padreFecha, "padre"));
  estFecha.addEventListener("blur", () => validateBirthDate(estFecha, "estudiante"));

  // Validación final antes de enviar
  const form = document.querySelector("form");
  form.addEventListener("submit", (e) => {
    let valid = true;
    valid &= validateName(padreNombres, 3);
    valid &= validateLastName(padreApellidos, 2);
    valid &= validateCI(padreCI);
    valid &= validatePhone(padreTelefono);
    valid &= validateAddress(padreDireccion);

    valid &= validateUser(usuario);
    valid &= validatePassword(contrasena);
    valid &= validatePassword2(contrasena2, contrasena);

    valid &= validateName(estNombres, 3);
    valid &= validateLastName(estApellidos, 2);
    valid &= validateCI(estCI);
    valid &= validatePhone(estTelefono);
    valid &= validateAddress(estDireccion);
    valid &= validateAddress(estColegio);
    valid &= validateGroup(estGrupo);

    if (!valid) e.preventDefault();
  });

});

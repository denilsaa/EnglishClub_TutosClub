document.addEventListener("DOMContentLoaded", () => {
  const form = document.querySelector(".form-container");
  if (form) {
    setTimeout(() => {
      form.classList.add("show");
    }, 200); // retrasa un poquito la animación
  }

  // Animar mensajes dinámicos
  const messages = document.querySelectorAll(".messages div");
  messages.forEach((msg, index) => {
    msg.style.animationDelay = `${index * 0.2}s`;
  });
});

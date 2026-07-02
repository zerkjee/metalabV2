document.querySelectorAll(".newsletter-form").forEach((form) => {
  form.addEventListener("submit", (event) => {
    event.preventDefault();
    form.replaceChildren();

    const message = document.createElement("p");
    message.className = "text-white mb-0 py-2";
    message.textContent = "Obrigado! Em breve voce recebera nossas novidades.";
    form.appendChild(message);
  });
});

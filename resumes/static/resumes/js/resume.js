// resume.js

// Animate page on load
document.addEventListener("DOMContentLoaded", () => {
    const fadeElements = document.querySelectorAll(".fade-slide-up");

    fadeElements.forEach((el, i) => {
        el.style.animationDelay = `${i * 0.2}s`;
        el.classList.add("animate");
    });
});

// Toast popup message (for success or error messages)
function showToast(message, type = "info") {
    const toast = document.createElement("div");
    toast.className = `toast-message ${type}`;
    toast.textContent = message;

    document.body.appendChild(toast);

    setTimeout(() => {
        toast.classList.add("show");
    }, 100);

    setTimeout(() => {
        toast.classList.remove("show");
        setTimeout(() => document.body.removeChild(toast), 300);
    }, 3000);
}

// Optional: hook into Django message tags
document.addEventListener("DOMContentLoaded", () => {
    const flashMessages = document.querySelectorAll(".django-message");
    flashMessages.forEach((msg) => {
        const text = msg.textContent.trim();
        const type = msg.dataset.level || "info";
        showToast(text, type);
    });
});

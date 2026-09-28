function showToast(message, type = "success") {
    const container = document.getElementById("toast-container");
    if (!container) return;

    const toast = document.createElement("div");
    toast.className = `toast toast-${type}`;
    toast.setAttribute("popover", "manual");
    toast.textContent = message;
    container.appendChild(toast);
    toast.showPopover();

    setTimeout(() => {
        toast.classList.add("is-leaving");
        setTimeout(() => {
            toast.hidePopover();
            toast.remove();
        }, 300);
    }, 3000);
}

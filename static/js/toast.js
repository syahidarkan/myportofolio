function repositionToasts(container) {
    let bottom = 24;
    container.querySelectorAll(".toast:popover-open").forEach((el) => {
        el.style.bottom = `${bottom}px`;
        bottom += el.offsetHeight + 10;
    });
}

function showToast(message, type = "success") {
    const container = document.getElementById("toast-container");
    if (!container) return;

    const toast = document.createElement("div");
    toast.className = `toast toast-${type}`;
    toast.setAttribute("popover", "manual");
    toast.textContent = message;
    container.appendChild(toast);
    toast.showPopover();
    repositionToasts(container);

    setTimeout(() => {
        toast.classList.add("is-leaving");
        setTimeout(() => {
            toast.hidePopover();
            toast.remove();
            repositionToasts(container);
        }, 300);
    }, 3000);
}

/* KoNote Web — minimal vanilla JS for interactions */

// HTMX configuration
document.body.addEventListener("htmx:configRequest", function (event) {
    // Include CSRF token in HTMX requests
    const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]");
    if (csrfToken) {
        event.detail.headers["X-CSRFToken"] = csrfToken.value;
    }
});

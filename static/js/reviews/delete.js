document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("deleteForm");

    form.addEventListener("submit", (event) => {
        event.preventDefault();

        const url = form.getAttribute("data-url");
        const redirectUrl = form.getAttribute("data-redirect-url");
        const formData = new FormData(form);
        const csrfToken = formData.get("csrfmiddlewaretoken");

        fetch(url, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': csrfToken,
                'Accept': 'application/json'
            },
            credentials: 'same-origin'
        })
        .then(response => {
            if (response.status === 204) {
                window.location.href = redirectUrl;
            } else {
                return response.json().then(data => {
                    const errorText = Object.entries(data)
                        .map(([field, messages]) => `${field}: ${messages.join(", ")}`)
                        .join("\n");
                    throw new Error(errorText || "Delete failed");
                });
            }
        })
        .catch(error => {
            console.error("Error:", error);
            alert("Delete failed:\n" + error.message);
        });
    });
});

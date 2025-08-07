document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById("createForm");

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const formData = new FormData(form);
        const redirectUrl = form.getAttribute("data-redirect-url");
        const csrfToken = formData.get("csrfmiddlewaretoken");

        fetch(form.action, {
            method: 'PATCH',
            headers: {
                'X-CSRFToken': csrfToken,
            },
            body: formData
        })
        .then(response => {
            if (response.status === 200) {
                window.location.href = redirectUrl;
            } else {
                return response.json().then(data => {
                    const errorText = Object.entries(data)
                        .map(([field, messages]) => `${field}: ${messages.join(", ")}`)
                        .join("\n");
                    throw new Error(errorText || "Update failed");
                });
            }
        })
        .catch(error => {
            console.error("Network error:", error);
            alert("Update failed:\n" + error.message);
        });
    });
});

document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById("createForm");

    form.addEventListener('submit', async function (e) {
        e.preventDefault();

        const formData = new FormData(form);
        const redirectUrl = form.getAttribute("data-redirect-url");
        const csrfToken = formData.get("csrfmiddlewaretoken");

        fetch(form.action, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
            },
            body: formData
        })
        .then(response => {
            if (response.status === 201) {
                window.location.href = redirectUrl;
            } else {
                return response.json().then(data => {
                    const errors = Object.entries(data)
                        .map(([field, messages]) => `${field}: ${messages.join(", ")}`)
                        .join("\n");
                    throw new Error(errors || "Create Failed");
                });
            }
        })
        .catch(error => {
            console.error('Network error:', error.message);
            alert('Request failed:\n' + error.message);
        });
    });
});

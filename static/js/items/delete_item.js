document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("deleteForm");

    form.addEventListener("submit", function (event) {
        event.preventDefault();

        const url = form.getAttribute("data-url");
        const redirectUrl = form.getAttribute("data-redirect-url");
        const formData = new FormData(form);
        const csrfToken = formData.get("csrfmiddlewaretoken");

        fetch(url, {
            method: 'DELETE',
            headers: {
                "X-CSRFToken": csrfToken,
                'Accept': 'application/json'
            },
            credentials: "same-origin"
        })
        .then(response => {
            if (response.status === 204) {
                window.location.href = redirectUrl;
            } else {
                return response.json().then(data => {
                    throw new Error(data?.message || "Delete failed");
                });
            }
        })
        .catch(error => {
            console.error("Error:", error);
        });
    });
});

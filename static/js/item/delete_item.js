document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("deleteForm");

    form.addEventListener("submit", function (event) {
        event.preventDefault();

        const url = form.getAttribute("data-url");
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
        .then(response => response.json())
        .then(data => {
            if (data.status === 200) {
                // TODO: Redirect
            } else {
                throw new Error("Delete failed");
            }
        })
        .catch(error => {
            console.error("Error:", error);
        });
    });
});

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
        .then(response =>{
            if (response.status === 201) {
                window.location.href = redirectUrl;
            } else {
                return response.json().then(data => {
                    throw new Error(data?.message || "Create Failed");
                });
            }
        })
        .catch(error => {
            console.error('Network error:', error);
            alert('Request failed.');
        })
    });
});

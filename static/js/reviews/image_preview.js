document.addEventListener("DOMContentLoaded", () => {
  const coverInput = document.getElementById("id_cover");
  const coverUpload = document.getElementById("coverUpload");
  const previewImg = document.getElementById("coverPreview");
  const coverText = document.getElementById("coverText");
  const removeButton = document.getElementById("removeButton");

  coverUpload.addEventListener("click", () => coverInput.click());

  coverInput.addEventListener("change", () => {
    const file = coverInput.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        previewImg.src = e.target.result;
        coverText.textContent = file.name;
      };
      reader.readAsDataURL(file);
    }
  });
  removeButton.addEventListener("click", (event) => {
    event.preventDefault()
    previewImg.src = "/static/img/plus.png"; // fallback
    coverText.textContent = "Choose cover";
  })
});

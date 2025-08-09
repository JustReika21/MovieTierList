const itemSearchInput = document.getElementById('item-search-input');
const itemSearchResults = document.getElementById('item-search-results');
const userId = itemSearchInput.dataset.userId;

let searchTimeout = null;

itemSearchInput.addEventListener('input', () => {
  const q = itemSearchInput.value.trim();
  clearTimeout(searchTimeout);

  if (!q) {
    itemSearchResults.innerHTML = '';
    return;
  }

  searchTimeout = setTimeout(() => {
    fetch(`/api/v1/reviews/search/?user_id=${userId}&query=${encodeURIComponent(q)}`)
      .then(res => res.json())
      .then(data => {
        itemSearchResults.innerHTML = '';

        if (data.length === 0) {
          const li = document.createElement('li');
          li.textContent = 'No results found';
          li.style.color = '#aaa';
          li.style.padding = '10px';
          itemSearchResults.appendChild(li);
          return;
        }

        data.forEach(review => {
          const li = document.createElement('li');
          li.classList.add('item-search-result');
          li.innerHTML = `
            <img src="${review.cover}" class="item-search-cover" alt="Cover">
            <div class="item-search-text">
              <h4>${review.title}</h4>
              <p>Rating: ${review.rating}</p>
            </div>
          `;
          li.addEventListener('click', () => {
            window.location.href = `../../../reviews/info/${review.id}`;
          });
          itemSearchResults.appendChild(li);
        });
      });
  }, 100);
});

itemSearchInput.addEventListener('blur', () => {
  setTimeout(() => {
    itemSearchResults.innerHTML = '';
  }, 150); // Small delay allows result clicks to register
});

itemSearchInput.addEventListener('focus', () => {
  if (itemSearchInput.value.trim()) {
    const event = new Event('input');
    itemSearchInput.dispatchEvent(event);
  }
});

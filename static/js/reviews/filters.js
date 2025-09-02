const tagInput = document.getElementById('tag-input');
const ratingInput = document.getElementById('rating-input');
const typeInput = document.getElementById('type-input');
const suggestions = document.getElementById('suggestions');
const searchBtn = document.getElementById('search-btn');
const resetBtn = document.getElementById('reset-btn');

let tagTimeout = null;

tagInput.addEventListener('input', () => {
  const q = tagInput.value.trim();
  clearTimeout(tagTimeout);

  if (!q) {
    suggestions.innerHTML = '';
    return;
  }

  tagTimeout = setTimeout(() => {
    fetch(`/api/v1/tags/?query=${q}`)
      .then(res => res.json())
      .then(data => {
        suggestions.innerHTML = '';

        if (data.length === 0) {
          const li = document.createElement('li');
          li.textContent = 'No results found';
          li.style.color = '#aaa';
          suggestions.appendChild(li);
          return;
        }

        data.forEach(tag => {
          const li = document.createElement('li');
          li.textContent = tag.name;
          li.classList.add('tag-suggestion');
          li.addEventListener('click', () => {
            tagInput.value = tag.name;
            suggestions.innerHTML = '';
          });
          suggestions.appendChild(li);
        });
      });
  }, 100);
});

document.addEventListener('click', (e) => {
  if (!document.querySelector('.filters-wrapper').contains(e.target)) {
    suggestions.innerHTML = '';
  }
});

function updateFilters() {
  const params = new URLSearchParams(window.location.search);
  params.delete('page'); // reset pagination on new search

  const filters = {
    tag_filter: tagInput.value.trim(),
    rating_filter: ratingInput.value.trim(),
    type_filter: typeInput.value.trim(),
  };

  Object.entries(filters).forEach(([key, value]) => {
    if (value) {
      params.set(key, value);
    } else {
      params.delete(key);
    }
  });

  return params;
}

searchBtn.addEventListener('click', () => {
  const params = updateFilters();
  window.location.search = params.toString() ? `?${params.toString()}` : '';
});

resetBtn.addEventListener('click', () => {
  const params = new URLSearchParams(window.location.search);
  ['tag_filter', 'rating_filter', 'type_filter', 'page'].forEach((key) => params.delete(key));
  window.location.search = params.toString();
});

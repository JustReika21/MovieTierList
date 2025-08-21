const tagInput = document.getElementById('tag-input');
const ratingInput = document.getElementById('rating-input');
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

searchBtn.addEventListener('click', () => {
  const tagValue = tagInput.value.trim();
  const ratingValue = ratingInput.value.trim();
  const params = new URLSearchParams(window.location.search);

  params.delete('page');

  if (tagValue) {
    params.set('tag_filter', tagValue);
  } else {
    params.delete('tag_filter');
  }

  if (ratingValue) {
    params.set('rating_filter', ratingValue);
  } else {
    params.delete('rating_filter');
  }

  window.location.search = params.toString() ? `?${params.toString()}` : '';
});

resetBtn.addEventListener('click', () => {
  const params = new URLSearchParams(window.location.search);
  params.delete('tag_filter');
  params.delete('rating_filter');
  params.delete('page');
  window.location.search = params.toString();
});
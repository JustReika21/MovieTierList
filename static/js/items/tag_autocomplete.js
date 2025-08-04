const input = document.getElementById('tag-input');
const suggestions = document.getElementById('suggestions');
const searchBtn = document.getElementById('tag-search-btn');

input.addEventListener('input', function () {
  const q = this.value.trim();
  if (!q) {
    suggestions.innerHTML = '';
    return;
  }

  fetch(`/api/v1/tags/get/${q}`)
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
          input.value = tag.name;
          suggestions.innerHTML = '';
        });
        suggestions.appendChild(li);
      });
    });
});

searchBtn.addEventListener('click', () => {
  const selectedTag = input.value.trim();
  const params = new URLSearchParams(window.location.search);

  params.delete('page');

  if (!selectedTag) {
    params.delete('tag_filter');
  } else {
    params.set('tag_filter', selectedTag);
  }

  const newSearch = params.toString();
  window.location.search = newSearch ? `?${newSearch}` : '';
});


const resetBtn = document.getElementById('tag-reset-btn');

resetBtn.addEventListener('click', () => {
  const params = new URLSearchParams(window.location.search);
  params.delete('tag_filter');
  params.delete('page');
  window.location.search = params.toString();
});

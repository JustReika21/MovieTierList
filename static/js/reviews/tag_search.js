const tagInput = document.getElementById('tagInput');
const tagSuggestions = document.getElementById('tagSuggestions');
const selectedTags = document.getElementById('selectedTags');
const hiddenTagsContainer = document.getElementById('hiddenTagsContainer');
let chosenTags = [];

document.querySelectorAll('#selectedTags .selected-tag').forEach(el => {
  chosenTags.push({
    id: parseInt(el.dataset.id, 10),
    name: el.textContent.trim().replace('x', '').trim()
  });
  updateSelectedTags();
  updateHiddenInputs();
});

async function fetchTags(query) {
  try {
    const res = await fetch(`/api/v1/tags/?query=${encodeURIComponent(query)}`);
    if (!res.ok) return [];
    return await res.json();
  } catch (e) {
    console.error('Tag fetch failed', e);
    return [];
  }
}

function showSuggestions(tags) {
  tagSuggestions.innerHTML = '';
  if (tags.length === 0) {
    tagSuggestions.style.display = 'none';
    return;
  }
  tags.forEach(tag => {
    const div = document.createElement('div');
    div.textContent = tag.name;
    div.addEventListener('click', () => selectTag(tag));
    tagSuggestions.appendChild(div);
  });
  tagSuggestions.style.display = 'block';
}

function selectTag(tag) {
  if (!chosenTags.some(t => t.id === tag.id)) {
    chosenTags.push(tag);
    updateSelectedTags();
    updateHiddenInputs();
  }
  tagInput.value = '';
  tagSuggestions.innerHTML = '';
  tagSuggestions.style.display = 'none';
}

function updateSelectedTags() {
  selectedTags.innerHTML = '';
  chosenTags.forEach(tag => {
    const chip = document.createElement('div');
    chip.classList.add('tag-chip');
    chip.innerHTML = `${tag.name} <span data-id="${tag.id}">×</span>`;
    chip.querySelector('span').addEventListener('click', () => removeTag(tag.id));
    selectedTags.appendChild(chip);
  });
}


function removeTag(tagId) {
  chosenTags = chosenTags.filter(t => t.id !== tagId);
  updateSelectedTags();
  updateHiddenInputs();
}

function updateHiddenInputs() {
  hiddenTagsContainer.innerHTML = '';
  chosenTags.forEach(tag => {
    const input = document.createElement('input');
    input.type = 'hidden';
    input.name = 'tags';
    input.value = tag.id;
    hiddenTagsContainer.appendChild(input);
  });
}

let debounceTimer;
tagInput.addEventListener('input', () => {
  clearTimeout(debounceTimer);
  const query = tagInput.value.trim();
  if (query.length === 0) {
    tagSuggestions.style.display = 'none';
    return;
  }
  debounceTimer = setTimeout(async () => {
    const tags = await fetchTags(query);
    showSuggestions(tags);
  }, 200);
});

tagInput.addEventListener('blur', () => {
  setTimeout(() => {
    tagSuggestions.style.display = 'none';
  }, 200);
});

tagInput.addEventListener('focus', () => {
  if (tagSuggestions.children.length > 0) {
    tagSuggestions.style.display = 'block';
  }
});

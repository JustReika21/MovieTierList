const itemSearchInput = document.getElementById('item-search-input');
const itemSearchResults = document.getElementById('item-search-results');
const itemSearchContainer = document.getElementById('item-search-container');
const selectedReviews = document.getElementById('selectedReviews');
const hiddenReviewsContainer = document.getElementById('hiddenReviewsContainer');
const userId = itemSearchInput.dataset.userId;

let searchTimeout = null;
let chosenReviews = [];

itemSearchInput.addEventListener('input', () => {
  const q = itemSearchInput.value.trim();
  clearTimeout(searchTimeout);

  if (!q) {
    itemSearchResults.innerHTML = '';
    itemSearchContainer.style.display = 'none';
    return;
  }

  searchTimeout = setTimeout(async () => {
    try {
      const res = await fetch(`/api/v1/reviews/search/?user_id=${userId}&query=${encodeURIComponent(q)}`);
      const data = await res.json();

      itemSearchResults.innerHTML = '';

      if (data.length === 0) {
        const li = document.createElement('li');
        li.textContent = 'No results found';
        li.classList.add('item-search-result');
        itemSearchResults.appendChild(li);
        itemSearchContainer.style.display = 'block';
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
        li.addEventListener('click', () => selectReview(review));
        itemSearchResults.appendChild(li);
      });

      itemSearchContainer.style.display = 'block';
    } catch (err) {
      console.error('Search failed:', err);
    }
  }, 200);
});

function selectReview(review) {
  if (!chosenReviews.some(r => r.id === review.id)) {
    chosenReviews.push(review);
    updateSelectedReviews();
    updateHiddenInputs();
  }
  itemSearchInput.value = '';
  itemSearchResults.innerHTML = '';
  itemSearchContainer.style.display = 'none';
}

function updateSelectedReviews() {
  selectedReviews.innerHTML = '';
  chosenReviews.forEach(review => {
    const chip = document.createElement('div');
    chip.classList.add('tag-chip');
    chip.innerHTML = `${review.title} <span data-id="${review.id}">×</span>`;
    chip.querySelector('span').addEventListener('click', () => removeReview(review.id));
    selectedReviews.appendChild(chip);
  });
}

function removeReview(id) {
  chosenReviews = chosenReviews.filter(r => r.id !== id);
  updateSelectedReviews();
  updateHiddenInputs();
}

function updateHiddenInputs() {
  hiddenReviewsContainer.innerHTML = '';
  chosenReviews.forEach(review => {
    const input = document.createElement('input');
    input.type = 'hidden';
    input.name = 'reviews';
    input.value = review.id;
    hiddenReviewsContainer.appendChild(input);
  });
}

itemSearchInput.addEventListener('blur', () => {
  setTimeout(() => {
    itemSearchContainer.style.display = 'none';
  }, 150);
});

itemSearchInput.addEventListener('focus', () => {
  if (itemSearchResults.children.length > 0) {
    itemSearchContainer.style.display = 'block';
  }
});

document.addEventListener('DOMContentLoaded', () => {
  const initialReviews = Array.from(selectedReviews.querySelectorAll('.selected-tag'));
  initialReviews.forEach(tag => {
    const id = parseInt(tag.dataset.id, 10);
    const title = tag.textContent.trim().replace('×', '').trim();
    chosenReviews.push({ id, title });
  });

  updateSelectedReviews();
  updateHiddenInputs();
});

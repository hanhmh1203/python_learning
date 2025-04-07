// Constants and Configuration
const API_URL = 'https://quotes-api-thrumming-log-8356.fly.dev';
const API_ENDPOINTS = {
  allQuotes: '/api/quotes',
  categories: '/api/categories',
  quotesByCategory: '/api/quotes/category/',
  favorite: '/api/quotes/{id}/favorite',
  unfavorite: '/api/quotes/{id}/favorite',
};

// Generate a simple user ID for favorites functionality
const USER_ID = localStorage.getItem('quotes_user_id') || generateUserId();
if (!localStorage.getItem('quotes_user_id')) {
  localStorage.setItem('quotes_user_id', USER_ID);
}

// DOM Elements
const quotesContainer = document.getElementById('quotes-container');
const categoryFilter = document.getElementById('category-filter');
const modal = document.getElementById('quote-modal');
const modalClose = document.querySelector('.close');
const quoteDetail = document.getElementById('quote-detail');

// Event Listeners
document.addEventListener('DOMContentLoaded', initApp);
categoryFilter.addEventListener('change', handleCategoryChange);
modalClose.addEventListener('click', closeModal);
window.addEventListener('click', (e) => {
  if (e.target === modal) closeModal();
});

// Initialize Application
async function initApp() {
  try {
    await Promise.all([
      fetchQuotes(),
      fetchCategories()
    ]);
  } catch (error) {
    showError('Failed to initialize the application. Please try again later.');
    console.error('Initialization error:', error);
  }
}

// Fetch all quotes from the API
async function fetchQuotes(category = '') {
  let endpoint = category 
    ? `${API_ENDPOINTS.quotesByCategory}${category}?user_id=${USER_ID}`
    : `${API_ENDPOINTS.allQuotes}?user_id=${USER_ID}`;
  
  try {
    showLoading();
    
    // Use fetch with mode: 'cors' explicitly
    const response = await fetch(`${API_URL}${endpoint}`, {
      method: 'GET',
      mode: 'cors',
      headers: {
        'Accept': 'application/json'
      }
    });
    
    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }
    
    const quotes = await response.json();
    renderQuotes(quotes);
    return quotes;
  } catch (error) {
    showError(`Failed to load quotes. Please try again later. Error: ${error.message}`);
    console.error('Error fetching quotes:', error);
    return [];
  }
}

// Fetch all categories from the API
async function fetchCategories() {
  try {
    const response = await fetch(`${API_URL}${API_ENDPOINTS.categories}`, {
      method: 'GET',
      mode: 'cors',
      headers: {
        'Accept': 'application/json'
      }
    });
    
    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }
    
    const categories = await response.json();
    renderCategories(categories);
    return categories;
  } catch (error) {
    console.error('Error fetching categories:', error);
    return [];
  }
}

// Render quotes to the DOM
function renderQuotes(quotes) {
  clearElement(quotesContainer);
  
  if (!quotes || quotes.length === 0) {
    quotesContainer.innerHTML = '<div class="error"><p>No quotes found</p></div>';
    return;
  }
  
  quotes.forEach(quote => {
    const quoteCard = document.createElement('div');
    quoteCard.className = 'quote-card';
    quoteCard.dataset.id = quote.id;
    
    quoteCard.innerHTML = `
      <p class="quote-text">"${truncateText(quote.text, 150)}"</p>
      <p class="quote-author">- ${quote.author}</p>
      ${quote.category ? `<span class="quote-category">${quote.category}</span>` : ''}
      <button class="favorite-btn ${quote.is_favorite ? 'favorited' : ''}">
        <i class="fas fa-star"></i>
      </button>
    `;
    
    // Add event listeners to the card
    quoteCard.addEventListener('click', (e) => {
      if (!e.target.closest('.favorite-btn')) {
        showQuoteDetails(quote);
      }
    });
    
    const favoriteBtn = quoteCard.querySelector('.favorite-btn');
    favoriteBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      toggleFavorite(quote.id, !quote.is_favorite, favoriteBtn);
    });
    
    quotesContainer.appendChild(quoteCard);
  });
}

// Render categories to the filter dropdown
function renderCategories(categories) {
  categories.forEach(category => {
    const option = document.createElement('option');
    option.value = category;
    option.textContent = category;
    categoryFilter.appendChild(option);
  });
}

// Show quote details in modal
function showQuoteDetails(quote) {
  quoteDetail.innerHTML = `
    <p class="detail-quote">"${quote.text}"</p>
    <p class="detail-author"><strong>Author:</strong> ${quote.author}</p>
    ${quote.source ? `<p class="detail-source"><strong>Source:</strong> ${quote.source}</p>` : ''}
    ${quote.category ? `<p><strong>Category:</strong> ${quote.category}</p>` : ''}
    <div class="detail-meta">
      <span>Added on ${formatDate(quote.created_at)}</span>
      <button class="favorite-btn detail-favorite ${quote.is_favorite ? 'favorited' : ''}">
        <i class="fas fa-star"></i> ${quote.is_favorite ? 'Remove from favorites' : 'Add to favorites'}
      </button>
    </div>
  `;
  
  // Add event listener for favorite button in modal
  const detailFavoriteBtn = quoteDetail.querySelector('.detail-favorite');
  detailFavoriteBtn.addEventListener('click', () => {
    toggleFavorite(quote.id, !quote.is_favorite, detailFavoriteBtn);
    
    // Also update the corresponding card on the main page
    const cardBtn = document.querySelector(`.quote-card[data-id="${quote.id}"] .favorite-btn`);
    if (cardBtn) {
      cardBtn.classList.toggle('favorited');
    }
  });
  
  modal.style.display = 'block';
}

// Close the modal
function closeModal() {
  modal.style.display = 'none';
}

// Toggle favorite status for a quote
async function toggleFavorite(quoteId, shouldFavorite, buttonEl) {
  try {
    const endpoint = API_ENDPOINTS.favorite.replace('{id}', quoteId);
    const method = shouldFavorite ? 'POST' : 'DELETE';
    
    const options = {
      method,
      mode: 'cors',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      }
    };
    
    // For POST requests, we need to include a body with user_id
    if (method === 'POST') {
      options.body = JSON.stringify({ user_id: USER_ID });
    }
    
    // For DELETE requests, we include the user_id as a query parameter
    const url = method === 'DELETE'
      ? `${API_URL}${endpoint}?user_id=${USER_ID}`
      : `${API_URL}${endpoint}`;
    
    const response = await fetch(url, options);
    
    if (!response.ok) {
      throw new Error(`Failed to ${shouldFavorite ? 'add' : 'remove'} favorite`);
    }
    
    // Update the UI
    if (buttonEl) {
      buttonEl.classList.toggle('favorited');
      
      // Update text if it's in the detail view
      if (buttonEl.classList.contains('detail-favorite')) {
        buttonEl.innerHTML = `
          <i class="fas fa-star"></i> ${shouldFavorite ? 'Remove from favorites' : 'Add to favorites'}
        `;
      }
    }
    
    return true;
  } catch (error) {
    console.error('Error toggling favorite:', error);
    return false;
  }
}

// Event handler for category filter changes
function handleCategoryChange() {
  const selectedCategory = categoryFilter.value;
  if (selectedCategory) {
    fetchQuotes(selectedCategory);
  } else {
    fetchQuotes();
  }
}

// Helper Functions
function showLoading() {
  quotesContainer.innerHTML = '<div class="loading"><p>Loading quotes...</p></div>';
}

function showError(message) {
  quotesContainer.innerHTML = `<div class="error"><p>${message}</p></div>`;
}

function clearElement(element) {
  element.innerHTML = '';
}

function truncateText(text, maxLength) {
  if (text.length <= maxLength) return text;
  return text.substring(0, maxLength) + '...';
}

function formatDate(dateString) {
  const options = { year: 'numeric', month: 'long', day: 'numeric' };
  return new Date(dateString).toLocaleDateString(undefined, options);
}

function generateUserId() {
  return 'user_' + Math.random().toString(36).substring(2, 15);
}
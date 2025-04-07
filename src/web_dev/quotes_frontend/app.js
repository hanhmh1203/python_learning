// Constants and Configuration
const API_URL = 'https://quotes-api-thrumming-log-8356.fly.dev';
const API_ENDPOINTS = {
  allQuotes: '/api/quotes',
  categories: '/api/categories',
  quotesByCategory: '/api/quotes/category/',
  favorite: '/api/quotes/{id}/favorite',
  unfavorite: '/api/quotes/{id}/favorite',
  createQuote: '/api/quotes', 
  deleteQuote: '/api/quotes/{id}',
};

// Default admin credentials (will be overridden by config file if available)
let ADMIN_CREDENTIALS = {
  username: 'admin',
  password: 'password'
};

// Try to load actual credentials from config file
document.addEventListener('DOMContentLoaded', () => {
  fetch('admin-config.json')
    .then(response => {
      if (!response.ok) {
        console.warn('Admin config file not found. Using default credentials.');
        return null;
      }
      return response.json();
    })
    .then(data => {
      if (data && data.adminCredentials) {
        ADMIN_CREDENTIALS = data.adminCredentials;
        console.log('Admin credentials loaded from config file');
      }
    })
    .catch(error => {
      console.error('Error loading admin config:', error);
    });
});

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

// Admin DOM Elements
const adminLoginBtn = document.getElementById('admin-login-btn');
const adminPanelBtn = document.getElementById('admin-panel-btn');
const logoutBtn = document.getElementById('logout-btn');
const adminLoginModal = document.getElementById('admin-login-modal');
const adminPanelModal = document.getElementById('admin-panel-modal');
const adminLoginForm = document.getElementById('admin-login-form');
const adminLoginError = document.getElementById('login-error');
const adminCloseBtn = document.querySelector('.admin-close');
const adminPanelCloseBtn = document.querySelector('.admin-panel-close');
const createQuoteForm = document.getElementById('create-quote-form');
const quoteCategory = document.getElementById('quote-category');
const newCategoryCheckbox = document.getElementById('new-category-checkbox');
const newCategoryInput = document.getElementById('new-category-input');
const createQuoteMessage = document.getElementById('create-quote-message');

// Import Quotes DOM Elements
const importForm = document.getElementById('import-form');
const excelFileInput = document.getElementById('excel-file');
const importMessage = document.getElementById('import-message');
const importPreview = document.getElementById('import-preview');
const quotesTableBody = document.getElementById('quotes-table-body');
const addRowBtn = document.getElementById('add-row-btn');
const submitAllBtn = document.getElementById('submit-all-btn');
const submitResult = document.getElementById('submit-result');
const tabButtons = document.querySelectorAll('.tab-btn');
const tabContents = document.querySelectorAll('.tab-content');

// Manage Quotes DOM Elements
const refreshQuotesBtn = document.getElementById('refresh-quotes-btn');
const manageQuotesTableBody = document.getElementById('manage-quotes-table-body');
const manageQuotesLoading = document.getElementById('manage-quotes-loading');
const manageQuotesMessage = document.getElementById('manage-quotes-message');
const deleteConfirmModal = document.getElementById('delete-confirm-modal');
const confirmDeleteBtn = document.getElementById('confirm-delete-btn');
const cancelDeleteBtn = document.getElementById('cancel-delete-btn');
let currentQuoteToDelete = null;

// Event Listeners
document.addEventListener('DOMContentLoaded', initApp);
categoryFilter.addEventListener('change', handleCategoryChange);
modalClose.addEventListener('click', closeModal);
window.addEventListener('click', (e) => {
  if (e.target === modal) closeModal();
});

// Admin Event Listeners
adminLoginBtn.addEventListener('click', openAdminLoginModal);
adminPanelBtn.addEventListener('click', openAdminPanelModal);
logoutBtn.addEventListener('click', handleLogout);
adminLoginForm.addEventListener('submit', handleAdminLogin);
adminCloseBtn.addEventListener('click', closeAdminLoginModal);
adminPanelCloseBtn.addEventListener('click', closeAdminPanelModal);
window.addEventListener('click', (e) => {
  if (e.target === adminLoginModal) closeAdminLoginModal();
  if (e.target === adminPanelModal) closeAdminPanelModal();
});
newCategoryCheckbox.addEventListener('change', toggleNewCategoryInput);
createQuoteForm.addEventListener('submit', handleCreateQuote);

// Import Event Listeners
importForm.addEventListener('submit', handleExcelImport);
addRowBtn.addEventListener('click', addEmptyRow);
submitAllBtn.addEventListener('click', submitAllQuotes);
tabButtons.forEach(button => {
  button.addEventListener('click', () => switchTab(button.dataset.tab));
});

// Manage Quotes Event Listeners
refreshQuotesBtn.addEventListener('click', loadAllQuotesForManagement);
confirmDeleteBtn.addEventListener('click', confirmDeleteQuote);
cancelDeleteBtn.addEventListener('click', cancelDeleteQuote);
window.addEventListener('click', (e) => {
  if (e.target === deleteConfirmModal) cancelDeleteQuote();
});

// Initialize Application
async function initApp() {
  try {
    // Check if admin is logged in
    checkAdminLoginStatus();
    
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

// Render categories to the filter dropdown and quote form
function renderCategories(categories) {
  // Clear existing options, except the default one for filter
  while (categoryFilter.children.length > 1) {
    categoryFilter.removeChild(categoryFilter.lastChild);
  }
  
  // Clear all options in the quote form dropdown
  quoteCategory.innerHTML = '';
  
  // Add a default empty option to the quote form dropdown
  const defaultOption = document.createElement('option');
  defaultOption.value = '';
  defaultOption.textContent = 'Select a category';
  quoteCategory.appendChild(defaultOption);
  
  // Add categories to both dropdowns
  categories.forEach(category => {
    // For the filter dropdown
    const filterOption = document.createElement('option');
    filterOption.value = category;
    filterOption.textContent = category;
    categoryFilter.appendChild(filterOption);
    
    // For the quote form dropdown
    const formOption = document.createElement('option');
    formOption.value = category;
    formOption.textContent = category;
    quoteCategory.appendChild(formOption);
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

// Admin Functions
function openAdminLoginModal() {
  adminLoginModal.style.display = 'block';
  adminLoginForm.reset();
  adminLoginError.textContent = '';
  adminLoginError.classList.add('hidden');
}

function closeAdminLoginModal() {
  adminLoginModal.style.display = 'none';
}

function openAdminPanelModal() {
  adminPanelModal.style.display = 'block';
  createQuoteForm.reset();
  createQuoteMessage.textContent = '';
  createQuoteMessage.classList.add('hidden');
  newCategoryCheckbox.checked = false;
  newCategoryInput.classList.add('hidden');
}

function closeAdminPanelModal() {
  adminPanelModal.style.display = 'none';
}

function handleAdminLogin(e) {
  e.preventDefault();
  
  const username = document.getElementById('username').value.trim();
  const password = document.getElementById('password').value.trim();
  
  if (username === ADMIN_CREDENTIALS.username && password === ADMIN_CREDENTIALS.password) {
    // Login successful
    localStorage.setItem('admin_logged_in', 'true');
    adminLoginBtn.classList.add('hidden');
    adminPanelBtn.classList.remove('hidden');
    logoutBtn.classList.remove('hidden');
    closeAdminLoginModal();
    
    // Show success message
    showMessage('Login successful', 'success');
  } else {
    // Login failed
    adminLoginError.textContent = 'Invalid username or password';
    adminLoginError.classList.remove('hidden');
  }
}

function checkAdminLoginStatus() {
  const isAdminLoggedIn = localStorage.getItem('admin_logged_in') === 'true';
  
  if (isAdminLoggedIn) {
    adminLoginBtn.classList.add('hidden');
    adminPanelBtn.classList.remove('hidden');
    logoutBtn.classList.remove('hidden');
  } else {
    adminLoginBtn.classList.remove('hidden');
    adminPanelBtn.classList.add('hidden');
    logoutBtn.classList.add('hidden');
  }
}

function handleLogout() {
  localStorage.removeItem('admin_logged_in');
  adminLoginBtn.classList.remove('hidden');
  adminPanelBtn.classList.add('hidden');
  logoutBtn.classList.add('hidden');
  
  // Show success message
  showMessage('Logged out successfully', 'success');
}

function toggleNewCategoryInput() {
  if (newCategoryCheckbox.checked) {
    newCategoryInput.classList.remove('hidden');
    quoteCategory.disabled = true;
  } else {
    newCategoryInput.classList.add('hidden');
    quoteCategory.disabled = false;
  }
}

async function handleCreateQuote(e) {
  e.preventDefault();
  
  // Get form data
  const formData = new FormData(createQuoteForm);
  const quoteData = {
    text: formData.get('text').trim(),
    author: formData.get('author').trim(),
    source: formData.get('source').trim() || null
  };
  
  // Handle category
  if (newCategoryCheckbox.checked) {
    const newCategory = newCategoryInput.value.trim();
    if (newCategory) {
      quoteData.category = newCategory;
    }
  } else {
    quoteData.category = formData.get('category');
  }
  
  // Validate data
  if (!quoteData.text || !quoteData.author || !quoteData.category) {
    showQuoteMessage('Please fill all required fields', 'error');
    return;
  }
  
  try {
    const response = await fetch(`${API_URL}${API_ENDPOINTS.createQuote}`, {
      method: 'POST',
      mode: 'cors',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
      body: JSON.stringify(quoteData)
    });
    
    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }
    
    const result = await response.json();
    
    // Clear form and show success message
    createQuoteForm.reset();
    showQuoteMessage('Quote created successfully!', 'success');
    
    // Refresh quotes list and categories
    await Promise.all([
      fetchQuotes(),
      fetchCategories()
    ]);
    
  } catch (error) {
    showQuoteMessage(`Failed to create quote: ${error.message}`, 'error');
    console.error('Error creating quote:', error);
  }
}

function showQuoteMessage(message, type) {
  createQuoteMessage.textContent = message;
  createQuoteMessage.className = 'message';
  createQuoteMessage.classList.add(type);
  createQuoteMessage.classList.remove('hidden');
}

function showMessage(message, type) {
  // Create a floating message element
  const messageEl = document.createElement('div');
  messageEl.className = `floating-message ${type}`;
  messageEl.textContent = message;
  
  // Add to body
  document.body.appendChild(messageEl);
  
  // Remove after 3 seconds
  setTimeout(() => {
    messageEl.classList.add('fade-out');
    setTimeout(() => document.body.removeChild(messageEl), 500);
  }, 3000);
}

// Import Functions
function switchTab(tabId) {
  // Update tab buttons
  tabButtons.forEach(btn => {
    if (btn.dataset.tab === tabId) {
      btn.classList.add('active');
    } else {
      btn.classList.remove('active');
    }
  });
  
  // Update tab contents
  tabContents.forEach(content => {
    if (content.id === `${tabId}-tab`) {
      content.classList.add('active');
    } else {
      content.classList.remove('active');
    }
  });
  
  // Reset the import form when switching to import tab
  if (tabId === 'import-quotes') {
    resetImportForm();
  }
}

function resetImportForm() {
  importForm.reset();
  importMessage.textContent = '';
  importMessage.classList.add('hidden');
  importPreview.classList.add('hidden');
  quotesTableBody.innerHTML = '';
  submitResult.textContent = '';
  submitResult.classList.add('hidden');
}

function handleExcelImport(e) {
  e.preventDefault();
  
  const file = excelFileInput.files[0];
  if (!file) {
    showImportMessage('Please select a file to import', 'error');
    return;
  }
  
  const reader = new FileReader();
  reader.onload = function(e) {
    try {
      const data = new Uint8Array(e.target.result);
      const workbook = XLSX.read(data, { type: 'array' });
      
      // Get the first sheet
      const firstSheetName = workbook.SheetNames[0];
      const worksheet = workbook.Sheets[firstSheetName];
      
      // Convert to JSON
      const jsonData = XLSX.utils.sheet_to_json(worksheet, { header: 1 });
      
      if (jsonData.length < 2) {
        showImportMessage('The Excel file does not contain enough data', 'error');
        return;
      }
      
      processExcelData(jsonData);
    } catch (error) {
      showImportMessage(`Error processing file: ${error.message}`, 'error');
      console.error('Excel import error:', error);
    }
  };
  
  reader.onerror = function() {
    showImportMessage('Error reading file', 'error');
  };
  
  reader.readAsArrayBuffer(file);
}

function processExcelData(data) {
  // Check if headers exist and find their indices
  const headers = data[0].map(h => String(h).toLowerCase());
  
  const requiredColumns = ['text', 'author', 'category'];
  const missingColumns = requiredColumns.filter(col => !headers.includes(col));
  
  if (missingColumns.length > 0) {
    showImportMessage(`Missing required columns: ${missingColumns.join(', ')}`, 'error');
    return;
  }
  
  const columnIndices = {
    text: headers.indexOf('text'),
    author: headers.indexOf('author'),
    source: headers.indexOf('source'),
    category: headers.indexOf('category')
  };
  
  // Extract quotes from data (skip the header row)
  const quotes = [];
  for (let i = 1; i < data.length; i++) {
    const row = data[i];
    if (row.length === 0 || !row[columnIndices.text]) continue; // Skip empty rows
    
    quotes.push({
      text: row[columnIndices.text] || '',
      author: row[columnIndices.author] || '',
      source: columnIndices.source >= 0 ? (row[columnIndices.source] || '') : '',
      category: row[columnIndices.category] || ''
    });
  }
  
  if (quotes.length === 0) {
    showImportMessage('No valid quotes found in the file', 'error');
    return;
  }
  
  // Render the quotes table
  renderQuotesTable(quotes);
  showImportMessage(`Successfully loaded ${quotes.length} quotes. You can now edit them before submitting.`, 'success');
  importPreview.classList.remove('hidden');
}

function renderQuotesTable(quotes) {
  quotesTableBody.innerHTML = '';
  
  quotes.forEach((quote, index) => {
    const row = createQuoteTableRow(quote, index);
    quotesTableBody.appendChild(row);
  });
}

function createQuoteTableRow(quote, index) {
  const row = document.createElement('tr');
  row.dataset.index = index;
  
  // Text cell with contenteditable div
  const textCell = document.createElement('td');
  const textDiv = document.createElement('div');
  textDiv.className = 'editable';
  textDiv.contentEditable = true;
  textDiv.textContent = quote.text;
  textCell.appendChild(textDiv);
  
  // Author cell with contenteditable div
  const authorCell = document.createElement('td');
  const authorDiv = document.createElement('div');
  authorDiv.className = 'editable';
  authorDiv.contentEditable = true;
  authorDiv.textContent = quote.author;
  authorCell.appendChild(authorDiv);
  
  // Source cell with contenteditable div
  const sourceCell = document.createElement('td');
  const sourceDiv = document.createElement('div');
  sourceDiv.className = 'editable';
  sourceDiv.contentEditable = true;
  sourceDiv.textContent = quote.source;
  sourceCell.appendChild(sourceDiv);
  
  // Category cell with dropdown
  const categoryCell = document.createElement('td');
  const categorySelect = document.createElement('select');
  categorySelect.className = 'quote-category-select';
  
  // Add blank option
  const blankOption = document.createElement('option');
  blankOption.value = '';
  blankOption.textContent = 'Select a category';
  categorySelect.appendChild(blankOption);
  
  // Get categories from the main category dropdown
  const categories = Array.from(quoteCategory.options).slice(1).map(opt => opt.value);
  
  // Add existing categories
  categories.forEach(category => {
    const option = document.createElement('option');
    option.value = category;
    option.textContent = category;
    categorySelect.appendChild(option);
  });
  
  // Add custom category input
  const customInput = document.createElement('input');
  customInput.type = 'text';
  customInput.className = 'custom-category hidden';
  customInput.placeholder = 'Enter custom category';
  
  // Add checkbox for custom category
  const customCheckbox = document.createElement('input');
  customCheckbox.type = 'checkbox';
  customCheckbox.className = 'custom-category-checkbox';
  
  const customLabel = document.createElement('label');
  customLabel.textContent = 'Custom';
  customLabel.appendChild(customCheckbox);
  
  // Set initial category value
  if (quote.category) {
    const existingOption = Array.from(categorySelect.options).find(opt => opt.value === quote.category);
    if (existingOption) {
      existingOption.selected = true;
    } else {
      customCheckbox.checked = true;
      customInput.value = quote.category;
      customInput.classList.remove('hidden');
      categorySelect.disabled = true;
    }
  }
  
  // Toggle event for custom category
  customCheckbox.addEventListener('change', function() {
    if (this.checked) {
      customInput.classList.remove('hidden');
      categorySelect.disabled = true;
    } else {
      customInput.classList.add('hidden');
      categorySelect.disabled = false;
    }
  });
  
  categoryCell.appendChild(categorySelect);
  categoryCell.appendChild(document.createElement('br'));
  categoryCell.appendChild(customLabel);
  categoryCell.appendChild(customInput);
  
  // Actions cell
  const actionsCell = document.createElement('td');
  actionsCell.className = 'action-cell';
  
  const deleteBtn = document.createElement('button');
  deleteBtn.className = 'small-btn delete-btn';
  deleteBtn.innerHTML = '<i class="fas fa-trash"></i>';
  deleteBtn.addEventListener('click', function() {
    row.remove();
  });
  
  actionsCell.appendChild(deleteBtn);
  
  // Add all cells to the row
  row.appendChild(textCell);
  row.appendChild(authorCell);
  row.appendChild(sourceCell);
  row.appendChild(categoryCell);
  row.appendChild(actionsCell);
  
  return row;
}

function addEmptyRow() {
  const emptyQuote = {
    text: '',
    author: '',
    source: '',
    category: ''
  };
  
  const newRow = createQuoteTableRow(emptyQuote, quotesTableBody.children.length);
  quotesTableBody.appendChild(newRow);
}

function gatherQuotesFromTable() {
  const quotes = [];
  const rows = quotesTableBody.querySelectorAll('tr');
  
  rows.forEach(row => {
    const textDiv = row.querySelector('td:nth-child(1) .editable');
    const authorDiv = row.querySelector('td:nth-child(2) .editable');
    const sourceDiv = row.querySelector('td:nth-child(3) .editable');
    const categorySelect = row.querySelector('.quote-category-select');
    const customCheckbox = row.querySelector('.custom-category-checkbox');
    const customInput = row.querySelector('.custom-category');
    
    let category = '';
    if (customCheckbox.checked) {
      category = customInput.value.trim();
    } else {
      category = categorySelect.value;
    }
    
    const quote = {
      text: textDiv.textContent.trim(),
      author: authorDiv.textContent.trim(),
      source: sourceDiv.textContent.trim() || null,
      category: category
    };
    
    // Only add quotes with required fields
    if (quote.text && quote.author && quote.category) {
      quotes.push(quote);
    }
  });
  
  return quotes;
}

async function submitAllQuotes() {
  const quotes = gatherQuotesFromTable();
  
  if (quotes.length === 0) {
    showSubmitResult('No valid quotes to submit. Please ensure all quotes have text, author, and category.', 'error');
    return;
  }
  
  // Show loading message
  showSubmitResult('Submitting quotes...', '');
  
  // Track success and errors
  let successCount = 0;
  let errorCount = 0;
  let lastError = '';
  
  // Submit quotes one by one
  for (const quote of quotes) {
    try {
      const response = await fetch(`${API_URL}${API_ENDPOINTS.createQuote}`, {
        method: 'POST',
        mode: 'cors',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        body: JSON.stringify(quote)
      });
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ detail: `Error ${response.status}` }));
        throw new Error(errorData.detail || `API error: ${response.status}`);
      }
      
      successCount++;
    } catch (error) {
      errorCount++;
      lastError = error.message;
      console.error('Error submitting quote:', error);
    }
  }
  
  // Show result message
  if (errorCount === 0) {
    showSubmitResult(`Successfully submitted all ${successCount} quotes!`, 'success');
    
    // Refresh quotes list and categories
    await Promise.all([
      fetchQuotes(),
      fetchCategories()
    ]);
    
    // Clear the table after successful submit
    setTimeout(() => {
      quotesTableBody.innerHTML = '';
      importPreview.classList.add('hidden');
      importForm.reset();
    }, 3000);
    
  } else {
    showSubmitResult(`Submitted ${successCount} quotes with ${errorCount} errors. Last error: ${lastError}`, 'error');
  }
}

function showImportMessage(message, type) {
  importMessage.textContent = message;
  importMessage.className = 'message';
  importMessage.classList.add(type);
  importMessage.classList.remove('hidden');
}

function showSubmitResult(message, type) {
  submitResult.textContent = message;
  submitResult.className = 'message';
  if (type) {
    submitResult.classList.add(type);
  }
  submitResult.classList.remove('hidden');
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

// Manage Quotes Functions
function loadAllQuotesForManagement() {
  // Show loading indicator
  manageQuotesLoading.classList.remove('hidden');
  manageQuotesMessage.classList.add('hidden');
  
  // Load the quotes when switching to the Manage tab
  if (document.getElementById('manage-quotes-tab').classList.contains('active')) {
    fetchAllQuotesForAdmin();
  }
}

async function fetchAllQuotesForAdmin() {
  try {
    const response = await fetch(`${API_URL}${API_ENDPOINTS.allQuotes}`, {
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
    renderManageQuotesTable(quotes);
    manageQuotesLoading.classList.add('hidden');
    
    if (quotes.length === 0) {
      showManageQuotesMessage('No quotes found.', 'info');
    }
    
    return quotes;
  } catch (error) {
    manageQuotesLoading.classList.add('hidden');
    showManageQuotesMessage(`Failed to load quotes: ${error.message}`, 'error');
    console.error('Error fetching quotes for management:', error);
    return [];
  }
}

function renderManageQuotesTable(quotes) {
  manageQuotesTableBody.innerHTML = '';
  
  quotes.forEach(quote => {
    const row = document.createElement('tr');
    
    // ID cell
    const idCell = document.createElement('td');
    idCell.textContent = quote.id;
    
    // Text cell (truncated)
    const textCell = document.createElement('td');
    textCell.className = 'quote-text-cell';
    textCell.setAttribute('title', quote.text);
    textCell.textContent = truncateText(quote.text, 100);
    
    // Author cell
    const authorCell = document.createElement('td');
    authorCell.textContent = quote.author;
    
    // Category cell
    const categoryCell = document.createElement('td');
    categoryCell.textContent = quote.category || 'None';
    
    // Source cell
    const sourceCell = document.createElement('td');
    sourceCell.textContent = quote.source || 'N/A';
    
    // Created At cell
    const createdAtCell = document.createElement('td');
    createdAtCell.textContent = formatDate(quote.created_at);
    
    // Actions cell
    const actionsCell = document.createElement('td');
    actionsCell.className = 'action-cell';
    
    const deleteBtn = document.createElement('button');
    deleteBtn.className = 'small-btn delete-btn';
    deleteBtn.innerHTML = '<i class="fas fa-trash"></i>';
    deleteBtn.addEventListener('click', () => {
      showDeleteConfirmation(quote.id);
    });
    
    actionsCell.appendChild(deleteBtn);
    
    // Add all cells to the row
    row.appendChild(idCell);
    row.appendChild(textCell);
    row.appendChild(authorCell);
    row.appendChild(categoryCell);
    row.appendChild(sourceCell);
    row.appendChild(createdAtCell);
    row.appendChild(actionsCell);
    
    manageQuotesTableBody.appendChild(row);
  });
}

function showManageQuotesMessage(message, type) {
  manageQuotesMessage.textContent = message;
  manageQuotesMessage.className = 'message';
  manageQuotesMessage.classList.add(type);
  manageQuotesMessage.classList.remove('hidden');
}

function showDeleteConfirmation(quoteId) {
  currentQuoteToDelete = quoteId;
  deleteConfirmModal.style.display = 'block';
}

function cancelDeleteQuote() {
  deleteConfirmModal.style.display = 'none';
  currentQuoteToDelete = null;
}

async function confirmDeleteQuote() {
  if (!currentQuoteToDelete) return;
  
  try {
    const endpoint = API_ENDPOINTS.deleteQuote.replace('{id}', currentQuoteToDelete);
    
    const response = await fetch(`${API_URL}${endpoint}`, {
      method: 'DELETE',
      mode: 'cors',
      headers: {
        'Accept': 'application/json'
      }
    });
    
    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }
    
    // Close the confirmation modal
    deleteConfirmModal.style.display = 'none';
    
    // Show success message
    showMessage('Quote deleted successfully', 'success');
    
    // Refresh the quotes table
    fetchAllQuotesForAdmin();
    
    // Also refresh the main quotes display
    fetchQuotes();
    
  } catch (error) {
    console.error('Error deleting quote:', error);
    
    // Close the confirmation modal
    deleteConfirmModal.style.display = 'none';
    
    // Show error message
    showMessage(`Failed to delete quote: ${error.message}`, 'error');
  }
  
  // Reset the current quote to delete
  currentQuoteToDelete = null;
}
// Global variables
let selectedFile = null;
let processedData = null;

// DOM elements
const fileInput = document.getElementById('fileInput');
const uploadArea = document.getElementById('uploadArea');
const fileSelected = document.getElementById('fileSelected');
const fileName = document.getElementById('fileName');
const optionsSection = document.getElementById('optionsSection');
const progressSection = document.getElementById('progressSection');
const resultsSection = document.getElementById('resultsSection');
const progressFill = document.getElementById('progressFill');
const progressText = document.getElementById('progressText');

// Initialize app
document.addEventListener('DOMContentLoaded', function() {
    setupEventListeners();
});

function setupEventListeners() {
    // File input change
    fileInput.addEventListener('change', handleFileSelect);
    
    // Drag and drop
    uploadArea.addEventListener('dragover', handleDragOver);
    uploadArea.addEventListener('dragleave', handleDragLeave);
    uploadArea.addEventListener('drop', handleDrop);
    
    // Upload area click
    uploadArea.addEventListener('click', () => fileInput.click());
}

function handleFileSelect(e) {
    const file = e.target.files[0];
    if (file) {
        if (file.type === 'text/plain' || file.name.endsWith('.txt')) {
            selectedFile = file;
            showSelectedFile(file);
        } else {
            showNotification('Please select a .txt file', 'error');
        }
    }
}

function handleDragOver(e) {
    e.preventDefault();
    uploadArea.classList.add('dragover');
}

function handleDragLeave(e) {
    e.preventDefault();
    uploadArea.classList.remove('dragover');
}

function handleDrop(e) {
    e.preventDefault();
    uploadArea.classList.remove('dragover');
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        const file = files[0];
        if (file.type === 'text/plain' || file.name.endsWith('.txt')) {
            selectedFile = file;
            fileInput.files = files;
            showSelectedFile(file);
        } else {
            showNotification('Please select a .txt file', 'error');
        }
    }
}

function showSelectedFile(file) {
    fileName.textContent = file.name;
    uploadArea.style.display = 'none';
    fileSelected.style.display = 'block';
    optionsSection.style.display = 'block';
    
    showNotification(`File "${file.name}" selected successfully`, 'success');
}

function removeFile() {
    selectedFile = null;
    fileInput.value = '';
    uploadArea.style.display = 'block';
    fileSelected.style.display = 'none';
    optionsSection.style.display = 'none';
    hideOtherSections();
}

function hideOtherSections() {
    progressSection.style.display = 'none';
    resultsSection.style.display = 'none';
}

// API Functions
async function previewFile() {
    if (!selectedFile) {
        showNotification('Please select a file first', 'error');
        return;
    }
    
    try {
        const formData = new FormData();
        formData.append('file', selectedFile);
        
        showProgress('Uploading file...');
        
        const response = await fetch('/upload-vocabulary/', {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        hideProgress();
        
        showNotification(`Preview: ${data.total_count} words found`, 'info');
        
        // Show preview in a simple format
        const previewHtml = `
            <div style="background: #f7fafc; padding: 20px; border-radius: 10px; margin: 20px 0;">
                <h4>File Preview (first 10 words):</h4>
                <p style="font-family: monospace; background: white; padding: 10px; border-radius: 5px;">
                    ${data.words.join(', ')}
                    ${data.total_count > 10 ? '...' : ''}
                </p>
                <p><strong>Total words:</strong> ${data.total_count}</p>
            </div>
        `;
        
        // Insert preview after options section
        const existingPreview = document.getElementById('preview');
        if (existingPreview) {
            existingPreview.remove();
        }
        
        const previewDiv = document.createElement('div');
        previewDiv.id = 'preview';
        previewDiv.innerHTML = previewHtml;
        optionsSection.after(previewDiv);
        
    } catch (error) {
        hideProgress();
        showNotification(`Error: ${error.message}`, 'error');
    }
}

async function processFile() {
    if (!selectedFile) {
        showNotification('Please select a file first', 'error');
        return;
    }
    
    try {
        const formData = new FormData();
        formData.append('file', selectedFile);
        
        showProgress('Processing vocabulary...');
        updateProgress(10, 'Uploading file...');
        
        const response = await fetch('/process-vocabulary/', {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        updateProgress(50, 'Getting definitions from Cambridge Dictionary...');
        
        const data = await response.json();
        
        updateProgress(80, 'Translating to Vietnamese...');
        
        processedData = data.data;
        
        updateProgress(100, 'Processing complete!');
        
        setTimeout(() => {
            hideProgress();
            showResults(data.data);
        }, 1000);
        
    } catch (error) {
        hideProgress();
        showNotification(`Error: ${error.message}`, 'error');
    }
}

async function exportCSV() {
    if (!selectedFile) {
        showNotification('Please select a file first', 'error');
        return;
    }
    
    try {
        const formData = new FormData();
        formData.append('file', selectedFile);
        
        showProgress('Creating CSV file...');
        updateProgress(20, 'Processing vocabulary...');
        
        const response = await fetch('/export-csv/', {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        updateProgress(90, 'Preparing download...');
        
        // Get the blob and create download link
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'vocabulary_export.csv';
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
        
        updateProgress(100, 'Download started!');
        
        setTimeout(() => {
            hideProgress();
            showNotification('CSV file downloaded successfully!', 'success');
        }, 1000);
        
    } catch (error) {
        hideProgress();
        showNotification(`Error: ${error.message}`, 'error');
    }
}

// Progress functions
function showProgress(message) {
    hideOtherSections();
    progressSection.style.display = 'block';
    progressText.textContent = message;
    progressFill.style.width = '0%';
}

function updateProgress(percentage, message) {
    progressFill.style.width = percentage + '%';
    progressText.textContent = message;
}

function hideProgress() {
    progressSection.style.display = 'none';
}

// Results functions
function showResults(data) {
    resultsSection.style.display = 'block';
    
    // Update stats
    const totalWords = data.length;
    const errorWords = data.filter(item => item.meaning_en.startsWith('Error')).length;
    const processedWords = totalWords - errorWords;
    
    document.getElementById('totalWords').textContent = totalWords;
    document.getElementById('processedWords').textContent = processedWords;
    document.getElementById('errorWords').textContent = errorWords;
    
    // Populate table
    const tableBody = document.getElementById('resultsTableBody');
    tableBody.innerHTML = '';
    
    data.forEach(item => {
        const row = document.createElement('tr');
        const isError = item.meaning_en.startsWith('Error');
        
        if (isError) {
            row.style.backgroundColor = '#fed7d7';
        }
        
        row.innerHTML = `
            <td><strong>${item.word}</strong></td>
            <td>${item.meaning_en}</td>
            <td>${item.meaning_vi}</td>
            <td>${item.example_en}</td>
            <td>${item.example_vi}</td>
            <td>${item.ipa}</td>
            <td>${item.pos}</td>
        `;
        
        tableBody.appendChild(row);
    });
    
    showNotification('Processing completed successfully!', 'success');
}

function downloadResults() {
    if (!processedData) {
        showNotification('No data to download', 'error');
        return;
    }
    
    // Convert to CSV format
    const headers = ['Word', 'Meaning_EN', 'Meaning_VI', 'Example_EN', 'Example_VI', 'IPA', 'POS'];
    const csvContent = [
        headers.join(','),
        ...processedData.map(item => [
            `"${item.word}"`,
            `"${item.meaning_en}"`,
            `"${item.meaning_vi}"`,
            `"${item.example_en}"`,
            `"${item.example_vi}"`,
            `"${item.ipa}"`,
            `"${item.pos}"`
        ].join(','))
    ].join('\n');
    
    // Create and download file
    const blob = new Blob(['\ufeff' + csvContent], { type: 'text/csv;charset=utf-8;' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'vocabulary_results.csv';
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);
    
    showNotification('Results downloaded successfully!', 'success');
}

function resetApp() {
    removeFile();
    processedData = null;
    
    // Remove preview if exists
    const existingPreview = document.getElementById('preview');
    if (existingPreview) {
        existingPreview.remove();
    }
    
    showNotification('App reset. You can now upload a new file.', 'info');
}

// Notification functions
function showNotification(message, type = 'info') {
    const notification = document.getElementById('notification');
    const icon = notification.querySelector('.notification-icon');
    const messageEl = notification.querySelector('.notification-message');
    
    // Set message
    messageEl.textContent = message;
    
    // Set type and icon
    notification.className = `notification ${type}`;
    
    switch (type) {
        case 'success':
            icon.className = 'notification-icon fas fa-check-circle';
            break;
        case 'error':
            icon.className = 'notification-icon fas fa-exclamation-circle';
            break;
        case 'info':
        default:
            icon.className = 'notification-icon fas fa-info-circle';
            break;
    }
    
    // Show notification
    notification.classList.add('show');
    
    // Auto hide after 5 seconds
    setTimeout(() => {
        hideNotification();
    }, 5000);
}

function hideNotification() {
    const notification = document.getElementById('notification');
    notification.classList.remove('show');
} 
// Astro Camera Web Interface JavaScript

// Global state
let currentSettings = {};
let isCapturing = false;

// DOM Elements
const statusDot = document.getElementById('status-dot');
const statusText = document.getElementById('status-text');
const videoFeed = document.getElementById('video-feed');
const loadingOverlay = document.getElementById('loading-overlay');
const isoSelect = document.getElementById('iso-select');
const shutterSelect = document.getElementById('shutter-select');
const outputSelect = document.getElementById('output-select');
const imageTimeSelect = document.getElementById('image-time-select');
const imageCountSelect = document.getElementById('image-count-select');
const captureBtn = document.getElementById('capture-btn');
const captureText = document.getElementById('capture-text');
const captureStatus = document.getElementById('capture-status');

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    console.log('Astro Camera web interface loaded');

    // Load initial settings
    loadSettings();

    // Setup event listeners
    setupEventListeners();

    // Start status polling
    startStatusPolling();

    // Hide loading overlay when video loads
    videoFeed.addEventListener('load', () => {
        loadingOverlay.classList.add('hidden');
    });

    videoFeed.addEventListener('error', () => {
        console.error('Video feed error');
        showStatus('error', 'Video feed unavailable');
    });
});

// Setup event listeners for controls
function setupEventListeners() {
    isoSelect.addEventListener('change', () => updateSetting('iso', isoSelect.value));
    shutterSelect.addEventListener('change', () => updateSetting('shutter', shutterSelect.value));
    outputSelect.addEventListener('change', () => updateSetting('output', outputSelect.value));
    imageTimeSelect.addEventListener('change', () => updateSetting('image_time', imageTimeSelect.value));
    imageCountSelect.addEventListener('change', () => updateSetting('image_count', imageCountSelect.value));
    captureBtn.addEventListener('click', startCapture);
}

// Load camera settings from API
async function loadSettings() {
    try {
        const response = await fetch('/api/settings');

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const settings = await response.json();
        currentSettings = settings;

        // Populate dropdowns
        populateSelect(isoSelect, settings.iso);
        populateSelect(shutterSelect, settings.shutter);
        populateSelect(outputSelect, settings.output);
        populateSelect(imageTimeSelect, settings.image_time);
        populateSelect(imageCountSelect, settings.image_count);

        console.log('Settings loaded:', settings);
        showStatus('success', 'Connected');

    } catch (error) {
        console.error('Error loading settings:', error);
        showStatus('error', 'Connection failed');
    }
}

// Populate select dropdown with options
function populateSelect(selectElement, settingData) {
    // Clear existing options
    selectElement.innerHTML = '';

    // Add options
    settingData.options.forEach((option, index) => {
        const optionElement = document.createElement('option');
        optionElement.value = index;
        optionElement.textContent = option;

        if (index === settingData.index) {
            optionElement.selected = true;
        }

        selectElement.appendChild(optionElement);
    });
}

// Update camera setting
async function updateSetting(setting, indexValue) {
    const index = parseInt(indexValue);

    console.log(`Updating ${setting} to index ${index}`);

    try {
        const response = await fetch('/api/settings', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                setting: setting,
                index: index
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const result = await response.json();

        if (result.success) {
            console.log(`${setting} updated to ${result.value}`);
            showCaptureStatus(`${setting.toUpperCase()} updated to ${result.value}`, 'success');
        } else {
            throw new Error(result.error || 'Update failed');
        }

    } catch (error) {
        console.error('Error updating setting:', error);
        showCaptureStatus(`Failed to update ${setting}`, 'error');
    }
}

// Start image capture
async function startCapture() {
    if (isCapturing) {
        return;
    }

    isCapturing = true;
    captureBtn.disabled = true;
    captureText.textContent = 'Capturing...';
    showCaptureStatus('Capture in progress...', 'capturing');

    try {
        const response = await fetch('/api/capture', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const result = await response.json();

        if (result.success) {
            console.log('Capture completed');
            showCaptureStatus('Capture completed successfully!', 'success');
        } else {
            throw new Error(result.error || 'Capture failed');
        }

    } catch (error) {
        console.error('Error during capture:', error);
        showCaptureStatus('Capture failed: ' + error.message, 'error');
    } finally {
        isCapturing = false;
        captureBtn.disabled = false;
        captureText.textContent = 'Start Capture';

        // Hide status after 5 seconds
        setTimeout(() => {
            captureStatus.className = 'capture-status';
        }, 5000);
    }
}

// Show capture status message
function showCaptureStatus(message, type) {
    captureStatus.textContent = message;
    captureStatus.className = `capture-status ${type}`;
}

// Show connection status
function showStatus(type, message) {
    statusText.textContent = message;

    if (type === 'error') {
        statusDot.classList.add('error');
    } else {
        statusDot.classList.remove('error');
    }
}

// Poll system status periodically
function startStatusPolling() {
    setInterval(async () => {
        try {
            const response = await fetch('/api/status');

            if (!response.ok) {
                throw new Error('Status check failed');
            }

            const status = await response.json();

            // Update connection status if needed
            if (statusText.textContent === 'Connection failed') {
                showStatus('success', 'Connected');
            }

        } catch (error) {
            console.error('Status check error:', error);
            if (statusText.textContent !== 'Connection failed') {
                showStatus('error', 'Connection lost');
            }
        }
    }, 5000); // Poll every 5 seconds
}

// Utility: Debounce function for rapid changes
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Export for debugging
window.astroCamera = {
    loadSettings,
    updateSetting,
    startCapture,
    currentSettings
};

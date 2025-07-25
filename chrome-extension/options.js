// Options page JavaScript for MCP Chrome Bookmark Manager
// Placeholder implementation

document.addEventListener('DOMContentLoaded', () => {
    loadSettings();
    setupEventListeners();
});

function loadSettings() {
    // Load saved settings
    chrome.storage.sync.get({
        serverUrl: 'http://localhost:8012',
        autoOrganize: false,
        organizationStrategy: 'ai_smart',
        autoClean: false,
        maxAge: 180,
        checkBrokenLinks: true,
        notificationsEnabled: true
    }, (items) => {
        document.getElementById('serverUrl').value = items.serverUrl;
        document.getElementById('autoOrganize').checked = items.autoOrganize;
        document.getElementById('organizationStrategy').value = items.organizationStrategy;
        document.getElementById('autoClean').checked = items.autoClean;
        document.getElementById('maxAge').value = items.maxAge;
        document.getElementById('checkBrokenLinks').checked = items.checkBrokenLinks;
        document.getElementById('notificationsEnabled').checked = items.notificationsEnabled;
    });
}

function setupEventListeners() {
    document.getElementById('saveSettings').addEventListener('click', saveSettings);
    document.getElementById('resetSettings').addEventListener('click', resetSettings);
    document.getElementById('testConnection').addEventListener('click', testConnection);
}

function saveSettings() {
    const settings = {
        serverUrl: document.getElementById('serverUrl').value,
        autoOrganize: document.getElementById('autoOrganize').checked,
        organizationStrategy: document.getElementById('organizationStrategy').value,
        autoClean: document.getElementById('autoClean').checked,
        maxAge: parseInt(document.getElementById('maxAge').value),
        checkBrokenLinks: document.getElementById('checkBrokenLinks').checked,
        notificationsEnabled: document.getElementById('notificationsEnabled').checked
    };
    
    chrome.storage.sync.set(settings, () => {
        showNotification('Settings saved successfully!');
    });
}

function resetSettings() {
    if (confirm('Reset all settings to defaults?')) {
        loadSettings();
        showNotification('Settings reset to defaults');
    }
}

function testConnection() {
    showNotification('Testing connection...');
    // Placeholder for connection test
}

function showNotification(message) {
    const notification = document.getElementById('notification');
    const notificationText = document.getElementById('notificationText');
    notificationText.textContent = message;
    notification.classList.add('show');
    setTimeout(() => {
        notification.classList.remove('show');
    }, 3000);
}
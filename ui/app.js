// Configuration object
let cfg = {
    url: 'http://localhost:7860',
    key: 'dev-secret',
    useStreaming: false,
    temperature: 0.0,
    maxTokens: 1024,
    frequencyPenalty: 1.0,
    markdownRender: true,
    autoSave: true,
    showTimestamps: true,
    soundEnabled: false
};

// State management
let conversationHistory = [];
let currentConversation = [];
let stats = {
    totalRequests: 0,
    totalMessages: 0,
    totalTokens: 0,
    totalTime: 0,
    activities: []
};

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    loadConfig();
    loadHistory();
    loadStats();
    loadModels();
    setupEventListeners();
    setupKeyboardShortcuts();
    checkConnection();
    updateUI();
});

// Load configuration from localStorage
function loadConfig() {
    const saved = {
        url: localStorage.getItem('perplexity_bridge_url'),
        key: localStorage.getItem('perplexity_bridge_key'),
        streaming: localStorage.getItem('perplexity_bridge_streaming'),
        temperature: localStorage.getItem('perplexity_bridge_temperature'),
        maxTokens: localStorage.getItem('perplexity_bridge_maxTokens'),
        frequencyPenalty: localStorage.getItem('perplexity_bridge_frequencyPenalty'),
        markdownRender: localStorage.getItem('perplexity_bridge_markdownRender'),
        autoSave: localStorage.getItem('perplexity_bridge_autoSave'),
        showTimestamps: localStorage.getItem('perplexity_bridge_showTimestamps'),
        soundEnabled: localStorage.getItem('perplexity_bridge_soundEnabled')
    };
    
    if (saved.url) cfg.url = saved.url;
    if (saved.key) cfg.key = saved.key;
    if (saved.streaming !== null) cfg.useStreaming = saved.streaming === 'true';
    if (saved.temperature !== null) cfg.temperature = parseFloat(saved.temperature);
    if (saved.maxTokens !== null) cfg.maxTokens = parseInt(saved.maxTokens);
    if (saved.frequencyPenalty !== null) cfg.frequencyPenalty = parseFloat(saved.frequencyPenalty);
    if (saved.markdownRender !== null) cfg.markdownRender = saved.markdownRender === 'true';
    if (saved.autoSave !== null) cfg.autoSave = saved.autoSave === 'true';
    if (saved.showTimestamps !== null) cfg.showTimestamps = saved.showTimestamps === 'true';
    if (saved.soundEnabled !== null) cfg.soundEnabled = saved.soundEnabled === 'true';
    
    // Populate form fields
    document.getElementById('url').value = cfg.url;
    document.getElementById('key').value = cfg.key;
    document.getElementById('streaming').checked = cfg.useStreaming;
    document.getElementById('temperature').value = cfg.temperature;
    document.getElementById('tempValue').textContent = cfg.temperature.toFixed(1);
    document.getElementById('maxTokens').value = cfg.maxTokens;
    document.getElementById('tokensValue').textContent = cfg.maxTokens;
    document.getElementById('frequencyPenalty').value = cfg.frequencyPenalty;
    document.getElementById('freqValue').textContent = cfg.frequencyPenalty.toFixed(1);
    document.getElementById('markdownRender').checked = cfg.markdownRender;
    document.getElementById('autoSave').checked = cfg.autoSave;
    document.getElementById('showTimestamps').checked = cfg.showTimestamps;
    document.getElementById('soundEnabled').checked = cfg.soundEnabled;
}

// Save configuration to localStorage
function save() {
    cfg.url = document.getElementById('url').value.trim();
    cfg.key = document.getElementById('key').value.trim();
    cfg.useStreaming = document.getElementById('streaming').checked;
    cfg.temperature = parseFloat(document.getElementById('temperature').value);
    cfg.maxTokens = parseInt(document.getElementById('maxTokens').value);
    cfg.frequencyPenalty = parseFloat(document.getElementById('frequencyPenalty').value);
    cfg.markdownRender = document.getElementById('markdownRender').checked;
    cfg.autoSave = document.getElementById('autoSave').checked;
    cfg.showTimestamps = document.getElementById('showTimestamps').checked;
    cfg.soundEnabled = document.getElementById('soundEnabled').checked;
    
    localStorage.setItem('perplexity_bridge_url', cfg.url);
    localStorage.setItem('perplexity_bridge_key', cfg.key);
    localStorage.setItem('perplexity_bridge_streaming', cfg.useStreaming.toString());
    localStorage.setItem('perplexity_bridge_temperature', cfg.temperature.toString());
    localStorage.setItem('perplexity_bridge_maxTokens', cfg.maxTokens.toString());
    localStorage.setItem('perplexity_bridge_frequencyPenalty', cfg.frequencyPenalty.toString());
    localStorage.setItem('perplexity_bridge_markdownRender', cfg.markdownRender.toString());
    localStorage.setItem('perplexity_bridge_autoSave', cfg.autoSave.toString());
    localStorage.setItem('perplexity_bridge_showTimestamps', cfg.showTimestamps.toString());
    localStorage.setItem('perplexity_bridge_soundEnabled', cfg.soundEnabled.toString());
    
    showMessage('Settings saved successfully!', 'success');
    checkConnection();
    loadModels();
}

// Setup event listeners
function setupEventListeners() {
    // Tab navigation
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const tab = e.currentTarget.dataset.tab;
            switchTab(tab);
        });
    });
    
    // Sliders
    document.getElementById('temperature').addEventListener('input', (e) => {
        cfg.temperature = parseFloat(e.target.value);
        document.getElementById('tempValue').textContent = cfg.temperature.toFixed(1);
    });
    
    document.getElementById('maxTokens').addEventListener('input', (e) => {
        cfg.maxTokens = parseInt(e.target.value);
        document.getElementById('tokensValue').textContent = cfg.maxTokens;
    });
    
    document.getElementById('frequencyPenalty').addEventListener('input', (e) => {
        cfg.frequencyPenalty = parseFloat(e.target.value);
        document.getElementById('freqValue').textContent = cfg.frequencyPenalty.toFixed(1);
    });
    
    // Advanced options toggle
    document.getElementById('advancedToggle').addEventListener('click', () => {
        const panel = document.getElementById('advancedOptions');
        panel.style.display = panel.style.display === 'none' ? 'block' : 'none';
    });
    
    // Buttons
    document.getElementById('clearBtn').addEventListener('click', clearConversation);
    document.getElementById('copyBtn').addEventListener('click', copyLastResponse);
    document.getElementById('exportBtn').addEventListener('click', exportConversation);
    document.getElementById('clearHistoryBtn').addEventListener('click', clearAllHistory);
    document.getElementById('exportAllBtn').addEventListener('click', exportAllHistory);
    document.getElementById('refreshModelsBtn').addEventListener('click', loadModels);
    document.getElementById('themeToggle').addEventListener('click', toggleTheme);
    
    // Settings checkboxes
    document.getElementById('markdownRender').addEventListener('change', save);
    document.getElementById('autoSave').addEventListener('change', save);
    document.getElementById('showTimestamps').addEventListener('change', save);
    document.getElementById('soundEnabled').addEventListener('change', save);
}

// Setup keyboard shortcuts
function setupKeyboardShortcuts() {
    document.addEventListener('keydown', (e) => {
        // Ctrl+Enter to send
        if (e.ctrlKey && e.key === 'Enter') {
            e.preventDefault();
            send();
        }
        // Ctrl+K to clear
        if (e.ctrlKey && e.key === 'k') {
            e.preventDefault();
            clearConversation();
        }
        // Ctrl+L to focus input
        if (e.ctrlKey && e.key === 'l') {
            e.preventDefault();
            document.getElementById('prompt').focus();
        }
    });
}

// Tab switching
function switchTab(tabName) {
    // Update tab buttons
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.tab === tabName);
    });
    
    // Update tab content
    document.querySelectorAll('.tab-content').forEach(content => {
        content.classList.toggle('active', content.id === `${tabName}-tab`);
    });
}

// Show message toast
function showMessage(text, type = 'info') {
    const msgEl = document.getElementById('message');
    if (!msgEl) return;
    
    msgEl.textContent = text;
    msgEl.className = `message message-${type}`;
    msgEl.style.display = 'block';
    
    setTimeout(() => {
        msgEl.style.display = 'none';
    }, 3000);
}

// Check connection status
async function checkConnection() {
    const statusEl = document.getElementById('connectionStatus');
    const dot = statusEl.querySelector('.status-dot');
    const text = statusEl.querySelector('.status-text');
    
    try {
        const response = await fetch(`${cfg.url}/health`);
        if (response.ok) {
            dot.className = 'status-dot connected';
            text.textContent = 'Connected';
            statusEl.className = 'status-indicator connected';
        } else {
            throw new Error('Health check failed');
        }
    } catch (error) {
        dot.className = 'status-dot disconnected';
        text.textContent = 'Disconnected';
        statusEl.className = 'status-indicator disconnected';
    }
}

// Add message to conversation
function addMessageToConversation(role, content, timestamp = null) {
    const message = {
        role,
        content,
        timestamp: timestamp || new Date().toISOString()
    };
    currentConversation.push(message);
    
    renderConversation();
    
    if (cfg.autoSave) {
        saveCurrentConversation();
    }
}

// Render conversation
function renderConversation() {
    const container = document.getElementById('conversation');
    container.innerHTML = '';
    
    if (currentConversation.length === 0) {
        container.innerHTML = '<div class="empty-conversation">Start a conversation by typing a message below...</div>';
        return;
    }
    
    currentConversation.forEach((msg, index) => {
        const msgEl = document.createElement('div');
        msgEl.className = `message-bubble ${msg.role}`;
        
        const timeStr = cfg.showTimestamps ? new Date(msg.timestamp).toLocaleTimeString() : '';
        
        msgEl.innerHTML = `
            <div class="message-header">
                <span class="message-role">${msg.role === 'user' ? '👤 You' : '🤖 Assistant'}</span>
                ${timeStr ? `<span class="message-time">${timeStr}</span>` : ''}
            </div>
            <div class="message-content">${cfg.markdownRender && msg.role === 'assistant' 
                ? renderMarkdown(msg.content) 
                : escapeHtml(msg.content)}</div>
        `;
        
        container.appendChild(msgEl);
    });
    
    // Scroll to bottom
    container.scrollTop = container.scrollHeight;
}

// Simple markdown renderer
function renderMarkdown(text) {
    let html = escapeHtml(text);
    // Code blocks
    html = html.replace(/```([\s\S]*?)```/g, '<pre><code>$1</code></pre>');
    // Inline code
    html = html.replace(/`([^`]+)`/g, '<code>$1</code>');
    // Bold
    html = html.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
    // Italic
    html = html.replace(/\*([^*]+)\*/g, '<em>$1</em>');
    // Links
    html = html.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank">$1</a>');
    // Line breaks
    html = html.replace(/\n/g, '<br>');
    return html;
}

// Escape HTML
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Set loading state
function setLoading(loading) {
    const sendBtn = document.getElementById('sendBtn');
    const promptEl = document.getElementById('prompt');
    
    if (loading) {
        sendBtn.disabled = true;
        sendBtn.querySelector('.btn-text').textContent = 'Sending...';
        promptEl.disabled = true;
    } else {
        sendBtn.disabled = false;
        sendBtn.querySelector('.btn-text').textContent = 'Send';
        promptEl.disabled = false;
    }
}

// Send request using REST API
async function sendRest() {
    const prompt = document.getElementById('prompt').value.trim();
    const model = document.getElementById('model').value;
    const systemPrompt = document.getElementById('systemPrompt').value.trim();
    
    if (!prompt) {
        showMessage('Please enter a prompt', 'error');
        return;
    }
    
    if (!cfg.url || !cfg.key) {
        showMessage('Please configure connection settings first', 'error');
        return;
    }
    
    setLoading(true);
    const startTime = Date.now();
    
    // Add user message to conversation
    addMessageToConversation('user', prompt);
    
    // Clear input
    document.getElementById('prompt').value = '';
    
    try {
        const messages = [];
        if (systemPrompt) {
            messages.push({ role: 'system', content: systemPrompt });
        }
        messages.push({ role: 'user', content: prompt });
        
        const response = await fetch(cfg.url + '/v1/chat/completions', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-API-KEY': cfg.key
            },
            body: JSON.stringify({
                model: model,
                messages: messages,
                max_tokens: cfg.maxTokens,
                temperature: cfg.temperature,
                frequency_penalty: cfg.frequencyPenalty
            })
        });
        
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({ error: 'Unknown error' }));
            throw new Error(errorData.error || `HTTP ${response.status}: ${response.statusText}`);
        }
        
        const data = await response.json();
        
        if (data.error) {
            throw new Error(data.error);
        }
        
        if (data.choices && data.choices[0] && data.choices[0].message) {
            const content = data.choices[0].message.content;
            const responseTime = (Date.now() - startTime) / 1000;
            
            // Add assistant message
            addMessageToConversation('assistant', content);
            
            // Update stats
            updateStats(responseTime, content.length);
            
            // Play sound if enabled
            if (cfg.soundEnabled) {
                playNotificationSound();
            }
        } else {
            throw new Error('Unexpected response format');
        }
        
    } catch (error) {
        const errorMsg = `Error: ${error.message}`;
        addMessageToConversation('assistant', errorMsg);
        showMessage(`Request failed: ${error.message}`, 'error');
        console.error('Request error:', error);
    } finally {
        setLoading(false);
    }
}

// Send request using WebSocket streaming
function sendWebSocket() {
    const prompt = document.getElementById('prompt').value.trim();
    const model = document.getElementById('model').value;
    const systemPrompt = document.getElementById('systemPrompt').value.trim();
    
    if (!prompt) {
        showMessage('Please enter a prompt', 'error');
        return;
    }
    
    if (!cfg.url || !cfg.key) {
        showMessage('Please configure connection settings first', 'error');
        return;
    }
    
    setLoading(true);
    const startTime = Date.now();
    
    // Add user message to conversation
    addMessageToConversation('user', prompt);
    
    // Clear input
    document.getElementById('prompt').value = '';
    
    // Create assistant message placeholder
    const assistantMsg = { role: 'assistant', content: '', timestamp: new Date().toISOString() };
    currentConversation.push(assistantMsg);
    
    // Convert HTTP URL to WebSocket URL
    const wsUrl = cfg.url.replace(/^http/, 'ws') + '/ws/chat?api_key=' + encodeURIComponent(cfg.key);
    const ws = new WebSocket(wsUrl);
    
    ws.onopen = () => {
        const messages = [];
        if (systemPrompt) {
            messages.push({ role: 'system', content: systemPrompt });
        }
        messages.push({ role: 'user', content: prompt });
        
        // Send request
        ws.send(JSON.stringify({
            model: model,
            messages: messages,
            stream: true,
            max_tokens: cfg.maxTokens,
            temperature: cfg.temperature,
            frequency_penalty: cfg.frequencyPenalty
        }));
    };
    
    ws.onmessage = (event) => {
        try {
            const text = event.data;
            const lines = text.split('\n');
            
            for (const line of lines) {
                if (line.startsWith('data: ')) {
                    const data = line.substring(6);
                    if (data === '[DONE]') {
                        ws.close();
                        setLoading(false);
                        const responseTime = (Date.now() - startTime) / 1000;
                        updateStats(responseTime, assistantMsg.content.length);
                        if (cfg.soundEnabled) playNotificationSound();
                        return;
                    }
                    
                    try {
                        const parsed = JSON.parse(data);
                        if (parsed.choices && parsed.choices[0] && parsed.choices[0].delta) {
                            const content = parsed.choices[0].delta.content || '';
                            if (content) {
                                assistantMsg.content += content;
                                renderConversation();
                            }
                        }
                    } catch (e) {
                        // Not JSON, might be plain text chunk
                        if (data.trim()) {
                            assistantMsg.content += data;
                            renderConversation();
                        }
                    }
                } else if (line.trim() && !line.startsWith(':')) {
                    assistantMsg.content += line;
                    renderConversation();
                }
            }
        } catch (error) {
            console.error('Error parsing WebSocket message:', error);
        }
    };
    
    ws.onerror = (error) => {
        assistantMsg.content = `WebSocket error: ${error.message || 'Connection failed'}`;
        renderConversation();
        showMessage('WebSocket connection failed', 'error');
        setLoading(false);
    };
    
    ws.onclose = (event) => {
        setLoading(false);
        if (event.code !== 1000 && event.code !== 1001) {
            if (!assistantMsg.content.includes('error')) {
                assistantMsg.content += `\n\n[Connection closed: ${event.code} - ${event.reason || 'Unknown reason'}]`;
                renderConversation();
            }
        }
    };
}

// Main send function (global for onclick handlers)
window.send = async function() {
    if (cfg.useStreaming) {
        sendWebSocket();
    } else {
        await sendRest();
    }
};

// Save function (global for onclick handlers)
window.save = save;

// Clear conversation
function clearConversation() {
    if (currentConversation.length === 0) return;
    
    if (confirm('Clear current conversation?')) {
        currentConversation = [];
        renderConversation();
    }
}

// Copy last response
function copyLastResponse() {
    const lastAssistant = [...currentConversation].reverse().find(m => m.role === 'assistant');
    if (lastAssistant) {
        navigator.clipboard.writeText(lastAssistant.content);
        showMessage('Response copied to clipboard!', 'success');
    } else {
        showMessage('No response to copy', 'error');
    }
}

// Export conversation
function exportConversation() {
    if (currentConversation.length === 0) {
        showMessage('No conversation to export', 'error');
        return;
    }
    
    const exportText = currentConversation.map(msg => {
        return `${msg.role.toUpperCase()} (${new Date(msg.timestamp).toLocaleString()}):\n${msg.content}\n\n`;
    }).join('');
    
    downloadText(exportText, `conversation-${Date.now()}.txt`);
}

// Load available models from API
async function loadModels() {
    const url = cfg.url || 'http://localhost:7860';
    const modelSelect = document.getElementById('model');
    const modelsList = document.getElementById('modelsList');
    
    modelSelect.innerHTML = '<option>Loading...</option>';
    if (modelsList) {
        modelsList.innerHTML = '<div class="loading">Loading models...</div>';
    }
    
    try {
        const response = await fetch(`${url}/models`);
        if (response.ok) {
            const data = await response.json();
            if (data.models && Array.isArray(data.models)) {
                // Populate select
                modelSelect.innerHTML = '';
                data.models.forEach(model => {
                    const option = document.createElement('option');
                    option.value = model.id;
                    option.textContent = model.name || model.id;
                    option.title = model.description || '';
                    modelSelect.appendChild(option);
                });
                
                // Populate models tab
                if (modelsList) {
                    modelsList.innerHTML = '';
                    data.models.forEach(model => {
                        const card = document.createElement('div');
                        card.className = 'model-card';
                        card.innerHTML = `
                            <div class="model-icon">🤖</div>
                            <div class="model-info">
                                <h4>${model.name || model.id}</h4>
                                <p class="model-id">${model.id}</p>
                                <p class="model-desc">${model.description || 'No description available'}</p>
                            </div>
                        `;
                        modelsList.appendChild(card);
                    });
                }
            }
        }
    } catch (error) {
        console.warn('Could not load models from API:', error);
        modelSelect.innerHTML = '<option value="mistral-7b-instruct">mistral-7b-instruct</option>';
        if (modelsList) {
            modelsList.innerHTML = '<div class="error">Could not load models. Check your connection.</div>';
        }
    }
}

// Load conversation history
function loadHistory() {
    const saved = localStorage.getItem('perplexity_bridge_history');
    if (saved) {
        try {
            conversationHistory = JSON.parse(saved);
            renderHistory();
        } catch (e) {
            console.error('Error loading history:', e);
        }
    }
}

// Save current conversation
function saveCurrentConversation() {
    if (currentConversation.length === 0) return;
    
    const conversation = {
        id: Date.now().toString(),
        messages: [...currentConversation],
        createdAt: new Date().toISOString()
    };
    
    conversationHistory.unshift(conversation);
    if (conversationHistory.length > 100) {
        conversationHistory = conversationHistory.slice(0, 100);
    }
    
    localStorage.setItem('perplexity_bridge_history', JSON.stringify(conversationHistory));
    renderHistory();
}

// Render history
function renderHistory() {
    const container = document.getElementById('historyList');
    if (!container) return;
    
    if (conversationHistory.length === 0) {
        container.innerHTML = '<div class="empty-state">No conversations yet. Start chatting to see history here.</div>';
        return;
    }
    
    container.innerHTML = '';
    conversationHistory.forEach(conv => {
        const item = document.createElement('div');
        item.className = 'history-item';
        const firstMsg = conv.messages[0]?.content.substring(0, 100) || 'Empty conversation';
        item.innerHTML = `
            <div class="history-preview">${escapeHtml(firstMsg)}...</div>
            <div class="history-meta">
                <span>${conv.messages.length} messages</span>
                <span>•</span>
                <span>${new Date(conv.createdAt).toLocaleString()}</span>
            </div>
            <div class="history-actions">
                <button onclick="loadConversation('${conv.id}')" class="btn-sm">Load</button>
                <button onclick="deleteConversation('${conv.id}')" class="btn-sm btn-danger">Delete</button>
            </div>
        `;
        container.appendChild(item);
    });
}

// Load conversation from history (global for onclick handlers)
window.loadConversation = function(id) {
    const conv = conversationHistory.find(c => c.id === id);
    if (conv) {
        currentConversation = [...conv.messages];
        renderConversation();
        switchTab('chat');
        showMessage('Conversation loaded!', 'success');
    }
};

// Delete conversation from history (global for onclick handlers)
window.deleteConversation = function(id) {
    conversationHistory = conversationHistory.filter(c => c.id !== id);
    localStorage.setItem('perplexity_bridge_history', JSON.stringify(conversationHistory));
    renderHistory();
    showMessage('Conversation deleted', 'success');
};

// Clear all history
function clearAllHistory() {
    if (confirm('Delete all conversation history?')) {
        conversationHistory = [];
        localStorage.removeItem('perplexity_bridge_history');
        renderHistory();
        showMessage('All history cleared', 'success');
    }
}

// Export all history
function exportAllHistory() {
    if (conversationHistory.length === 0) {
        showMessage('No history to export', 'error');
        return;
    }
    
    const exportText = conversationHistory.map((conv, idx) => {
        return `=== Conversation ${idx + 1} (${new Date(conv.createdAt).toLocaleString()}) ===\n\n` +
            conv.messages.map(msg => {
                return `${msg.role.toUpperCase()}: ${msg.content}\n\n`;
            }).join('') + '\n\n';
    }).join('---\n\n');
    
    downloadText(exportText, `all-conversations-${Date.now()}.txt`);
}

// Download text as file
function downloadText(text, filename) {
    const blob = new Blob([text], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    a.click();
    URL.revokeObjectURL(url);
}

// Update statistics
function updateStats(responseTime, contentLength) {
    stats.totalRequests++;
    stats.totalMessages += 2; // User + Assistant
    stats.totalTokens += Math.ceil(contentLength / 4); // Rough estimate: 1 token ≈ 4 chars
    stats.totalTime += responseTime;
    
    stats.activities.unshift({
        time: new Date().toISOString(),
        responseTime: responseTime.toFixed(2) + 's',
        tokens: Math.ceil(contentLength / 4)
    });
    
    if (stats.activities.length > 50) {
        stats.activities = stats.activities.slice(0, 50);
    }
    
    saveStats();
    updateStatsDisplay();
}

// Load statistics
function loadStats() {
    const saved = localStorage.getItem('perplexity_bridge_stats');
    if (saved) {
        try {
            stats = JSON.parse(saved);
            updateStatsDisplay();
        } catch (e) {
            console.error('Error loading stats:', e);
        }
    }
}

// Save statistics
function saveStats() {
    localStorage.setItem('perplexity_bridge_stats', JSON.stringify(stats));
}

// Update stats display
function updateStatsDisplay() {
    document.getElementById('totalRequests').textContent = stats.totalRequests;
    document.getElementById('totalMessages').textContent = stats.totalMessages;
    document.getElementById('totalTokens').textContent = stats.totalTokens.toLocaleString();
    document.getElementById('totalTime').textContent = stats.totalTime.toFixed(1) + 's';
    
    // Update activity log
    const log = document.getElementById('activityLog');
    if (log) {
        if (stats.activities.length === 0) {
            log.innerHTML = '<div class="empty-state">No activity yet</div>';
        } else {
            log.innerHTML = stats.activities.map(activity => {
                return `<div class="activity-item">
                    <span class="activity-time">${new Date(activity.time).toLocaleTimeString()}</span>
                    <span class="activity-details">${activity.responseTime} • ${activity.tokens} tokens</span>
                </div>`;
            }).join('');
        }
    }
}

// Update UI based on configuration
function updateUI() {
    // Reload models when URL changes
    document.getElementById('url').addEventListener('change', () => {
        cfg.url = document.getElementById('url').value.trim();
        checkConnection();
        loadModels();
    });
}

// Toggle theme (placeholder - can be enhanced)
function toggleTheme() {
    document.body.classList.toggle('light-theme');
    const isLight = document.body.classList.contains('light-theme');
    localStorage.setItem('perplexity_bridge_theme', isLight ? 'light' : 'dark');
    document.getElementById('themeToggle').textContent = isLight ? '🌙' : '☀️';
}

// Play notification sound
function playNotificationSound() {
    // Simple beep using Web Audio API
    const audioContext = new (window.AudioContext || window.webkitAudioContext)();
    const oscillator = audioContext.createOscillator();
    const gainNode = audioContext.createGain();
    
    oscillator.connect(gainNode);
    gainNode.connect(audioContext.destination);
    
    oscillator.frequency.value = 800;
    oscillator.type = 'sine';
    
    gainNode.gain.setValueAtTime(0.3, audioContext.currentTime);
    gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.1);
    
    oscillator.start(audioContext.currentTime);
    oscillator.stop(audioContext.currentTime + 0.1);
}

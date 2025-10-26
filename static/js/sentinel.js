// Sentinel Dashboard - Real-time JavaScript Controller

// State
let currentStatus = 'idle';
let eventSource = null;
let sessionStartTime = null;
let timerInterval = null;

// DOM Elements
const liveTradingToggle = document.getElementById('liveTradingToggle');
const devRerunsToggle = document.getElementById('devRerunsToggle');
const startBtn = document.getElementById('startBtn');
const stopBtn = document.getElementById('stopBtn');
const approveBtn = document.getElementById('approveBtn');
const denyBtn = document.getElementById('denyBtn');
const reusePlanBtn = document.getElementById('reusePlanBtn');
const regeneratePlanBtn = document.getElementById('regeneratePlanBtn');
const clearTerminalBtn = document.getElementById('clearTerminalBtn');
const terminal = document.getElementById('terminal');
const statusIndicator = document.getElementById('statusIndicator');
const statusDot = statusIndicator.querySelector('.status-dot');
const statusText = statusIndicator.querySelector('.status-text');
const approvalPanel = document.getElementById('approvalPanel');
const approvalContent = document.getElementById('approvalContent');
const planDecisionPanel = document.getElementById('planDecisionPanel');
const planDecisionContent = document.getElementById('planDecisionContent');
const tradingMode = document.getElementById('tradingMode');
const sessionTime = document.getElementById('sessionTime');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    loadConfig();
    updateTradingModeDisplay();

    // Event listeners
    startBtn.addEventListener('click', handleStart);
    stopBtn.addEventListener('click', handleStop);
    approveBtn.addEventListener('click', handleApprove);
    denyBtn.addEventListener('click', handleDeny);
    reusePlanBtn.addEventListener('click', handleReusePlan);
    regeneratePlanBtn.addEventListener('click', handleRegeneratePlan);
    clearTerminalBtn.addEventListener('click', clearTerminal);
    liveTradingToggle.addEventListener('change', updateTradingModeDisplay);

    // Start polling for status
    startStatusPolling();

    addTerminalLine('[DASHBOARD] Dashboard initialized and ready.', 'success');
});

// Load current configuration from server
async function loadConfig() {
    try {
        const response = await fetch('/api/config');
        const config = await response.json();

        liveTradingToggle.checked = config.LIVE_TRADING;
        devRerunsToggle.checked = config.ALLOW_DEV_RERUNS;
        updateTradingModeDisplay();
    } catch (error) {
        console.error('Failed to load config:', error);
        addTerminalLine('[ERROR] Failed to load configuration', 'error');
    }
}

// Update trading mode display
function updateTradingModeDisplay() {
    if (liveTradingToggle.checked) {
        tradingMode.textContent = 'LIVE TRADING';
        tradingMode.style.color = 'var(--warning)';
    } else {
        tradingMode.textContent = 'SAFE MODE';
        tradingMode.style.color = 'var(--success)';
    }
}

// Handle Start button
async function handleStart() {
    try {
        startBtn.disabled = true;

        const config = {
            LIVE_TRADING: liveTradingToggle.checked,
            ALLOW_DEV_RERUNS: devRerunsToggle.checked
        };

        const response = await fetch('/api/start', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(config)
        });

        const result = await response.json();

        if (response.ok) {
            addTerminalLine(`[DASHBOARD] Starting Sentinel...`, 'success');
            addTerminalLine(`[CONFIG] LIVE_TRADING = ${config.LIVE_TRADING}`, 'info');
            addTerminalLine(`[CONFIG] ALLOW_DEV_RERUNS = ${config.ALLOW_DEV_RERUNS}`, 'info');

            stopBtn.disabled = false;
            sessionStartTime = Date.now();
            startSessionTimer();

            // Start event stream
            startEventStream();
        } else {
            addTerminalLine(`[ERROR] ${result.error}`, 'error');
            startBtn.disabled = false;
        }
    } catch (error) {
        console.error('Start error:', error);
        addTerminalLine(`[ERROR] Failed to start: ${error.message}`, 'error');
        startBtn.disabled = false;
    }
}

// Handle Stop button
async function handleStop() {
    try {
        const response = await fetch('/api/stop', {
            method: 'POST'
        });

        const result = await response.json();

        if (response.ok) {
            addTerminalLine('[DASHBOARD] Abort requested - waiting for safe stop point...', 'warning');
            stopBtn.disabled = true;
        } else {
            addTerminalLine(`[ERROR] ${result.error}`, 'error');
        }
    } catch (error) {
        console.error('Stop error:', error);
        addTerminalLine(`[ERROR] Failed to stop: ${error.message}`, 'error');
    }
}

// Handle Approve button
async function handleApprove() {
    try {
        const response = await fetch('/api/approve', {
            method: 'POST'
        });

        const result = await response.json();

        if (response.ok) {
            addTerminalLine('[USER] Trade plan APPROVED', 'success');
            approvalPanel.style.display = 'none';
        } else {
            addTerminalLine(`[ERROR] ${result.error}`, 'error');
        }
    } catch (error) {
        console.error('Approve error:', error);
        addTerminalLine(`[ERROR] Failed to approve: ${error.message}`, 'error');
    }
}

// Handle Deny button
async function handleDeny() {
    try {
        const response = await fetch('/api/deny', {
            method: 'POST'
        });

        const result = await response.json();

        if (response.ok) {
            addTerminalLine('[USER] Trade plan DENIED', 'warning');
            approvalPanel.style.display = 'none';
        } else {
            addTerminalLine(`[ERROR] ${result.error}`, 'error');
        }
    } catch (error) {
        console.error('Deny error:', error);
        addTerminalLine(`[ERROR] Failed to deny: ${error.message}`, 'error');
    }
}

// Handle Reuse Plan button
async function handleReusePlan() {
    try {
        const response = await fetch('/api/reuse_plan', {
            method: 'POST'
        });

        const result = await response.json();

        if (response.ok) {
            addTerminalLine('[USER] Reusing existing plan', 'success');
            planDecisionPanel.style.display = 'none';
        } else {
            addTerminalLine(`[ERROR] ${result.error}`, 'error');
        }
    } catch (error) {
        console.error('Reuse plan error:', error);
        addTerminalLine(`[ERROR] Failed to reuse plan: ${error.message}`, 'error');
    }
}

// Handle Regenerate Plan button
async function handleRegeneratePlan() {
    try {
        const response = await fetch('/api/regenerate_plan', {
            method: 'POST'
        });

        const result = await response.json();

        if (response.ok) {
            addTerminalLine('[USER] Regenerating plan from scratch...', 'warning');
            planDecisionPanel.style.display = 'none';
        } else {
            addTerminalLine(`[ERROR] ${result.error}`, 'error');
        }
    } catch (error) {
        console.error('Regenerate plan error:', error);
        addTerminalLine(`[ERROR] Failed to regenerate plan: ${error.message}`, 'error');
    }
}

// Clear terminal
function clearTerminal() {
    terminal.innerHTML = '';
    addTerminalLine('[DASHBOARD] Terminal cleared', 'info');
}

// Add line to terminal
function addTerminalLine(text, type = 'info') {
    const line = document.createElement('div');
    line.className = `terminal-line terminal-${type}`;

    const timestamp = new Date().toLocaleTimeString();
    line.innerHTML = `<span class="terminal-prompt">[${timestamp}]</span><span>${escapeHtml(text)}</span>`;

    terminal.appendChild(line);
    terminal.scrollTop = terminal.scrollHeight;
}

// Escape HTML to prevent XSS
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Start Server-Sent Events stream
function startEventStream() {
    if (eventSource) {
        eventSource.close();
    }

    eventSource = new EventSource('/api/stream');

    eventSource.onmessage = (event) => {
        const data = JSON.parse(event.data);

        if (data.type === 'terminal') {
            addTerminalLine(data.data, 'info');
        } else if (data.type === 'status') {
            updateStatus(data.status);
        }
    };

    eventSource.onerror = (error) => {
        console.error('EventSource error:', error);
        eventSource.close();

        // Retry after 5 seconds if still running
        if (currentStatus === 'running' || currentStatus === 'waiting_approval') {
            setTimeout(startEventStream, 5000);
        }
    };
}

// Poll for status updates (fallback)
function startStatusPolling() {
    setInterval(async () => {
        try {
            const response = await fetch('/api/status');
            const data = await response.json();

            updateStatus(data.status);

            // Update approval panel if plan is present
            if (data.plan) {
                showApprovalPanel(data.plan);
            }
        } catch (error) {
            console.error('Status polling error:', error);
        }
    }, 2000);  // Poll every 2 seconds
}

// Update status indicator
function updateStatus(status) {
    if (status === currentStatus) return;

    currentStatus = status;

    // Update status dot and text
    statusDot.className = `status-dot ${status}`;
    statusText.textContent = status.toUpperCase().replace('_', ' ');

    // Update button states
    switch (status) {
        case 'idle':
            startBtn.disabled = false;
            stopBtn.disabled = true;
            approvalPanel.style.display = 'none';
            planDecisionPanel.style.display = 'none';
            stopSessionTimer();
            break;

        case 'running':
            startBtn.disabled = true;
            stopBtn.disabled = false;
            approvalPanel.style.display = 'none';
            planDecisionPanel.style.display = 'none';
            break;

        case 'waiting_plan_decision':
            startBtn.disabled = true;
            stopBtn.disabled = false;
            approvalPanel.style.display = 'none';
            planDecisionPanel.style.display = 'block';
            break;

        case 'waiting_approval':
            startBtn.disabled = true;
            stopBtn.disabled = false;
            approvalPanel.style.display = 'block';
            planDecisionPanel.style.display = 'none';
            break;

        case 'completed':
        case 'aborted':
        case 'failed':
            startBtn.disabled = false;
            stopBtn.disabled = true;
            approvalPanel.style.display = 'none';
            planDecisionPanel.style.display = 'none';
            stopSessionTimer();

            if (eventSource) {
                eventSource.close();
                eventSource = null;
            }
            break;
    }
}

// Show approval panel with plan details
function showApprovalPanel(plan) {
    approvalPanel.style.display = 'block';

    let html = '<pre style="margin: 0; white-space: pre-wrap;">';
    html += JSON.stringify(plan, null, 2);
    html += '</pre>';

    approvalContent.innerHTML = html;
}

// Session timer
function startSessionTimer() {
    if (timerInterval) {
        clearInterval(timerInterval);
    }

    timerInterval = setInterval(() => {
        if (sessionStartTime) {
            const elapsed = Date.now() - sessionStartTime;
            const hours = Math.floor(elapsed / 3600000);
            const minutes = Math.floor((elapsed % 3600000) / 60000);
            const seconds = Math.floor((elapsed % 60000) / 1000);

            sessionTime.textContent =
                `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
        }
    }, 1000);
}

function stopSessionTimer() {
    if (timerInterval) {
        clearInterval(timerInterval);
        timerInterval = null;
    }
    sessionStartTime = null;
    sessionTime.textContent = '--:--:--';
}

// Log unhandled errors to terminal
window.addEventListener('error', (event) => {
    addTerminalLine(`[JS ERROR] ${event.message}`, 'error');
});

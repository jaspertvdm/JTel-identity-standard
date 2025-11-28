// Configuration
const API_BASE = window.location.origin;
const AUTH_SECRET = prompt('Enter JIS_SHARED_SECRET to access admin panel:');

// API Helper
async function apiCall(endpoint, options = {}) {
    try {
        const response = await fetch(`${API_BASE}${endpoint}`, {
            ...options,
            headers: {
                'X-JIS-SECRET': AUTH_SECRET,
                'Content-Type': 'application/json',
                ...options.headers,
            },
        });

        if (!response.ok) {
            if (response.status === 401) {
                alert('Authentication failed. Please reload and enter correct secret.');
                throw new Error('Unauthorized');
            }
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }

        return await response.json();
    } catch (error) {
        console.error('API call failed:', error);
        throw error;
    }
}

// Tab Management
function initTabs() {
    const tabs = document.querySelectorAll('.tab-btn');
    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            const targetTab = tab.dataset.tab;

            // Update active tab button
            tabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');

            // Update active content
            document.querySelectorAll('.tab-content').forEach(content => {
                content.classList.remove('active');
            });
            document.getElementById(targetTab).classList.add('active');

            // Load data for the tab
            if (targetTab === 'relationships') {
                loadRelationships();
            } else if (targetTab === 'health') {
                loadHealth();
            } else if (targetTab === 'overview') {
                loadOverview();
            }
        });
    });
}

// Overview Tab
async function loadOverview() {
    try {
        // Load metrics
        const metrics = await apiCall('/metrics');
        document.getElementById('total-relationships').textContent =
            metrics.total_relationships?.toLocaleString() || '0';
        document.getElementById('total-events').textContent =
            metrics.total_events?.toLocaleString() || '0';
        document.getElementById('redis-commands').textContent =
            metrics.redis_total_commands?.toLocaleString() || '0';

        // Load health status
        const health = await apiCall('/health/ready');
        const statusEl = document.getElementById('router-status');
        statusEl.textContent = health.status === 'ready' ? '✓ Ready' : '✗ Not Ready';
        statusEl.className = `metric-value status ${health.status === 'ready' ? 'ready' : 'not-ready'}`;

        // Load recent activity
        const relationships = await apiCall('/admin/relationships?limit=10');
        const activityEl = document.getElementById('recent-activity');

        if (relationships.relationships.length === 0) {
            activityEl.innerHTML = '<p class="loading">No relationships yet.</p>';
        } else {
            activityEl.innerHTML = relationships.relationships.map(rel => `
                <div class="activity-item">
                    <h4>FIR/A: ${rel.fir_a_id}</h4>
                    <p>Events: ${rel.last_event_seq} | Last update: ${formatDate(rel.last_update)}</p>
                    <p class="hash-short">Hash: ${rel.continuity_hash.substring(0, 16)}...</p>
                </div>
            `).join('');
        }
    } catch (error) {
        console.error('Failed to load overview:', error);
    }
}

// Relationships Tab
async function loadRelationships() {
    const tbody = document.getElementById('relationships-tbody');
    tbody.innerHTML = '<tr><td colspan="5" class="loading">Loading...</td></tr>';

    try {
        const data = await apiCall('/admin/relationships?limit=100');

        if (data.relationships.length === 0) {
            tbody.innerHTML = '<tr><td colspan="5" class="loading">No relationships found.</td></tr>';
            return;
        }

        tbody.innerHTML = data.relationships.map(rel => `
            <tr>
                <td><code>${rel.fir_a_id}</code></td>
                <td>${rel.last_event_seq}</td>
                <td><span class="hash-short">${rel.continuity_hash.substring(0, 16)}...</span></td>
                <td>${formatDate(rel.last_update)}</td>
                <td>
                    <button class="btn-view" onclick="viewEvents('${rel.fir_a_id}')">
                        View Events
                    </button>
                </td>
            </tr>
        `).join('');
    } catch (error) {
        tbody.innerHTML = `<tr><td colspan="5" class="loading">Error: ${error.message}</td></tr>`;
    }
}

// Health Tab
async function loadHealth() {
    try {
        const health = await apiCall('/health/ready');

        // Update Postgres health
        const pgCard = document.querySelector('#postgres-health .health-status');
        const pgStatus = health.checks.postgres;
        pgCard.textContent = pgStatus === 'ok' ? '✓ Connected' : `✗ ${pgStatus}`;
        pgCard.className = `health-status ${pgStatus === 'ok' ? 'ok' : 'error'}`;

        // Update Redis health
        const redisCard = document.querySelector('#redis-health .health-status');
        const redisStatus = health.checks.redis;
        redisCard.textContent = redisStatus === 'ok' ? '✓ Connected' : `✗ ${redisStatus}`;
        redisCard.className = `health-status ${redisStatus === 'ok' ? 'ok' : 'error'}`;

        // Update JSON display
        document.getElementById('readiness-json').textContent =
            JSON.stringify(health, null, 2);
    } catch (error) {
        console.error('Failed to load health:', error);
    }
}

// Event Modal
async function viewEvents(firAId) {
    const modal = document.getElementById('event-modal');
    const detail = document.getElementById('event-detail');

    modal.classList.add('active');
    detail.innerHTML = '<p class="loading">Loading events...</p>';

    try {
        const data = await apiCall(`/relation/${firAId}/events?limit=20`);

        detail.innerHTML = `
            <div style="margin-bottom: 1rem;">
                <strong>FIR/A ID:</strong> <code>${firAId}</code><br>
                <strong>Total Events:</strong> ${data.events.length}
            </div>
            ${data.events.map((event, idx) => `
                <div class="event-item">
                    <h4>Event #${event.seq} - ${formatDate(event.timestamp)}</h4>
                    <p><strong>Hash:</strong> <code style="font-size: 0.7rem;">${event.continuity_hash}</code></p>
                    <pre>${JSON.stringify(event.payload, null, 2)}</pre>
                </div>
            `).join('')}
        `;
    } catch (error) {
        detail.innerHTML = `<p class="loading">Error: ${error.message}</p>`;
    }
}

function closeModal() {
    document.getElementById('event-modal').classList.remove('active');
}

// Search functionality
function initSearch() {
    const searchInput = document.getElementById('search-fira');
    searchInput.addEventListener('input', (e) => {
        const query = e.target.value.toLowerCase();
        const rows = document.querySelectorAll('#relationships-tbody tr');

        rows.forEach(row => {
            const firAId = row.querySelector('code')?.textContent.toLowerCase() || '';
            row.style.display = firAId.includes(query) ? '' : 'none';
        });
    });
}

// Utility functions
function formatDate(isoString) {
    if (!isoString) return 'N/A';
    const date = new Date(isoString);
    return date.toLocaleString('nl-NL', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// Close modal on outside click
window.addEventListener('click', (e) => {
    const modal = document.getElementById('event-modal');
    if (e.target === modal) {
        closeModal();
    }
});

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    if (!AUTH_SECRET) {
        alert('Authentication required to access admin panel.');
        return;
    }

    initTabs();
    initSearch();
    loadOverview();

    // Auto-refresh overview every 30 seconds
    setInterval(() => {
        if (document.querySelector('.tab-btn.active').dataset.tab === 'overview') {
            loadOverview();
        }
    }, 30000);
});

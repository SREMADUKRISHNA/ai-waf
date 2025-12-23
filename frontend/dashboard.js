let attackChart = null;

async function fetchStats() {
    try {
        const response = await fetch('/api/dashboard/stats');
        const data = await response.json();
        
        // Update Total
        document.getElementById('total-blocked').innerText = data.total_blocked;
        
        // Update Chart
        updateChart(data.attack_distribution);
        
        // Update Table
        updateTable(data.recent_attacks);
        
    } catch (error) {
        console.error("Error fetching stats:", error);
    }
}

function updateChart(distribution) {
    const ctx = document.getElementById('attackChart').getContext('2d');
    const labels = Object.keys(distribution);
    const values = Object.values(distribution);
    
    if (attackChart) {
        attackChart.destroy();
    }
    
    attackChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: values,
                backgroundColor: [
                    '#ff5252', // SQLi
                    '#ffab40', // XSS
                    '#448aff', // CSRF
                    '#e040fb', // LFI
                    '#69f0ae'  // Anomaly
                ],
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { position: 'right', labels: { color: '#fff' } }
            }
        }
    });
}

function updateTable(attacks) {
    const tbody = document.getElementById('logs-body');
    tbody.innerHTML = '';
    
    if (attacks.length === 0) {
        tbody.innerHTML = '<tr><td colspan="6" class="text-center">No attacks detected yet.</td></tr>';
        return;
    }
    
    attacks.forEach(attack => {
        const date = new Date(attack.timestamp * 1000).toLocaleTimeString();
        let badgeClass = 'secondary';
        if (attack.attack_type === 'SQLi') badgeClass = 'sqli';
        if (attack.attack_type === 'XSS') badgeClass = 'xss';
        if (attack.attack_type === 'CSRF') badgeClass = 'csrf';
        if (attack.attack_type === 'LFI') badgeClass = 'lfi';
        if (attack.attack_type === 'Anomaly') badgeClass = 'anomaly';

        const row = `
            <tr>
                <td>${date}</td>
                <td>${attack.ip}</td>
                <td><span class="badge badge-${badgeClass}" style="padding: 5px 10px; border-radius: 4px;">${attack.attack_type}</span></td>
                <td>${attack.severity}/10</td>
                <td style="font-family: monospace; color: #ff8a80;">${escapeHtml(attack.payload)}</td>
                <td style="font-size: 0.9em; color: #b0bec5;">${attack.explanation}</td>
            </tr>
        `;
        tbody.innerHTML += row;
    });
}

function escapeHtml(text) {
    if (!text) return "";
    return text
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

// Poll every 3 seconds
setInterval(fetchStats, 3000);
fetchStats();

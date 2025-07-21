<template>
  <div class="dashboard">
    <!-- Header Section -->
    <div class="dashboard-header">
      <div class="welcome-section">
        <h1>Welcome to Stremio Manager</h1>
        <p class="subtitle">Manage your streaming addons and monitor usage</p>
      </div>
      <div class="quick-stats">
        <div class="quick-stat">
          <div class="stat-icon">👥</div>
          <div class="stat-info">
            <span class="stat-number">{{ stats?.total_users || 0 }}</span>
            <span class="stat-label">Users</span>
          </div>
        </div>
        <div class="quick-stat">
          <div class="stat-icon">🔗</div>
          <div class="stat-info">
            <span class="stat-number">{{ stats?.total_addon_usage || 0 }}</span>
            <span class="stat-label">Addon Installs</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Loading and Error States -->
    <div v-if="loading" class="loading-state">
      <div class="spinner"></div>
      <p>Loading dashboard...</p>
    </div>
    
    <div v-if="error" class="error-state">
      <div class="error-icon">⚠️</div>
      <p>{{ error }}</p>
      <button @click="fetchStats" class="retry-btn">Retry</button>
    </div>

    <!-- Main Dashboard Content -->
    <div v-if="!loading && !error" class="dashboard-content">
      <!-- Quick Actions Section -->
      <section class="quick-actions">
        <h2>Quick Actions</h2>
        <div class="action-cards">
          <div class="action-card" @click="getAddonUrl('torrentio')">
            <div class="action-icon">🎬</div>
            <h3>Get Torrentio URL</h3>
            <p>Generate your personalized Torrentio addon link</p>
            <button class="action-btn">Generate URL</button>
          </div>
          <div class="action-card" @click="getAddonUrl('aiostreams')">
            <div class="action-icon">🌊</div>
            <h3>Get AIOStreams URL</h3>
            <p>Access the complete streaming addon suite</p>
            <button class="action-btn">Generate URL</button>
          </div>
          <div class="action-card">
            <div class="action-icon">📊</div>
            <h3>View Analytics</h3>
            <p>Monitor usage patterns and statistics</p>
            <button class="action-btn" @click="scrollToAnalytics">View Charts</button>
          </div>
        </div>
      </section>

      <!-- Generated URLs Section -->
      <section v-if="generatedUrls.length > 0" class="generated-urls">
        <h2>Your Addon URLs</h2>
        <div class="url-cards">
          <div v-for="urlData in generatedUrls" :key="urlData.type" class="url-card">
            <div class="url-header">
              <h3>{{ urlData.name }}</h3>
              <span class="url-type">{{ urlData.type }}</span>
            </div>
            <div class="url-content">
              <code class="url-display">{{ urlData.url }}</code>
              <div class="url-actions">
                <button @click="copyToClipboard(urlData.url)" class="copy-btn">
                  {{ urlData.copied ? '✓ Copied!' : '📋 Copy' }}
                </button>
                <a :href="urlData.url" class="install-btn">🚀 Install in Stremio</a>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Analytics Section -->
      <section ref="analyticsSection" class="analytics" v-if="stats">
        <h2>Usage Analytics</h2>
        <div class="analytics-grid">
          <div class="chart-card">
            <h3>📈 Usage Trend (Last 30 Days)</h3>
            <div class="chart-container">
              <Line :data="usageByDayData" :options="lineChartOptions" />
            </div>
          </div>
          <div class="chart-card">
            <h3>👑 Most Active Users</h3>
            <div class="chart-container">
              <Bar :data="mostActiveUsersData" :options="barChartOptions" />
            </div>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';
import { Line, Bar } from 'vue-chartjs';
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Filler,
} from 'chart.js';

ChartJS.register(
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Filler
);

const stats = ref(null);
const loading = ref(true);
const error = ref(null);
const generatedUrls = ref([]);
const analyticsSection = ref(null);

// Enhanced chart options
const lineChartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      display: false,
    },
    tooltip: {
      mode: 'index',
      intersect: false,
    },
  },
  scales: {
    x: {
      display: true,
      grid: {
        display: false,
      },
    },
    y: {
      display: true,
      beginAtZero: true,
      grid: {
        color: 'rgba(0, 0, 0, 0.1)',
      },
    },
  },
};

const barChartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      display: false,
    },
  },
  scales: {
    x: {
      grid: {
        display: false,
      },
    },
    y: {
      beginAtZero: true,
      grid: {
        color: 'rgba(0, 0, 0, 0.1)',
      },
    },
  },
};

const usageByDayData = computed(() => ({
  labels: stats.value?.usage_by_day.map(d => new Date(d.date).toLocaleDateString()).reverse() || [],
  datasets: [
    {
      label: 'Daily Usage',
      backgroundColor: 'rgba(66, 185, 131, 0.2)',
      borderColor: '#42b983',
      borderWidth: 2,
      fill: true,
      tension: 0.4,
      data: stats.value?.usage_by_day.map(d => d.count).reverse() || [],
    },
  ],
}));

const mostActiveUsersData = computed(() => ({
  labels: stats.value?.most_active_users.map(u => u.email.split('@')[0]) || [],
  datasets: [
    {
      label: 'Addon Installs',
      backgroundColor: [
        '#42b983',
        '#f87979',
        '#4fc3f7',
        '#ffb74d',
        '#9575cd',
      ],
      borderWidth: 0,
      data: stats.value?.most_active_users.map(u => u.count) || [],
    },
  ],
}));

// Fetch stats function
const fetchStats = async () => {
  loading.value = true;
  error.value = null;
  try {
    const token = localStorage.getItem('accessToken');
    if (!token) {
      throw new Error('No access token found. Please log in.');
    }
    const response = await axios.get('/api/v1/analytics/stats', {
      headers: { Authorization: `Bearer ${token}` },
    });
    stats.value = response.data;
  } catch (err) {
    error.value = err.response?.data?.detail || err.message || 'Failed to fetch stats.';
  } finally {
    loading.value = false;
  }
};

// Generate addon URLs
const getAddonUrl = async (type) => {
  try {
    const token = localStorage.getItem('accessToken');
    if (!token) {
      throw new Error('No access token found. Please log in.');
    }
    
    let endpoint, name;
    if (type === 'torrentio') {
      endpoint = '/api/v1/addons/torrentio/installation-url';
      name = 'Torrentio';
    } else if (type === 'aiostreams') {
      endpoint = '/api/v1/addons/aiostreams/installation-url';
      name = 'AIOStreams';
    }
    
    const response = await axios.get(endpoint, {
      headers: { Authorization: `Bearer ${token}` },
    });
    
    const urlData = {
      type,
      name,
      url: response.data.installation_url,
      copied: false,
    };
    
    // Remove existing URL of same type and add new one
    generatedUrls.value = generatedUrls.value.filter(u => u.type !== type);
    generatedUrls.value.push(urlData);
    
  } catch (err) {
    error.value = err.response?.data?.detail || err.message || 'Failed to generate URL.';
  }
};

// Copy to clipboard
const copyToClipboard = async (url) => {
  try {
    await navigator.clipboard.writeText(url);
    const urlData = generatedUrls.value.find(u => u.url === url);
    if (urlData) {
      urlData.copied = true;
      setTimeout(() => {
        urlData.copied = false;
      }, 2000);
    }
  } catch (err) {
    console.error('Failed to copy to clipboard:', err);
  }
};

// Scroll to analytics section
const scrollToAnalytics = () => {
  if (analyticsSection.value) {
    analyticsSection.value.scrollIntoView({ behavior: 'smooth' });
  }
};

onMounted(() => {
  fetchStats();
});
</script>

<style scoped>
.dashboard {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  min-height: 100vh;
  color: #333;
}

/* Header Section */
.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 3rem;
  padding: 2rem;
  background: rgba(255, 255, 255, 0.95);
  border-radius: 20px;
  backdrop-filter: blur(10px);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.welcome-section h1 {
  margin: 0;
  font-size: 2.5rem;
  font-weight: 700;
  background: linear-gradient(135deg, #667eea, #764ba2);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.subtitle {
  margin: 0.5rem 0 0 0;
  color: #666;
  font-size: 1.1rem;
}

.quick-stats {
  display: flex;
  gap: 2rem;
}

.quick-stat {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem 1.5rem;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 15px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.stat-icon {
  font-size: 2rem;
}

.stat-info {
  display: flex;
  flex-direction: column;
}

.stat-number {
  font-size: 1.8rem;
  font-weight: 700;
  color: #333;
}

.stat-label {
  font-size: 0.9rem;
  color: #666;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

/* Loading and Error States */
.loading-state, .error-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem;
  background: rgba(255, 255, 255, 0.95);
  border-radius: 20px;
  text-align: center;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #667eea;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.retry-btn {
  padding: 0.75rem 1.5rem;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s ease;
}

.retry-btn:hover {
  background: #5a67d8;
  transform: translateY(-2px);
}

/* Dashboard Content */
.dashboard-content {
  display: flex;
  flex-direction: column;
  gap: 3rem;
}

/* Quick Actions */
.quick-actions h2, .generated-urls h2, .analytics h2 {
  color: white;
  font-size: 1.8rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.action-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
}

.action-card {
  background: rgba(255, 255, 255, 0.95);
  padding: 2rem;
  border-radius: 20px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(10px);
}

.action-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 40px rgba(0, 0, 0, 0.2);
}

.action-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.action-card h3 {
  margin: 0 0 1rem 0;
  font-size: 1.3rem;
  font-weight: 600;
  color: #333;
}

.action-card p {
  margin: 0 0 1.5rem 0;
  color: #666;
  line-height: 1.5;
}

.action-btn {
  padding: 0.75rem 2rem;
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  border: none;
  border-radius: 25px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
}

.action-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6);
}

/* Generated URLs */
.url-cards {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.url-card {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 20px;
  padding: 2rem;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(10px);
}

.url-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.url-header h3 {
  margin: 0;
  font-size: 1.3rem;
  font-weight: 600;
  color: #333;
}

.url-type {
  padding: 0.25rem 0.75rem;
  background: #667eea;
  color: white;
  border-radius: 15px;
  font-size: 0.8rem;
  font-weight: 600;
  text-transform: uppercase;
}

.url-display {
  display: block;
  width: 100%;
  padding: 1rem;
  background: #f8f9fa;
  border: 2px solid #e9ecef;
  border-radius: 10px;
  font-family: 'Monaco', 'Menlo', monospace;
  font-size: 0.9rem;
  word-break: break-all;
  margin-bottom: 1rem;
}

.url-actions {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.copy-btn, .install-btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.3s ease;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
}

.copy-btn {
  background: #28a745;
  color: white;
}

.copy-btn:hover {
  background: #218838;
  transform: translateY(-2px);
}

.install-btn {
  background: #007bff;
  color: white;
}

.install-btn:hover {
  background: #0056b3;
  transform: translateY(-2px);
}

/* Analytics */
.analytics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 2rem;
}

.chart-card {
  background: rgba(255, 255, 255, 0.95);
  padding: 2rem;
  border-radius: 20px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(10px);
}

.chart-card h3 {
  margin: 0 0 1.5rem 0;
  font-size: 1.2rem;
  font-weight: 600;
  color: #333;
}

.chart-container {
  height: 300px;
  position: relative;
}

/* Responsive Design */
@media (max-width: 768px) {
  .dashboard {
    padding: 1rem;
  }
  
  .dashboard-header {
    flex-direction: column;
    gap: 2rem;
    text-align: center;
  }
  
  .quick-stats {
    flex-direction: column;
    gap: 1rem;
  }
  
  .welcome-section h1 {
    font-size: 2rem;
  }
  
  .action-cards {
    grid-template-columns: 1fr;
  }
  
  .analytics-grid {
    grid-template-columns: 1fr;
  }
  
  .url-actions {
    flex-direction: column;
  }
}

@media (max-width: 480px) {
  .welcome-section h1 {
    font-size: 1.8rem;
  }
  
  .dashboard-header {
    padding: 1.5rem;
  }
  
  .action-card, .url-card, .chart-card {
    padding: 1.5rem;
  }
}
</style>

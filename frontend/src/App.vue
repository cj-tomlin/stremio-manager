<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import Dashboard from './components/Dashboard.vue';
import UserManagement from './components/UserManagement.vue';

const email = ref('admin@example.com');
const password = ref('adminpassword');
const token = ref(localStorage.getItem('accessToken') || null);
const installationUrl = ref(null);
const error = ref(null);
const currentUser = ref(null);
const currentView = ref('addon'); // 'addon', 'dashboard', or 'userManagement'

async function fetchCurrentUser() {
  if (!token.value) return;
  try {
    const response = await axios.get('/api/v1/users/me', {
      headers: { 'Authorization': `Bearer ${token.value}` }
    });
    currentUser.value = response.data;
  } catch (err) {
    console.error('Failed to fetch user data:', err);
    logout(); // Log out if token is invalid
  }
}

async function login() {
  error.value = null;
  const formData = new FormData();
  formData.append('username', email.value);
  formData.append('password', password.value);

  try {
    const response = await axios.post('/api/v1/auth/token', formData);
    token.value = response.data.access_token;
    localStorage.setItem('accessToken', token.value);
    await fetchCurrentUser();
    currentView.value = 'addon'; // Reset to default view on login
  } catch (err) {
    error.value = err.response?.data?.detail || 'Login failed';
    localStorage.removeItem('accessToken');
  }
}

async function getInstallationUrl() {
  error.value = null;
  try {
    const response = await axios.get('/api/v1/addons/torrentio/installation-url', {
      headers: {
        'Authorization': `Bearer ${token.value}`,
      },
    });
    installationUrl.value = response.data.installation_url;
  } catch (err) {
    error.value = err.response?.data?.detail || 'Failed to fetch URL';
  }
}

function logout() {
  token.value = null;
  installationUrl.value = null;
  error.value = null;
  currentUser.value = null;
  localStorage.removeItem('accessToken');
}

onMounted(() => {
  if (token.value) {
    fetchCurrentUser();
  }
});
</script>

<template>
  <header>
    <h1>Stremio Manager</h1>
    <button v-if="token" @click="logout">Logout</button>
  </header>

  <main>
    <div v-if="!token">
      <form @submit.prevent="login">
        <h2>Login</h2>
        <div>
          <label for="email">Email:</label>
          <input id="email" v-model="email" type="email" required>
        </div>
        <div>
          <label for="password">Password:</label>
          <input id="password" v-model="password" type="password" required>
        </div>
        <button type="submit">Login</button>
      </form>
    </div>

    <div v-if="token">
      <nav class="sub-nav">
        <button @click="currentView = 'addon'" :class="{ active: currentView === 'addon' }">Addon URL</button>
        <button @click="currentView = 'dashboard'" :class="{ active: currentView === 'dashboard' }">Dashboard</button>
        <button v-if="currentUser && currentUser.is_admin" @click="currentView = 'userManagement'" :class="{ active: currentView === 'userManagement' }">User Management</button>
      </nav>

      <div v-if="currentView === 'addon'" class="view-container">
        <h2>Get Your Add-on</h2>
        <button @click="getInstallationUrl">Get Torrentio URL</button>
        <div v-if="installationUrl">
          <p>Click the link to install your personalized Torrentio add-on:</p>
          <a :href="installationUrl">{{ installationUrl }}</a>
        </div>
      </div>

      <Dashboard v-if="currentView === 'dashboard'" />
      <UserManagement v-if="currentView === 'userManagement'" />
    </div>

    <div v-if="error" class="error">
      <p>Error: {{ error }}</p>
    </div>
  </main>
</template>

<style scoped>
header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  line-height: 1.5;
  margin-bottom: 2rem;
  padding: 0 1rem;
}

main {
  width: 100%;
  max-width: 960px; /* Wider for dashboard */
  margin: 0 auto;
  padding: 0 1rem;
}

form {
  max-width: 500px;
  margin: 0 auto;
}

form div {
  margin-bottom: 1rem;
}

label {
  display: block;
  margin-bottom: 0.25rem;
}

input {
  width: 100%;
  padding: 0.5rem;
  box-sizing: border-box;
}

.error {
  color: red;
  margin-top: 1rem;
  border: 1px solid red;
  padding: 1rem;
  max-width: 500px;
  margin: 1rem auto;
}

.sub-nav {
  margin-bottom: 2rem;
  border-bottom: 1px solid #ccc;
  padding-bottom: 1rem;
}

.sub-nav button {
  margin-right: 1rem;
  padding: 0.5rem 1rem;
  border: 1px solid transparent;
  background: none;
  cursor: pointer;
  font-size: 1rem;
}

.sub-nav button.active {
  border-bottom: 2px solid #42b983;
  font-weight: bold;
}

.view-container {
    max-width: 500px;
    margin: 0 auto;
}

</style>

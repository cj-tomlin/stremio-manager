<script setup>
import { ref } from 'vue';

const email = ref('admin@example.com');
const password = ref('admin');
const token = ref(localStorage.getItem('token') || null);
const installationUrl = ref(null);
const error = ref(null);

async function login() {
  error.value = null;
  const formData = new FormData();
  formData.append('username', email.value);
  formData.append('password', password.value);

  try {
    const response = await fetch('/api/v1/auth/token', {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || 'Login failed');
    }

    const data = await response.json();
    token.value = data.access_token;
    localStorage.setItem('token', token.value);
  } catch (err) {
    error.value = err.message;
    localStorage.removeItem('token');
  }
}

async function getInstallationUrl() {
  error.value = null;
  try {
    const response = await fetch('/api/v1/addons/torrentio/installation-url', {
      headers: {
        'Authorization': `Bearer ${token.value}`,
      },
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || 'Failed to fetch URL');
    }

    const data = await response.json();
    installationUrl.value = data.installation_url;
  } catch (err) {
    error.value = err.message;
  }
}

function logout() {
  token.value = null;
  installationUrl.value = null;
  error.value = null;
  localStorage.removeItem('token');
}
</script>

<template>
  <header>
    <h1>Stremio Manager</h1>
    <button v-if="token" @click="logout">Logout</button>
  </header>

  <main>
    <div v-if="!token">
      <h2>Login</h2>
      <form @submit.prevent="login">
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
      <h2>Get Your Add-on</h2>
      <button @click="getInstallationUrl">Get Torrentio URL</button>
      <div v-if="installationUrl">
        <p>Click the link to install your personalized Torrentio add-on:</p>
        <a :href="installationUrl">{{ installationUrl }}</a>
      </div>
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
}

main {
  width: 100%;
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
}
</style>

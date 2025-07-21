<template>
  <div class="container mx-auto px-4 sm:px-8">
    <div class="py-8">
      <div class="flex justify-between items-center">
        <h2 class="text-2xl font-semibold leading-tight">User Management</h2>
        <button @click="showCreateModal = true" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
          Create User
        </button>
      </div>
      <div v-if="error" class="error bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative" role="alert">
        <strong class="font-bold">Error:</strong>
        <span class="block sm:inline">{{ error }}</span>
      </div>
      <div class="-mx-4 sm:-mx-8 px-4 sm:px-8 py-4 overflow-x-auto">
        <div class="inline-block min-w-full shadow rounded-lg overflow-hidden">
          <table class="min-w-full leading-normal">
            <thead>
              <tr>
                <th class="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
                  User
                </th>
                <th class="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
                  Role
                </th>
                <th class="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
                  Created at
                </th>
                <th class="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
                  Status
                </th>
                <th class="px-5 py-3 border-b-2 border-gray-200 bg-gray-100"></th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="user in users" :key="user.id">
                <td class="px-5 py-5 border-b border-gray-200 bg-white text-sm">
                  <p class="text-gray-900 whitespace-no-wrap">{{ user.email }}</p>
                </td>
                <td class="px-5 py-5 border-b border-gray-200 bg-white text-sm">
                  <p class="text-gray-900 whitespace-no-wrap">{{ user.is_admin ? 'Admin' : 'User' }}</p>
                </td>
                <td class="px-5 py-5 border-b border-gray-200 bg-white text-sm">
                  <p class="text-gray-900 whitespace-no-wrap">
                    {{ new Date(user.created_at).toLocaleDateString() }}
                  </p>
                </td>
                <td class="px-5 py-5 border-b border-gray-200 bg-white text-sm">
                  <span class="relative inline-block px-3 py-1 font-semibold text-green-900 leading-tight">
                    <span aria-hidden class="absolute inset-0 bg-green-200 opacity-50 rounded-full"></span>
                    <span class="relative">Active</span>
                  </span>
                </td>
                <td class="px-5 py-5 border-b border-gray-200 bg-white text-sm text-right">
                  <button @click="openEditModal(user)" class="text-indigo-600 hover:text-indigo-900">Edit</button>
                  <button @click="openDeleteModal(user)" class="text-red-600 hover:text-red-900 ml-4">Delete</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

        <!-- Edit User Modal -->
    <div v-if="showEditModal" class="fixed z-10 inset-0 overflow-y-auto">
      <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
        <div class="fixed inset-0 transition-opacity" aria-hidden="true">
          <div class="absolute inset-0 bg-gray-500 opacity-75"></div>
        </div>
        <div class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full">
          <form @submit.prevent="updateUser">
            <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
              <h3 class="text-lg leading-6 font-medium text-gray-900">Edit User</h3>
              <div class="mt-2">
                <input v-model="editingUser.email" type="email" placeholder="Email" required class="w-full px-3 py-2 border border-gray-300 rounded-md">
              </div>
              <div class="mt-2">
                <input v-model="editingUser.password" type="password" placeholder="New Password (optional)" class="w-full px-3 py-2 border border-gray-300 rounded-md">
              </div>
              <div class="mt-2">
                <label class="inline-flex items-center">
                  <input type="checkbox" v-model="editingUser.is_admin" class="form-checkbox">
                  <span class="ml-2">Is Admin</span>
                </label>
              </div>
            </div>
            <div class="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
              <button type="submit" class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-blue-600 text-base font-medium text-white hover:bg-blue-700 sm:ml-3 sm:w-auto sm:text-sm">
                Update
              </button>
              <button @click="showEditModal = false" type="button" class="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm">
                Cancel
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- Delete User Modal -->
    <div v-if="showDeleteModal" class="fixed z-10 inset-0 overflow-y-auto">
        <div class="flex items-center justify-center min-h-screen">
            <div class="bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:max-w-lg sm:w-full">
                <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
                    <h3 class="text-lg leading-6 font-medium text-gray-900">Delete User</h3>
                    <p class="mt-2">Are you sure you want to delete {{ userToDelete.email }}? This action cannot be undone.</p>
                </div>
                <div class="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
                    <button @click="deleteUser" class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-red-600 text-base font-medium text-white hover:bg-red-700 sm:ml-3 sm:w-auto sm:text-sm">
                        Delete
                    </button>
                    <button @click="showDeleteModal = false" type="button" class="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm">
                        Cancel
                    </button>
                </div>
            </div>
        </div>
    </div>

    <!-- Create User Modal -->
    <div v-if="showCreateModal" class="fixed z-10 inset-0 overflow-y-auto">
      <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
        <div class="fixed inset-0 transition-opacity" aria-hidden="true">
          <div class="absolute inset-0 bg-gray-500 opacity-75"></div>
        </div>
        <div class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full">
          <form @submit.prevent="createUser">
            <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
              <h3 class="text-lg leading-6 font-medium text-gray-900">Create New User</h3>
              <div class="mt-2">
                <input v-model="newUser.email" type="email" placeholder="Email" required class="w-full px-3 py-2 border border-gray-300 rounded-md">
              </div>
              <div class="mt-2">
                <input v-model="newUser.password" type="password" placeholder="Password" required class="w-full px-3 py-2 border border-gray-300 rounded-md">
              </div>
            </div>
            <div class="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
              <button type="submit" class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-blue-600 text-base font-medium text-white hover:bg-blue-700 sm:ml-3 sm:w-auto sm:text-sm">
                Create
              </button>
              <button @click="showCreateModal = false" type="button" class="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm">
                Cancel
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const users = ref([]);
const error = ref(null);
const showCreateModal = ref(false);
const newUser = ref({
  email: '',
  password: '',
});
const showEditModal = ref(false);
const editingUser = ref(null);
const showDeleteModal = ref(false);
const userToDelete = ref(null);

const fetchUsers = async () => {
  error.value = null;
  try {
    const token = localStorage.getItem('accessToken');
    if (!token) {
      throw new Error('Authentication token not found.');
    }
    const response = await axios.get('/api/v1/users/', {
      headers: { 'Authorization': `Bearer ${token}` },
    });
    users.value = response.data;
  } catch (err) {
    error.value = err.response?.data?.detail || 'Failed to fetch users';
    console.error('Failed to fetch users:', err);
  }
};

const openEditModal = (user) => {
  editingUser.value = { ...user, password: '' }; // Copy user and clear password
  showEditModal.value = true;
};

const updateUser = async () => {
  if (!editingUser.value) return;
  error.value = null;
  try {
    const token = localStorage.getItem('accessToken');
    const payload = {
      email: editingUser.value.email,
      is_admin: editingUser.value.is_admin,
    };
    if (editingUser.value.password) {
      payload.password = editingUser.value.password;
    }
    await axios.put(`/api/v1/users/${editingUser.value.id}`, payload, {
      headers: { 'Authorization': `Bearer ${token}` },
    });
    showEditModal.value = false;
    await fetchUsers();
  } catch (err) {
    error.value = err.response?.data?.detail || 'Failed to update user';
    console.error('Failed to update user:', err);
  }
};

const openDeleteModal = (user) => {
  userToDelete.value = user;
  showDeleteModal.value = true;
};

const deleteUser = async () => {
  if (!userToDelete.value) return;
  error.value = null;
  try {
    const token = localStorage.getItem('accessToken');
    await axios.delete(`/api/v1/users/${userToDelete.value.id}`, {
      headers: { 'Authorization': `Bearer ${token}` },
    });
    showDeleteModal.value = false;
    await fetchUsers();
  } catch (err) {
    error.value = err.response?.data?.detail || 'Failed to delete user';
    console.error('Failed to delete user:', err);
  }
};

const createUser = async () => {
  error.value = null;
  try {
    const token = localStorage.getItem('accessToken');
    await axios.post('/api/v1/users/', newUser.value, {
      headers: { 'Authorization': `Bearer ${token}` },
    });
    showCreateModal.value = false;
    newUser.value = { email: '', password: '' }; // Reset form
    await fetchUsers(); // Refresh the list
  } catch (err) {
    error.value = err.response?.data?.detail || 'Failed to create user';
    console.error('Failed to create user:', err);
  }
};

onMounted(() => {
  fetchUsers();
});
</script>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { authApi } from '@/api'

const router = useRouter()
const form = ref({ username: '', email: '', password: '', password2: '' })
const error = ref('')
const loading = ref(false)

const register = async () => {
  if (form.value.password !== form.value.password2) {
    error.value = 'Le password non coincidono'
    return
  }
  loading.value = true
  error.value = ''
  try {
    await authApi.register({ username: form.value.username, email: form.value.email, password: form.value.password })
    router.push('/login')
  } catch (e) {
    error.value = e.response?.data?.detail || 'Errore registrazione'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="container py-5">
    <div class="row justify-content-center">
      <div class="col-md-5">
        <div class="card">
          <div class="card-body p-4">
            <h2 class="mb-4">Registrazione</h2>
            <div class="alert alert-danger" v-if="error">{{ error }}</div>
            <div class="mb-3">
              <label class="form-label">Username</label>
              <input type="text" class="form-control" v-model="form.username" required autofocus>
            </div>
            <div class="mb-3">
              <label class="form-label">Email</label>
              <input type="email" class="form-control" v-model="form.email" required>
            </div>
            <div class="mb-3">
              <label class="form-label">Password</label>
              <input type="password" class="form-control" v-model="form.password" required>
            </div>
            <div class="mb-3">
              <label class="form-label">Conferma Password</label>
              <input type="password" class="form-control" v-model="form.password2" required>
            </div>
            <button class="btn btn-primary w-100" @click="register" :disabled="loading">
              {{ loading ? 'Registrazione...' : 'Registrati' }}
            </button>
            <p class="mt-3 text-center">
              Hai già un account? <router-link to="/login">Login</router-link>
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
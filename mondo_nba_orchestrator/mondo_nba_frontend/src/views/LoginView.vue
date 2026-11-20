<script setup>
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { authApi } from '@/api'

const router = useRouter()
const route = useRoute()
const form = ref({ username: '', password: '' })
const error = ref('')
const loading = ref(false)

const login = async () => {
  loading.value = true
  error.value = ''
  try {
    const res = await authApi.login(form.value)
    localStorage.setItem('auth_token', res.data.token)
    localStorage.setItem('user', form.value.username)
    const redirect = route.query.redirect || '/'
    router.push(redirect)
  } catch (e) {
    error.value = e.response?.data?.detail || 'Credenziali non valide'
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
            <h2 class="mb-4">Login</h2>
            <div class="alert alert-danger" v-if="error">{{ error }}</div>
            <div class="mb-3">
              <label class="form-label">Username</label>
              <input type="text" class="form-control" v-model="form.username" required autofocus>
            </div>
            <div class="mb-3">
              <label class="form-label">Password</label>
              <input type="password" class="form-control" v-model="form.password" required>
            </div>
            <button class="btn btn-primary w-100" @click="login" :disabled="loading">
              {{ loading ? 'Accesso...' : 'Accedi' }}
            </button>
            <p class="mt-3 text-center">
              Non hai un account? <router-link to="/register">Registrati</router-link>
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
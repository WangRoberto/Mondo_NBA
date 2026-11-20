<script setup>
import { onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useProductStore } from '@/stores'
import ProductCard from '@/components/ProductCard.vue'
import Pagination from '@/components/Pagination.vue'

const router = useRouter()
const productStore = useProductStore()

const isLoggedIn = computed(() => !!localStorage.getItem('auth_token'))
const user = computed(() => localStorage.getItem('user') || '')
const cartCount = computed(() => {
  const cart = JSON.parse(localStorage.getItem('cart') || '[]')
  return cart.reduce((sum, item) => sum + item.quantity, 0)
})

onMounted(() => {
  productStore.fetchProducts()
})

const loadPage = (url) => {
  if (url) productStore.fetchProducts({ page: new URL(url).searchParams.get('page') })
}

const logout = () => {
  localStorage.removeItem('auth_token')
  localStorage.removeItem('user')
  router.push('/')
}
</script>

<template>
  <div class="container py-4">
    <header class="d-flex justify-content-between align-items-center mb-4">
      <h1>Mondo NBA</h1>
      <nav>
        <router-link to="/cart" class="btn btn-outline-primary me-2">
          Carrello ({{ cartCount }})
        </router-link>
        <router-link to="/login" class="btn btn-outline-secondary me-2" v-if="!isLoggedIn">Login</router-link>
        <router-link to="/register" class="btn btn-outline-secondary me-2" v-if="!isLoggedIn">Registrati</router-link>
        <span v-else class="me-2">Ciao, {{ user }}</span>
        <button class="btn btn-outline-danger" v-if="isLoggedIn" @click="logout">Logout</button>
      </nav>
    </header>

    <div class="row g-4" v-if="!productStore.loading">
      <div class="col-md-4" v-for="product in productStore.items" :key="product.id">
        <ProductCard :product="product" />
      </div>
    </div>
    <div v-else class="text-center py-5">Caricamento...</div>

    <Pagination
      v-if="productStore.pagination.next || productStore.pagination.previous"
      :next="productStore.pagination.next"
      :previous="productStore.pagination.previous"
      @load="loadPage"
    />
  </div>
</template>
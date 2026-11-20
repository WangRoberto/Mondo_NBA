<script setup>
import { computed } from 'vue'

defineProps(['product'])

const stars = computed(() => {
  const v = Number(product.valuation) || 0
  return '★'.repeat(v) + '☆'.repeat(5 - v)
})
</script>

<template>
  <div class="card h-100 shadow-sm">
    <img :src="product.image" class="card-img-top" :alt="product.name" style="height: 220px; object-fit: cover;">
    <div class="card-body d-flex flex-column">
      <h5 class="card-title">{{ product.name }}</h5>
      <p class="card-text text-muted small">{{ product.category }}</p>
      <p class="card-text small text-truncate">{{ product.description }}</p>
      <p class="text-warning mb-1">{{ stars }}</p>
      <p class="fw-bold fs-5 text-primary">&euro;{{ product.price }}</p>
      <router-link :to="`/products/${product.id}`" class="btn btn-outline-primary mt-auto">Dettagli</router-link>
    </div>
  </div>
</template>
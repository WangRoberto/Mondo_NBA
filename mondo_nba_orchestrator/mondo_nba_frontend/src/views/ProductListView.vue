<script setup>
import { ref, onMounted, computed } from 'vue'
import { useProductStore } from '@/stores'
import { productsApi } from '@/api'
import ProductCard from '@/components/ProductCard.vue'
import Pagination from '@/components/Pagination.vue'

const productStore = useProductStore()
const searchQuery = ref('')
const selectedCategory = ref('')
const priceRange = ref('')
const orderBy = ref('-id')

const categories = ref(['Clothing', 'Gadget', 'Shoes', 'Accessories'])

const fetchProducts = () => {
  const params = {}
  if (searchQuery.value) params.search = searchQuery.value
  if (selectedCategory.value) params.category = selectedCategory.value
  if (orderBy.value) params.ordering = orderBy.value
  if (priceRange.value) {
    const [min, max] = priceRange.value.split('-')
    if (min) params.min_price = min
    if (max) params.max_price = max
  }
  productStore.fetchProducts(params)
}

onMounted(() => fetchProducts())

const loadPage = (url) => {
  if (url) {
    const page = new URL(url).searchParams.get('page')
    productStore.fetchProducts({ ...getParams(), page })
  }
}

const getParams = () => {
  const params = {}
  if (searchQuery.value) params.search = searchQuery.value
  if (selectedCategory.value) params.category = selectedCategory.value
  if (orderBy.value) params.ordering = orderBy.value
  if (priceRange.value) {
    const [min, max] = priceRange.value.split('-')
    if (min) params.min_price = min
    if (max) params.max_price = max
  }
  return params
}
</script>

<template>
  <div class="container py-4">
    <h1 class="mb-4">Prodotti</h1>

    <!-- Filtri e ricerca -->
    <div class="row mb-4 g-3">
      <div class="col-md-4">
        <input type="text" class="form-control" placeholder="Cerca prodotto..." v-model="searchQuery" @input="fetchProducts">
      </div>
      <div class="col-md-2">
        <select class="form-select" v-model="selectedCategory" @change="fetchProducts">
          <option value="">Tutte le categorie</option>
          <option v-for="cat in categories" :key="cat" :value="cat">{{ cat }}</option>
        </select>
      </div>
      <div class="col-md-2">
        <select class="form-select" v-model="priceRange" @change="fetchProducts">
          <option value="">Tutti i prezzi</option>
          <option value="0-50">0-50 €</option>
          <option value="51-100">51-100 €</option>
          <option value="101-150">101-150 €</option>
          <option value="151-200">151-200 €</option>
          <option value="201-">201+ €</option>
        </select>
      </div>
      <div class="col-md-2">
        <select class="form-select" v-model="orderBy" @change="fetchProducts">
          <option value="-id">Più recenti</option>
          <option value="-valuation">Più votati</option>
          <option value="price">Prezzo crescente</option>
          <option value="-price">Prezzo decrescente</option>
        </select>
      </div>
    </div>

    <!-- Griglia prodotti -->
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
<script setup>
import { onMounted, ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useProductStore, useCartStore } from '@/stores'
import { productsApi, commentsApi } from '@/api'
import StarRating from '@/components/StarRating.vue'

const route = useRoute()
const router = useRouter()
const productStore = useProductStore()
const cartStore = useCartStore()

const product = ref(null)
const loading = ref(true)
const comments = ref([])
const newComment = ref({ content: '', valuation: 5 })
const posting = ref(false)

onMounted(async () => {
  try {
    const res = await productsApi.get(route.params.id)
    product.value = res.data
  } catch (e) {
    console.error(e)
    router.push('/')
  } finally {
    loading.value = false
  }
})

const addToCart = async () => {
  if (!product.value) return
  await cartStore.addToCart(product.value.id, 1)
  alert('Aggiunto al carrello!')
}

const submitComment = async () => {
  if (!newComment.value.content.trim()) return
  posting.value = true
  try {
    await commentsApi.add({
      product: product.value.id,
      content: newComment.value.content,
      valuation: newComment.value.valuation,
    })
    newComment.value.content = ''
    newComment.value.valuation = 5
    // reload comments (would need comments fetch)
  } catch (e) {
    alert('Errore: ' + e.message)
  } finally {
    posting.value = false
  }
}
</script>

<template>
  <div class="container py-4" v-if="!loading && product">
    <router-link to="/" class="btn btn-outline-secondary mb-3">&larr; Indietro</router-link>

    <div class="row">
      <div class="col-md-6">
        <img :src="product.image" class="img-fluid rounded" :alt="product.name">
      </div>
      <div class="col-md-6">
        <h1>{{ product.name }}</h1>
        <p class="text-muted">{{ product.category }}</p>
        <StarRating :value="product.valuation" readonly />
        <p class="mt-3">{{ product.description }}</p>
        <p class="fw-bold fs-3 text-primary">&euro;{{ product.price }}</p>
        <button class="btn btn-primary btn-lg mt-3" @click="addToCart" :disabled="cartStore.loading">
          <span v-if="cartStore.loading">Aggiunta...</span>
          <span v-else>Aggiungi al carrello</span>
        </button>
      </div>
    </div>

    <hr class="my-5">

    <h3>Recensioni</h3>
    <div class="mb-4">
      <h5>Lascia una recensione</h5>
      <StarRating v-model="newComment.valuation" />
      <textarea class="form-control mt-2" v-model="newComment.content" rows="3" placeholder="La tua opinione..."></textarea>
      <button class="btn btn-success mt-2" @click="submitComment" :disabled="posting">
        {{ posting ? 'Invio...' : 'Invia' }}
      </button>
    </div>

    <div v-for="c in comments" :key="c.id" class="border-bottom py-3">
      <strong>{{ c.user }}</strong>
      <StarRating :value="c.valuation" readonly class="ms-2" />
      <p class="mt-1">{{ c.content }}</p>
    </div>
  </div>
  <div v-else class="text-center py-5">Caricamento...</div>
</template>
<script setup>
import { onMounted, computed } from 'vue'
import { useCartStore } from '@/stores'
import { cartApi } from '@/api'
import { useRouter } from 'vue-router'

const cartStore = useCartStore()
const router = useRouter()

onMounted(() => cartStore.fetchCart())

const checkout = async () => {
  if (cartStore.items.length === 0) return
  // Redirect to payment flow (stripe)
  router.push('/payment')
}
</script>

<template>
  <div class="container py-4">
    <h1>Carrello</h1>

    <div v-if="cartStore.loading" class="text-center py-5">Caricamento...</div>
    <div v-else-if="cartStore.items.length === 0" class="text-center py-5">
      <p class="text-muted">Il carrello è vuoto</p>
      <router-link to="/" class="btn btn-primary">Continua lo shopping</router-link>
    </div>
    <div v-else>
      <div class="table-responsive">
        <table class="table align-middle">
          <thead>
            <tr>
              <th>Prodotto</th>
              <th>Prezzo</th>
              <th>Quantità</th>
              <th>Totale</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in cartStore.items" :key="item.id">
              <td>
                <div class="d-flex align-items-center">
                  <img :src="item.product.image" :alt="item.product.name" style="width: 60px; height: 60px; object-fit: cover;" class="me-3 rounded">
                  {{ item.product.name }}
                </div>
              </td>
              <td>&euro;{{ item.product.price }}</td>
              <td>
                <input type="number" class="form-control form-control-sm w-50" v-model.number="item.quantity" min="1" @change="cartStore.updateQuantity(item.id, item.quantity)">
              </td>
              <td class="fw-bold">&euro;{{ (item.product.price * item.quantity).toFixed(2) }}</td>
              <td>
                <button class="btn btn-sm btn-outline-danger" @click="cartStore.removeFromCart(item.id)">Rimuovi</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="d-flex justify-content-end gap-2 mt-3">
        <router-link to="/" class="btn btn-outline-secondary">Continua lo shopping</router-link>
        <button class="btn btn-success btn-lg" @click="checkout" :disabled="cartStore.loading">
          Checkout &euro;{{ cartStore.total.toFixed(2) }}
        </button>
      </div>
    </div>
  </div>
</template>
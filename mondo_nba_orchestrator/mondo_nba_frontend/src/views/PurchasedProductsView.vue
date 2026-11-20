<script setup>
import { onMounted, ref } from 'vue'
import { useCartStore } from '@/stores'
import { paymentsApi } from '@/api'

const payments = ref([])
const loading = ref(true)

onMounted(async () => {
  try {
    const res = await paymentsApi.list()
    payments.value = res.data
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div class="container py-4">
    <h1 class="mb-4">I miei acquisti</h1>

    <div v-if="loading" class="text-center py-5">Caricamento...</div>
    <div v-else-if="payments.length === 0" class="text-center py-5">
      <p class="text-muted">Nessun acquisto effettuato</p>
      <router-link to="/" class="btn btn-primary">Vai allo shopping</router-link>
    </div>
    <div v-else>
      <div class="table-responsive">
        <table class="table align-middle">
          <thead>
            <tr>
              <th>Prodotto</th>
              <th>Quantità</th>
              <th>Indirizzo</th>
              <th>Pagato</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="p in payments" :key="p.id">
              <td>
                <div class="d-flex align-items-center">
                  <img :src="p.product?.image" :alt="p.product?.name" style="width: 50px; height: 50px; object-fit: cover;" class="me-2 rounded">
                  {{ p.product?.name }}
                </div>
              </td>
              <td>{{ p.quantity }}</td>
              <td>{{ p.address }}</td>
              <td>
                <span class="badge" :class="p.payment_bool ? 'bg-success' : 'bg-warning'">
                  {{ p.payment_bool ? 'Pagato' : 'In attesa' }}
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>
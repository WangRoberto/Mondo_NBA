<script setup>
import { ref, onMounted } from 'vue'
import { productsApi } from '@/api'
import { useRouter } from 'vue-router'

const router = useRouter()
const products = ref([])
const loading = ref(true)
const message = ref('')
const page = ref(1)
const totalPages = ref(1)

// Form stato
const form = ref({ name: '', price: '', valuation: 3, category: '', description: '' })
const imageFile = ref(null)
const action = ref('Create')
const updateId = ref(null)
const whatField = ref('name')
const fieldValue = ref('')
const deleteId = ref(null)

const fetchProducts = async () => {
  loading.value = true
  try {
    const res = await productsApi.list({ page: page.value })
    products.value = res.data.results
    totalPages.value = Math.ceil(res.data.count / 5)
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

onMounted(() => fetchProducts())

const submitCreate = async () => {
  const formData = new FormData()
  formData.append('name', form.value.name)
  formData.append('price', form.value.price)
  formData.append('valuation', form.value.valuation)
  formData.append('category', form.value.category)
  formData.append('description', form.value.description)
  if (imageFile.value) formData.append('image', imageFile.value)

  try {
    await productsApi.create(formData)
    message.value = 'Prodotto creato con successo'
    form.value = { name: '', price: '', valuation: 3, category: '', description: '' }
    imageFile.value = null
    fetchProducts()
  } catch (e) {
    message.value = 'Errore: ' + (e.response?.data?.detail || e.message)
  }
}

const submitDelete = async () => {
  if (!deleteId.value) return
  try {
    await productsApi.delete(deleteId.value)
    message.value = 'Prodotto eliminato'
    deleteId.value = null
    fetchProducts()
  } catch (e) {
    message.value = 'Errore: ' + (e.response?.data?.detail || e.message)
  }
}

const submitUpdate = async () => {
  if (!updateId.value || !whatField.value) return
  const data = {}
  data[whatField.value] = fieldValue.value
  try {
    await productsApi.update(updateId.value, data)
    message.value = 'Prodotto aggiornato'
    fetchProducts()
  } catch (e) {
    message.value = 'Errore: ' + (e.response?.data?.detail || e.message)
  }
}

const onFileChange = (e) => {
  imageFile.value = e.target.files[0]
}
</script>

<template>
  <div class="container py-4">
    <h1 class="mb-4">Gestione Prodotti (Admin)</h1>

    <div class="alert alert-info" v-if="message">{{ message }}</div>

    <!-- Form creazione -->
    <div class="card mb-4">
      <div class="card-header">Crea nuovo prodotto</div>
      <div class="card-body">
        <div class="row g-3">
          <div class="col-md-4">
            <input type="text" class="form-control" placeholder="Nome" v-model="form.name">
          </div>
          <div class="col-md-2">
            <input type="number" class="form-control" placeholder="Prezzo" v-model="form.price">
          </div>
          <div class="col-md-2">
            <input type="number" class="form-control" placeholder="Valutazione" v-model="form.valuation" min="0" max="5">
          </div>
          <div class="col-md-2">
            <input type="text" class="form-control" placeholder="Categoria" v-model="form.category">
          </div>
          <div class="col-md-2">
            <input type="file" class="form-control" @change="onFileChange">
          </div>
          <div class="col-12">
            <textarea class="form-control" placeholder="Descrizione" v-model="form.description" rows="2"></textarea>
          </div>
          <div class="col-12">
            <button class="btn btn-success" @click="submitCreate">Crea</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Form eliminazione -->
    <div class="card mb-4">
      <div class="card-header">Elimina prodotto</div>
      <div class="card-body">
        <div class="input-group">
          <input type="number" class="form-control" placeholder="ID prodotto" v-model="deleteId">
          <button class="btn btn-danger" @click="submitDelete">Elimina</button>
        </div>
      </div>
    </div>

    <!-- Form aggiornamento -->
    <div class="card mb-4">
      <div class="card-header">Aggiorna prodotto</div>
      <div class="card-body">
        <div class="row g-3">
          <div class="col-md-2">
            <input type="number" class="form-control" placeholder="ID" v-model="updateId">
          </div>
          <div class="col-md-3">
            <select class="form-select" v-model="whatField">
              <option value="name">Nome</option>
              <option value="price">Prezzo</option>
              <option value="valuation">Valutazione</option>
              <option value="category">Categoria</option>
              <option value="description">Descrizione</option>
            </select>
          </div>
          <div class="col-md-4">
            <input type="text" class="form-control" placeholder="Nuovo valore" v-model="fieldValue">
          </div>
          <div class="col-md-3">
            <button class="btn btn-warning" @click="submitUpdate">Aggiorna</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Lista prodotti -->
    <h3>Lista prodotti (pagina {{ page }})</h3>
    <div v-if="loading" class="text-center py-5">Caricamento...</div>
    <div v-else>
      <table class="table table-striped">
        <thead>
          <tr>
            <th>ID</th>
            <th>Nome</th>
            <th>Prezzo</th>
            <th>Categoria</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="p in products" :key="p.id">
            <td>{{ p.id }}</td>
            <td>{{ p.name }}</td>
            <td>&euro;{{ p.price }}</td>
            <td>{{ p.category }}</td>
          </tr>
        </tbody>
      </table>
      <div class="d-flex justify-content-between">
        <button class="btn btn-outline-secondary" :disabled="page <= 1" @click="page--; fetchProducts()">Precedente</button>
        <button class="btn btn-outline-secondary" :disabled="page >= totalPages" @click="page++; fetchProducts()">Successiva</button>
      </div>
    </div>
  </div>
</template>
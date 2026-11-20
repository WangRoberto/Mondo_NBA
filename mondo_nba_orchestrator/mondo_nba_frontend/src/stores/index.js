import { defineStore } from 'pinia'
import { productsApi, cartApi } from '@/api'

export const useProductStore = defineStore('products', {
  state: () => ({
    items: [],
    loading: false,
    pagination: { count: 0, next: null, previous: null },
    error: null,
  }),
  actions: {
    async fetchProducts(params = {}) {
      this.loading = true
      this.error = null
      try {
        const res = await productsApi.list(params)
        this.items = res.data.results
        this.pagination = {
          count: res.data.count,
          next: res.data.next,
          previous: res.data.previous,
        }
      } catch (e) {
        this.error = e.message
      } finally {
        this.loading = false
      }
    },
  },
})

export const useCartStore = defineStore('cart', {
  state: () => ({
    items: [],
    loading: false,
    error: null,
  }),
  getters: {
    total: (state) => state.items.reduce((sum, item) => sum + item.product.price * item.quantity, 0),
    count: (state) => state.items.reduce((sum, item) => sum + item.quantity, 0),
  },
  actions: {
    async fetchCart() {
      this.loading = true
      try {
        const res = await cartApi.list()
        this.items = res.data
      } catch (e) {
        this.error = e.message
      } finally {
        this.loading = false
      }
    },
    async addToCart(productId, quantity = 1) {
      await cartApi.add({ product: productId, quantity })
      await this.fetchCart()
    },
    async updateQuantity(id, quantity) {
      await cartApi.update(id, { quantity })
      await this.fetchCart()
    },
    async removeFromCart(id) {
      await cartApi.remove(id)
      await this.fetchCart()
    },
  },
})
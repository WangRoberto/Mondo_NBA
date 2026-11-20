<script setup>
defineProps({ value: { type: Number, default: 0 }, readonly: { type: Boolean, default: false } })
defineEmits(['update:modelValue'])

const stars = [1, 2, 3, 4, 5]
const hover = ref(0)

const setRating = (val) => {
  if (!readonly.value) emit('update:modelValue', val)
}
</script>

<template>
  <span class="fs-4 text-warning" style="cursor: pointer;">
    <span v-for="s in stars" :key="s" @click="setRating(s)" @mouseenter="hover = s" @mouseleave="hover = 0">
      {{ !readonly && (hover >= s || value >= s) ? '★' : '☆' }}
    </span>
  </span>
</template>
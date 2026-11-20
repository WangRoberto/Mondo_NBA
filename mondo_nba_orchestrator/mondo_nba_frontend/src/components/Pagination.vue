<script setup>
defineProps(['next', 'previous'])
defineEmits(['load'])
</script>

<template>
  <nav aria-label="Pagination" class="mt-4">
    <ul class="pagination justify-content-center">
      <li class="page-item" :class="{ disabled: !previous }">
        <a class="page-link" href="#" @click.prevent="() => $emit('load', previous)">Precedente</a>
      </li>
      <li class="page-item" :class="{ disabled: !next }">
        <a class="page-link" href="#" @click.prevent="() => $emit('load', next)">Successiva</a>
      </li>
    </ul>
  </nav>
</template>
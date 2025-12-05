<script setup>
import { storeToRefs } from "pinia";
import { useCatalogStore } from "../../stores/catalog";
import { watch } from "vue";

// STORES
const productStore = useCatalogStore();
const { query } = storeToRefs(productStore);
const { getProductsByQuery } = productStore;

// METHODS
const debounce = (fn, delay) => {
  let timeout;
  return (...args) => {
    clearTimeout(timeout);
    timeout = setTimeout(() => {
      fn(...args);
    }, delay);
  };
};

watch(query, debounce(getProductsByQuery, 500));
</script>

<template>
  <div class="search">
    <input
      class="search__input"
      type="text"
      v-model="query"
      placeholder="Поиск товаров..."
    />
  </div>
</template>

<style scoped lang="scss">
.search {
  width: 400px;
  &__input {
    width: 100%;
    padding: 20px;
    border-radius: 10px;
    border: none;
    font-size: 18px;
  }
}
</style>

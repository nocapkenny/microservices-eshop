<script setup>
import { computed } from "vue";
import { useCatalogStore } from "../stores/catalog";
import { storeToRefs } from "pinia";

const catalogStore = useCatalogStore();
const { categories, activeCategory, productsCount } = storeToRefs(catalogStore);
const { setActiveCategory } = catalogStore;

</script>

<template>
  <section class="categories" v-auto-animate>
    <button :class="{active: activeCategory === null}" class="category" @click="setActiveCategory(null)">Все товары ({{ productsCount }})</button>
    <button
      class="category"
      :class="{active: activeCategory === category.slug}"
      v-for="category in categories"
      :key="category.id"
      @click="setActiveCategory(category.slug)"
    >
      {{ category.name }} ({{ category.products_count }})
    </button>
  </section>
</template>

<style scoped lang="scss">
.categories{
    display: flex;
    gap: 10px;
}
.category.active{
    background-color: #2e8b57;;
    color: #fff;
}
</style>

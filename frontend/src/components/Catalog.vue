<script setup>
import { onMounted, watch } from "vue";
import { useCatalogStore } from "../stores/catalog";
import { storeToRefs } from "pinia";
import CatalogCard from "./CatalogCard.vue";
import Pagination from "./ui/Pagination.vue";
import Filter from "./Filter.vue";
import Loader from "./ui/Loader.vue";

// STORES
const catalogStore = useCatalogStore();
const {
  products,
  catalogPages,
  activePage,
  activeCategory,
  productsCount,
  isProductsLoading,
} = storeToRefs(catalogStore);
const { getProducts, getCategories } = catalogStore;

watch(
  () => activePage.value,
  () => {
    getProducts();
  },
  { deep: true },
);

onMounted(() => {
  getProducts();
  getCategories();
});
</script>

<template>
  <div class="container">
    <h2 class="title">Каталог товаров</h2>
    <Filter />
    <section class="loading" v-if="isProductsLoading">
      <Loader size="lg" />
    </section>
    <section
      class="products"
      v-auto-animate
      v-if="products.length > 0 && !isProductsLoading"
    >
      <CatalogCard
        v-for="product in products"
        :key="product.id"
        :product="product"
      />
    </section>
    <section
      class="not-found"
      v-auto-animate
      v-else-if="(products.length === 0 || !products) && !isProductsLoading"
    >
      <p class="not-found__text" v-auto-animate>Товары не найдены 😭</p>
    </section>
    <Pagination
      v-if="productsCount > 3 && !activeCategory"
      :pages="catalogPages"
      v-model="activePage"
    />
  </div>
</template>

<style scoped lang="scss">
.loading{
  margin-top: 200px;
}
.products {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  padding-bottom: 30px;
}
.not-found__text {
  font-size: 50px;
  text-align: center;
}
</style>

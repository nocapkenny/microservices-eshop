<script setup>
import { onMounted, watch, ref } from "vue";
import { useCatalogStore } from "../stores/catalog";
import { storeToRefs } from "pinia";
import CatalogCard from "../components/CatalogCard.vue";
import Pagination from "../components/ui/Pagination.vue";
import Filter from "../components/Filter.vue";
import Loader from "../components/ui/Loader.vue";
import axios from "axios";
import Slider from "../components/ui/Slider.vue";

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


// REFS
const sliders = ref([]);

// METHODS
const getSliders = async () => {
  try {
    const { data } = await axios.get(`/api/sliders/`);
    sliders.value = data.results;
  } catch (e) {
    console.log(e);
  }
};

// HOOKS
onMounted(async () => {
  await getSliders();
  await getProducts();
  await getCategories();
});
watch(
  () => activePage.value,
  async () => {
    await getProducts();
  },
  { deep: true },
);
</script>

<template>
  <div class="container">
    <Slider :slides="sliders" />
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
.title {
  margin-top: 50px;
  margin-bottom: 30px;
}
.loading {
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

@media (max-width: 1024px) {
  .title {
    margin-top: 100px;
    margin-bottom: 20px;
  }
  .products {
    grid-template-columns: repeat(2, 1fr);
  }
}
@media (max-width: 768px) {
  .products {
    grid-template-columns: repeat(1, 1fr);
  }
}
</style>

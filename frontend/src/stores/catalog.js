import { defineStore } from "pinia";
import { ref } from "vue";
import axios from "axios";

export const useCatalogStore = defineStore("catalog", () => {
  // STATES
  const products = ref([]);
  const categories = ref([]);
  const activeCategory = ref(null);
  const query = ref("");
  const catalogPages = ref(1)
  const activePage = ref(1)
  const productsCount = ref(0)
  const isProductsLoading = ref(false)

  // ACTIONS
  const getProducts = async () => {
    try {
      isProductsLoading.value = true
      const { data } = await axios.get(`/api/products/?page=${activePage.value}`);
      products.value = data.results;
      catalogPages.value = Math.ceil(data.count / 3)
      productsCount.value = data.count
    } catch (e) {
      console.log(e);
    } finally{
      isProductsLoading.value = false
    }
  };

  const getProductsByQuery = async () => {
    try {
      isProductsLoading.value = true
      const { data } = await axios.get(
        `/api/products/?search=${query.value}`
      );
      products.value = data.results;
    } catch (e) {
      console.log(e);
    } finally{
      isProductsLoading.value = false
    }
  };

  const getProductsBySlug = async (slug) => {
    try {
      isProductsLoading.value = true
      const { data } = await axios.get(
        `/api/products/${slug}/`
      );
      products.value = data.results;
    } catch (e) {
      console.log(e);
    } finally{
      isProductsLoading.value = false
    }
  };

  const getCategories = async () => {
    try {
      const { data } = await axios.get("/api/categories");
      categories.value = data.results;
    } catch (e) {
      console.log(e);
    }
  };

  const setActiveCategory = (category) => {
    if (category === activeCategory.value) {
      return;
    }
    if (category === null) {
      activeCategory.value = null;
      getProducts();
      return;
    } else {
      console.log(category);
      activeCategory.value = category;
      getProductsBySlug(category);
    }
  };

  return {
    products,
    getProducts,
    categories,
    getCategories,
    activeCategory,
    setActiveCategory,
    getProductsByQuery,
    query,
    catalogPages,
    activePage,
    productsCount,
    isProductsLoading
  };
});

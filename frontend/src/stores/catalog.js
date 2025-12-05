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

  // ACTIONS
  const getProducts = async () => {
    try {
      const { data } = await axios.get(`/api/products/?page=${activePage.value}`);
      products.value = data.results;
      catalogPages.value = Math.ceil(data.count / 3)
      productsCount.value = data.count
    } catch (e) {
      console.log(e);
    }
  };

  const getProductsByQuery = async () => {
    try {
      const { data } = await axios.get(
        `/api/products/?search=${query.value}`
      );
      products.value = data.results;
    } catch (e) {
      console.log(e);
    }
  };

  const getProductsBySlug = async (slug) => {
    try {
      const { data } = await axios.get(
        `/api/products/${slug}/`
      );
      products.value = data.results;
    } catch (e) {
      console.log(e);
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
    productsCount
  };
});

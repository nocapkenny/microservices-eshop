import { defineStore } from "pinia";
import { ref } from "vue";
import axios from "axios";
import { notyf } from "../plugins/notyf";

export const useCartStore = defineStore("cart", () => {
  // STATE
  const cart = ref([]);
  const isCartLoading = ref(false);

  // ACTIONS
  const getCart = async (accessToken) => {
    isCartLoading.value = true
    try {
      const { data } = await axios.get("/api/cart/", {
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      });
      cart.value = data;
      console.log(cart.value);
    } catch (e) {
      console.log(e);
    } finally{
      isCartLoading.value = false
    }
  };

  const addToCart = async (product_id, accessToken) => {
    try {
      isCartLoading.value = true
      const { data } = await axios.post(
        "/api/cart/add/",
        {
          product_id: product_id,
        },
        {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        }
      );
      cart.value = data;
      getCart(accessToken);
      notyf.success("Товар добавлен в корзину!");
    } catch (e) {
      console.log(e);
      notyf.error('Ошибка добавления товара в корзину')
    } finally{
      isCartLoading.value = false
    }
  };

  const clearCart = async (accessToken) => {
    try {
      isCartLoading.value = true
      const { data } = await axios.post(
        "/api/cart/clear/",
        { user_id: cart.value.user_id },
        {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        }
      );
      getCart(accessToken);
      notyf.success("Корзина очищена!");
    } catch (e) {
      console.log(e);
    } finally{
      isCartLoading.value = false
    }
  };

  const updateCart = async (product_id, quantity, accessToken) => {
    try {
      const { data } = await axios.patch(
        `/api/cart/update/${product_id}/`,
        { quantity },
        {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        }
      );
      cart.value = data;
    } catch (e) {
      console.log(e);
    }
  };

  const deleteItem = async (product_id, accessToken) => {
    try {
      isCartLoading.value = true
      const { data } = await axios.delete(
        `/api/cart/delete/${product_id}/`,
        {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        }
      );
      cart.value = data;
    } catch (e) {
      console.log(e);
    } finally{
      isCartLoading.value = false
    }
  };

  return {
    cart,
    getCart,
    addToCart,
    updateCart,
    clearCart,
    deleteItem,
    isCartLoading
  };
});

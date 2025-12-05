import { defineStore } from "pinia";
import { ref } from "vue";
import axios from "axios";

export const useCartStore = defineStore("cart", () => {
  // STATE
  const cart = ref([]);
  const accessToken = ref(localStorage.getItem("access") || null);

  // ACTIONS
  const getCart = async () => {
    try {
      const { data } = await axios.get("/api/cart/", {
        headers: {
          Authorization: `Bearer ${accessToken.value}`,
        },
      });
      cart.value = data;
      console.log(cart.value);
    } catch (e) {
      console.log(e);
    }
  };

  const addToCart = async (product_id) => {
    try {
      const { data } = await axios.post(
        "/api/cart/add/",
        {
          product_id: product_id,
        },
        {
          headers: {
            Authorization: `Bearer ${accessToken.value}`,
          },
        }
      );
      cart.value = data;
      getCart();
    } catch (e) {
      console.log(e);
    }
  };

  const clearCart = async () => {
    try {
      const { data } = await axios.post(
        "/api/cart/clear/",
        { user_id: cart.value.user_id },
        {
          headers: {
            Authorization: `Bearer ${accessToken.value}`,
          },
        }
      );
      getCart();
    } catch (e) {
      console.log(e);
    }
  };

  const updateCart = async (product_id, quantity) => {
    try {
      const { data } = await axios.patch(
        `/api/cart/update/${product_id}/`,
        { quantity },
        {
          headers: {
            Authorization: `Bearer ${accessToken.value}`,
          },
        }
      );
      cart.value = data;
      console.log(data);
    } catch (e) {
      console.log(e);
    }
  };

  const deleteItem = async (product_id) => {
    try {
      const { data } = await axios.delete(
        `/api/cart/delete/${product_id}/`,
        {
          headers: {
            Authorization: `Bearer ${accessToken.value}`,
          },
        }
      );
      cart.value = data;
      console.log(data);
    } catch (e) {
      console.log(e);
    }
  };

  return {
    cart,
    getCart,
    addToCart,
    updateCart,
    clearCart,
    deleteItem
  };
});

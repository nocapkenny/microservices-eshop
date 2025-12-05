import { defineStore } from "pinia";
import { ref } from "vue";
import axios from "axios";

export const useOrderStore = defineStore("order", () => {
  const orders = ref([]);
  const accessToken = ref(localStorage.getItem("access") || null);

  const getOrders = async () => {
    try {
      const { data } = await axios.get("/api/order/list/", {
        headers: {
          Authorization: `Bearer ${accessToken.value}`,
        },
      });
      orders.value = data.results;
      console.log(orders.value);
    } catch (e) {
      console.log(e);
    }
  };

  const createOrder = async (shipping_address) => {
    try {
      const { data } = await axios.post(
        "/api/order/create/",
        { shipping_address },
        {
          headers: {
            Authorization: `Bearer ${accessToken.value}`,
          },
        }
      );
      orders.value = data;
    } catch (e) {
      console.log(e);
    }
  }

  return {
    orders,
    getOrders,
    createOrder
  };
});

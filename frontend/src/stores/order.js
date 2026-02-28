import { defineStore } from "pinia";
import { ref } from "vue";
import axios from "axios";
import { notyf } from "../plugins/notyf";

export const useOrderStore = defineStore("order", () => {
  const orders = ref([]);
  const getOrders = async (accessToken) => {
    try {
      const { data } = await axios.get("/api/order/list/", {
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      });
      orders.value = data.results;
      console.log(orders.value);
    } catch (e) {
      console.log(e);
    }
  };

  const createOrder = async (shipping_address, accessToken) => {
    try {
      const { data } = await axios.post(
        "/api/order/create/",
        { shipping_address },
        {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        }
      );
      orders.value = data;
      notyf.success("Заказ успешно создан!");
    } catch (e) {
      console.log(e);
      notyf.error('Ошибка создания заказа')
    }
  }

  return {
    orders,
    getOrders,
    createOrder
  };
});

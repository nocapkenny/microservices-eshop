<script setup>
import Header from "./components/Header.vue";
import Catalog from "./components/Catalog.vue";
import ModalManager from "./components/ModalManager.vue";
import { onMounted } from "vue";
import { useUserStore } from "./stores/user";
import { useCartStore } from "./stores/cart";
import { useOrderStore } from "./stores/order";

const userStore = useUserStore();
const cartStore = useCartStore();
const orderStore = useOrderStore();

onMounted( async () => {
  if (localStorage.getItem("access")){
    await userStore.getUser();
    await cartStore.getCart(localStorage.getItem("access"));
    await orderStore.getOrders(localStorage.getItem("access"));
  }
});
</script>

<template>
  <Header />
  <Catalog />
  <ModalManager />
</template>

<style scoped lang="scss"></style>

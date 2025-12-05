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

onMounted(() => {
  if (localStorage.getItem("access")){
    userStore.getUser();
    cartStore.getCart();
    orderStore.getOrders();
  }
});
</script>

<template>
  <Header />
  <Catalog />
  <ModalManager />
</template>

<style scoped lang="scss"></style>

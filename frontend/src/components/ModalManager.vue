<script setup>
import Login from "./modal/Login.vue";
import Cart from "./modal/Cart.vue";
import Order from "./modal/Order.vue";
import { useModalStore } from "../stores/modal";
import { computed } from "vue";
import { storeToRefs } from "pinia";

// STORE
const modalStore = useModalStore();
const { activeModal } = storeToRefs(modalStore);
const { closeModal } = modalStore;

// COMPUTED
const component = computed(() => {
  if (activeModal.value === "login") return Login;
  else if(activeModal.value === 'cart') return Cart
  else if(activeModal.value === 'order') return Order
});
</script>

<template>
  <component :is="component" @close="closeModal" />
</template>

<style scoped lang="scss"></style>

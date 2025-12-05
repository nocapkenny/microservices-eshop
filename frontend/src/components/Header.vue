<script setup>
import Search from "./ui/Search.vue";
import { useModalStore } from "../stores/modal";
import { useUserStore } from "../stores/user";
import { storeToRefs } from "pinia";

// STORES
const userStore = useUserStore();
const { user, isLoggedIn } = storeToRefs(userStore);

// STORE
const modalStore = useModalStore();
const { setActiveModal } = modalStore;
</script>

<template>
  <header class="header">
    <div class="container">
      <h1 class="header__title">TechStore</h1>
      <Search />
      <div class="header__buttons">
        <button
          class="header__button"
          @click="setActiveModal('login')"
          v-if="!isLoggedIn"
        >
          <img
            class="header__button-img"
            src="../assets/images/user.svg"
            alt="userImg"
          />
        </button>
        <p class="header__email" v-if="isLoggedIn">{{ user.email }}</p>
        <button class="header__button" @click="setActiveModal('cart')">
          <img
            class="header__button-img"
            src="../assets/images/cart.svg"
            alt="cartImg"
          />
        </button>
        <button class="header__button" @click="setActiveModal('order')">
          <img
            class="header__button-img"
            src="../assets/images/order.svg"
            alt="orderImg"
          />
        </button>
      </div>
    </div>
  </header>
</template>

<style lang="scss" scoped>
.header .container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 75px;
}
.header {
  border-bottom: 1px solid rgba(255, 255, 255, 0.5);
  height: 75px;
  &__email {
    margin-right: 20px;
    font-size: 20px;
    font-weight: 600;
  }
  &__buttons {
    display: flex;
    gap: 10px;
    align-items: center;
  }
  &__button {
    background-color: rgba(255, 255, 255, 1);
    padding: 10px;
    border-radius: 10px;
    border: none;
    width: 50px;
    height: 50px;
    &:hover {
      .header__button-img {
        transform: scale(1.1);
      }
    }
  }
  &__button-img {
    width: 30px;
    height: 30px;
    transition: all 0.1s ease-in-out;
  }
}
</style>

<script setup>
import Search from "./ui/Search.vue";
import { useUserStore } from "../stores/user";
import { useOrderStore } from "../stores/order";
import { useCartStore } from "../stores/cart";
import { storeToRefs } from "pinia";
import { computed, onMounted, ref } from "vue";
import { onClickOutside } from "@vueuse/core";

// STORES
const userStore = useUserStore();
const { user, isLoggedIn } = storeToRefs(userStore);
const { logout } = userStore;

const orderStore = useOrderStore();
const { orders } = storeToRefs(orderStore);

const cartStore = useCartStore();
const { cart } = storeToRefs(cartStore);

// REFS
const isShowDropdown = ref(false);
const dropdownRef = ref(null);

// COMPUTED
const ordersText = computed(() => {
  if (orders.value.length > 0) return `Кол-во заказов: ${orders.value.length}`;
  else return "У вас пока нет заказов";
});

const cartText = computed(() => {
  console.log(cart.value);
  if (cart.value.items && cart.value.items.length > 0)
    return `Товаров в корзине: ${cart.value.items.length}`;
  else return "Корзина пуста";
});

const dropdownClasses = computed(() => {
  return {
    "header__email-dropdown--active": isShowDropdown.value,
    "header__email-dropdown": true,
  };
});

// METHODS
const handleDropdownClick = () => {
  isShowDropdown.value = !isShowDropdown.value;
};
const handleLogout = async () => {
  logout();
  orders.value = [];
  cart.value = [];
};

// HOOKS
onClickOutside(dropdownRef, () => {
  isShowDropdown.value = false;
});
</script>

<template>
  <header class="header">
    <div class="container">
      <router-link class="header__title" to="/">TechStore</router-link>
      <Search />
      <div class="header__buttons">
        <router-link class="header__button" to="/me" v-if="!isLoggedIn">
          <img
            class="header__button-img"
            src="../assets/images/user.svg"
            alt="userImg"
          />
        </router-link>
        <div class="header__email" v-if="isLoggedIn">
          <p class="header__email-text" @click="handleDropdownClick">
            {{ user.email }}
          </p>
          <div :class="dropdownClasses" ref="dropdownRef">
            <router-link
              class="header__email-text header__email-text--dropdown"
              to="/orders"
              >{{ ordersText }}</router-link
            >
            <router-link
              class="header__email-text header__email-text--dropdown"
              to="/cart"
              >{{ cartText }}</router-link
            >
            <button class="danger" @click="handleLogout">Выйти</button>
          </div>
        </div>
        <router-link class="header__button" to="/cart">
          <img
            class="header__button-img"
            src="../assets/images/cart.svg"
            alt="cartImg"
          />
        </router-link>
        <router-link class="header__button" to="/orders">
          <img
            class="header__button-img"
            src="../assets/images/order.svg"
            alt="orderImg"
          />
        </router-link>
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
  &__title{
    font-size: 50px;
    color: white;
    font-weight: 300;
    cursor: pointer;
  }
  &__email {
    margin-right: 20px;
    font-size: 20px;
    font-weight: 600;
    position: relative;
  }
  &__email-text {
    cursor: pointer;
    color: white;
  }
  &__email-dropdown {
    position: absolute;
    max-height: 0px;
    opacity: 0;
    pointer-events: none;
    z-index: 3;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
    background-color: #242424;
    padding: 15px;
    top: 100%;
    left: 50%;
    transform: translateX(-50%);
    height: fit-content;
    width: 250px;
    border-radius: 15px;
    display: flex;
    flex-direction: column;
    gap: 20px;
    transition: all 0.2s ease-in-out;
  }
  &__email-dropdown--active {
    max-height: 300px;
    opacity: 1;
    pointer-events: all;
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

@media (max-width: 1024px){
  .header{
    & .container{
      flex-wrap: wrap;
    }
    &__title{
      order: 1;
      padding: 15px 0;
      font-size: 30px;
    }
    &__email{
      margin-right: 0;
      position: static;
    }
    &__email-text{
      font-size: 16px;
    }
    &__buttons{
      order: 2;
    }
    &__email-dropdown{
      left: 0;
      top: 74px;
      border-radius: 0px 0px 15px 15px;
      transform: translateX(0px);
      width: 100vw;
    }
    & .search{
      order: 3;
      width: 100%;
      display: block;
      margin-top: 30px;
    }
  }
}
</style>

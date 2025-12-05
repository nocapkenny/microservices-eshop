<script setup>
import { computed, onMounted, watch } from "vue";
import { useCartStore } from "../stores/cart";
import { storeToRefs } from "pinia";

const props = defineProps({
  product: {
    type: Object,
    required: true,
  },
});

const cartStore = useCartStore();
const { addToCart } = cartStore;
const { cart } = storeToRefs(cartStore);

const isProductInCart = computed(() => {
  const items = cart.value?.items || [];
  return (
    props.product.id &&
    items.some((item) => item.product_id === props.product.id)
  );
});

const stockClass = computed(() => ({
  "card__info-stock": true,
  "card__info-stock--out": props.product.stock_quantity === 0,
}));
</script>

<template>
  <div class="card">
    <div class="card__box">
      <img
        :src="props.product.main_image"
        :alt="props.name"
        class="card__box-img"
      />
    </div>
    <div class="card__info">
      <h3 class="card__info-title">{{ props.product.name }}</h3>
      <p
        :class="stockClass"
        v-if="
          props.product.stock_quantity >= 10 ||
          props.product.stock_quantity === 0
        "
      >
        {{ props.product.is_in_stock ? "В наличии" : "Нет в наличии" }}
      </p>
      <p
        class="card__info-count"
        v-else-if="
          props.product.stock_quantity < 10 &&
          props.product.stock_quantity !== 0
        "
      >
        {{ `Осталось ${props.product.stock_quantity} шт.` }}
      </p>
    </div>
    <div class="card__footer">
      <p class="card__footer-price">
        {{
          props.product.price
            ? `${Number(props.product.price).toFixed(0)} ₽`
            : "Цена не указана"
        }}
      </p>
      <button
        class="card__footer-button"
        :class="{ disabled: !props.product.is_in_stock || isProductInCart }"
        :disabled="!props.product.is_in_stock || isProductInCart"
        @click="addToCart(props.product.id)"
      >
        <img
          class="card__footer-img"
          src="../assets/images/cart.svg"
          alt="cart"
        />
      </button>
    </div>
  </div>
</template>

<style lang="scss">
$dark-bg: #121212;
$card-bg: #1e1e1e;
$text: #e0e0e0;
$accent-red: #c22a3b;
$accent-green: #2e8b57;
.card {
  // border: 1px solid black;
  border-radius: 30px;
  &__box {
    width: 400px;
    height: 400px;
  }
  &__box-img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    border-radius: 6px;
  }
  &__info {
    display: flex;
    align-items: center;
    justify-content: space-between;
  }
  &__info-count {
    color: $accent-red;
    font-weight: 500;
    font-size: 16px;
  }
  &__info-stock {
    border: 2px solid #2e8b57;
    border-radius: 10px;
    padding: 5px;
    color: #2e8b57;
    font-weight: 500;
    font-size: 16px;
  }
  &__info-stock.card__info-stock--out {
    color: $accent-red;
    border: 2px solid $accent-red;
  }
  &__footer {
    display: flex;
    align-items: center;
    justify-content: space-between;
  }
  &__footer-price {
    color: #2e8b57;
    font-size: 30px;
    font-weight: 700;
  }
  &__footer-button {
    background-color: #2e8b57;
    &.disabled {
      opacity: 0.5;
    }
  }
  &__footer-img {
    width: 30px;
    height: 30px;
  }
}
</style>

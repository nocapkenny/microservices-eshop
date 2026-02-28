<script setup>
import { defineEmits } from "vue";
import { computed, ref } from "vue";
import { useOrderStore } from "../../stores/order";
import { storeToRefs } from "pinia";

const emit = defineEmits(["close"]);

const orderStore = useOrderStore();
const { orders } = storeToRefs(orderStore);

const status = computed(() => (item) => {
  if (item.status === "pending") return "В обработке";
  else if (item.status === "confirmed") return "Подтвержден";
  else if (item.status === "shipped") return "Отправлен";
  else if (item.status === "delivered") return "Доставлен";
  else if (item.status === "cancelled") return "Отклонен";
});

const closeModal = () => {
  emit("close");
};
</script>

<template>
  <div class="aside" @click="closeModal">
    <div class="aside__overlay"></div>
    <div class="aside__order" @click.stop>
      <button class="aside__order-close" @click="closeModal">&times;</button>

      <h2 class="aside__order-title">Заказы</h2>

      <div v-if="orders.length === 0" class="aside__empty">
        У вас нет заказов
      </div>
      <div class="aside__orders" v-else>
        <div class="aside__orders-order" v-for="order in orders">
          <p class="aside__order-title">Заказ #{{ order.id }}</p>
          <div class="aside__items">
            <div v-for="item in order.items" :key="item.id" class="aside__item">
              <div class="aside__item-info">
                <h3 class="aside__item-name">{{ item.product_name }} x {{ item.quantity }} шт.</h3>
                <p class="aside__item-price">{{ item.subtotal }} ₽</p>
              </div>
            </div>
          </div>
          <p class="aside__item-status">{{ status(order) }}</p>
          <div class="aside__total">
            Итого: <strong>{{ order.total_amount }} ₽</strong>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
// Используем те же переменные, что и в auth modal
$dark-bg: #121212;
$card-bg: #1e1e1e;
$text: #e0e0e0;
$accent-red: #c22a3b;
$accent-green: #2e8b57;
.btn-primary.disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.aside {
  position: fixed;
  top: 0;
  right: 0;
  width: 100vw;
  height: 100vh;
  z-index: 1000;
  display: flex;
  justify-content: flex-end;
  align-items: flex-start;
  &__input {
    margin-top: 30px;
    border: none;
    padding: 15px 20px;
    border-radius: 6px;
    font-size: 16px;
  }
  &__overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.7);
    backdrop-filter: blur(4px);
  }
  &__orders {
    padding-bottom: 120px;
    max-height: 100vh;
    overflow-y: auto;
  }
  &__order {
    position: relative;
    width: 90%;
    max-width: 420px;
    height: 100vh;
    background: $card-bg;
    color: $text;
    padding: 2rem 1.5rem;
    box-shadow: -10px 0 30px rgba(0, 0, 0, 0.5);
    z-index: 1;
    animation: slideInFromRight 0.3s ease-out;

    @keyframes slideInFromRight {
      from {
        transform: translateX(100%);
        opacity: 0;
      }
      to {
        transform: translateX(0);
        opacity: 1;
      }
    }
  }

  &__order-close {
    position: absolute;
    top: 1rem;
    right: 1rem;
    background: none;
    border: none;
    color: #aaa;
    font-size: 1.8rem;
    cursor: pointer;
    width: 32px;
    height: 32px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    transition: color 0.2s, background 0.2s;
  }

  &__order-title {
    margin-top: 0;
    margin-bottom: 1.5rem;
    font-size: 1.5rem;
    font-weight: 600;
    text-align: center;
  }

  &__empty {
    text-align: center;
    color: #aaa;
    font-style: italic;
    padding: 2rem 0;
  }

  &__items {
    display: flex;
    flex-direction: column;
    gap: 1.2rem;
  }

  &__item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-bottom: 1rem;
    border-bottom: 1px solid #333;
  }

  &__item-info {
    flex: 1;
  }

  &__item-name {
    font-size: 1rem;
    margin: 0 0 0.3rem 0;
  }

  &__item-price {
    font-size: 0.9rem;
    color: #aaa;
    margin: 0;
  }

  &__item-controls {
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }

  &__item-btn {
    width: 28px;
    height: 28px;
    border: 1px solid #444;
    background: #2a2a2a;
    color: $text;
    border-radius: 4px;
    font-weight: bold;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;

    &:disabled {
      opacity: 0.4;
      cursor: not-allowed;
    }

    &:not(:disabled):hover {
      background: $accent-red;
      border-color: $accent-red;
    }
  }

  &__item-quantity {
    min-width: 24px;
    text-align: center;
    font-weight: 600;
  }

  &__total {
    margin: 1.5rem 0;
    font-size: 1.2rem;
    text-align: right;
    border-top: 1px solid #333;
    padding-top: 1rem;
  }

  &__checkout,
  &__clear {
    width: 100%;
    padding: 0.85rem;
    background: $accent-green;
    color: white;
    border: none;
    border-radius: 8px;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    transition: background 0.2s;

    &:hover {
      background: #d03a4b;
    }
  }
  &__clear {
    background: $accent-red;
  }
}
</style>

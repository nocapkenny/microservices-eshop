<script setup>
import { computed, ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { useOrderStore } from "../stores/order";
import { useUserStore } from "../stores/user";
import { storeToRefs } from "pinia";
import Loader from "../components/ui/Loader.vue";

// ROUTER
const router = useRouter();

// STORES
const orderStore = useOrderStore();
const { orders, isOrdersLoading } = storeToRefs(orderStore);
const { fetchOrders } = orderStore;

const userStore = useUserStore();
const { accessToken, isLoggedIn } = storeToRefs(userStore);

// REFS
const errorMessage = ref("");
const expandedOrderId = ref(null);

// COMPUTED
const getStatusText = (status) => {
  const statusMap = {
    pending: "В обработке",
    confirmed: "Подтвержден",
    shipped: "Отправлен",
    delivered: "Доставлен",
    cancelled: "Отменен",
  };
  return statusMap[status] || status;
};

const getStatusClass = (status) => {
  const classMap = {
    pending: "status-pending",
    confirmed: "status-confirmed",
    shipped: "status-shipped",
    delivered: "status-delivered",
    cancelled: "status-cancelled",
  };
  return classMap[status] || "";
};

const formatDate = (dateString) => {
  if (!dateString) return "";
  return new Date(dateString).toLocaleDateString("ru-RU", {
    year: "numeric",
    month: "long",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
};

// METHODS
const toggleOrderDetails = (orderId) => {
  expandedOrderId.value = expandedOrderId.value === orderId ? null : orderId;
};

const continueShopping = () => {
  router.push({ name: "catalog" });
};

onMounted(async () => {
  if (!isLoggedIn.value) {
    router.push({
      name: "user",
      query: { next: router.currentRoute.value.fullPath },
    });
    return;
  }

  try {
    await fetchOrders(accessToken.value);
  } catch (err) {
    errorMessage.value = "Не удалось загрузить историю заказов";
  }
});
</script>

<template>
  <main class="orders-page">
    <div class="container">
      <div class="orders-header">
        <h1 class="orders-title">Мои заказы</h1>
        <button class="btn-secondary" @click="continueShopping">
          ← В каталог
        </button>
      </div>

      <div v-if="isOrdersLoading" class="orders-loading">
        <Loader size="lg" text="Загружаем заказы..." />
      </div>

      <div v-else-if="orders.length === 0" class="orders-empty">
        <div class="orders-empty-icon">📦</div>
        <h2>У вас пока нет заказов</h2>
        <p>Оформите первый заказ в нашем каталоге</p>
        <button class="btn-primary" @click="continueShopping">
          Перейти к покупкам
        </button>
      </div>

      <div v-else class="orders-list">
        <div
          v-for="order in orders"
          :key="order.id"
          class="order-card"
          :class="{ 'order-card--expanded': expandedOrderId === order.id }"
        >
          <div class="order-header" @click="toggleOrderDetails(order.id)">
            <div class="order-meta">
              <span class="order-id">Заказ #{{ order.id }}</span>
              <span class="order-date">{{ formatDate(order.created_at) }}</span>
            </div>

            <div class="order-status-wrapper">
              <span :class="['order-status', getStatusClass(order.status)]">
                {{ getStatusText(order.status) }}
              </span>
              <button
                class="order-toggle-btn"
                :class="{ expanded: expandedOrderId === order.id }"
              >
                {{ expandedOrderId === order.id ? "▲" : "▼" }}
              </button>
            </div>
          </div>

          <div class="order-details">
            <div class="order-items">
              <div
                v-for="item in order.items"
                :key="item.id"
                class="order-item"
              >
                <div class="order-item-info">
                  <h4 class="order-item-name">{{ item.product_name }}</h4>
                  <p class="order-item-quantity">× {{ item.quantity }} шт.</p>
                </div>

                <div class="order-item-price">{{ item.subtotal }} ₽</div>
              </div>
            </div>

            <div class="order-footer">
              <div class="order-total">
                <span>Итого:</span>
                <strong>{{ order.total_amount }} ₽</strong>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>

<style lang="scss" scoped>
$dark-bg: #121212;
$card-bg: #1e1e1e;
$text: #e0e0e0;
$text-muted: #aaa;
$accent-red: #c22a3b;
$accent-green: #2e8b57;
$input-bg: #2a2a2a;
$border-color: #333;

// Статусы заказов
$status-pending: #ffc107;
$status-confirmed: #17a2b8;
$status-shipped: #6f42c1;
$status-delivered: #28a745;
$status-cancelled: #dc3545;

.orders-page {
  min-height: calc(100vh - 75px);
  padding: 40px 0;
  background: $dark-bg;
  color: $text;
  @media (max-width: 768px) {
    padding: 120px 0;
  }
}

.container {
  max-width: 900px;
  margin: 0 auto;
  padding: 0 20px;
}

// Заголовок
.orders-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  flex-wrap: wrap;
  gap: 15px;

  @media (max-width: 576px) {
    flex-direction: column;
    align-items: flex-start;
  }
}

.orders-title {
  margin: 0;
  font-size: 2rem;
  font-weight: 700;
}

// Кнопки
.btn-secondary {
  padding: 10px 20px;
  background: transparent;
  border: 1px solid $border-color;
  border-radius: 8px;
  color: $text;
  font-size: 1rem;
  cursor: pointer;
  transition: background 0.2s;

  &:hover {
    background: $input-bg;
  }
}

.btn-primary {
  padding: 12px 30px;
  background: $accent-green;
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;

  &:hover {
    background: lighten($accent-green, 5%);
  }
}

// Ошибки
.error-banner {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: rgba(255, 107, 107, 0.15);
  border: 1px solid #ff6b6b;
  color: #ff6b6b;
  padding: 1rem 1.25rem;
  border-radius: 10px;
  margin-bottom: 25px;

  .error-close {
    background: none;
    border: none;
    color: inherit;
    font-size: 1.5rem;
    cursor: pointer;
    padding: 0 5px;

    &:hover {
      opacity: 0.8;
    }
  }
}

// Пустой список
.orders-empty {
  text-align: center;
  padding: 60px 20px;
  background: $card-bg;
  border-radius: 16px;

  &-icon {
    font-size: 4rem;
    margin-bottom: 20px;
    opacity: 0.7;
  }

  h2 {
    margin: 0 0 10px;
    font-size: 1.5rem;
  }

  p {
    margin: 0 0 25px;
    color: $text-muted;
  }
}

.orders-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.order-card {
  background: $card-bg;
  border-radius: 16px;
  border: 1px solid $border-color;
  overflow: hidden;
  transition: border-color 0.2s;

  &:hover {
    border-color: lighten($border-color, 10%);
  }
}

.order-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 25px;
  cursor: pointer;
  user-select: none;

  @media (max-width: 576px) {
    padding: 15px 20px;
  }
}

.order-meta {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.order-id {
  font-size: 1.1rem;
  font-weight: 600;
}

.order-date {
  font-size: 0.9rem;
  color: $text-muted;
}

.order-status-wrapper {
  display: flex;
  align-items: center;
  gap: 12px;
}

.order-status {
  padding: 6px 14px;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 500;
  color: white;

  &.status-pending {
    background: $status-pending;
    color: #121212;
  }
  &.status-confirmed {
    background: $status-confirmed;
  }
  &.status-shipped {
    background: $status-shipped;
  }
  &.status-delivered {
    background: $status-delivered;
  }
  &.status-cancelled {
    background: $status-cancelled;
  }
}

.order-toggle-btn {
  background: none;
  border: none;
  color: $text-muted;
  font-size: 1rem;
  cursor: pointer;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition:
    background 0.2s,
    color 0.2s;

  &:hover {
    background: $input-bg;
    color: $text;
  }

  &.expanded {
    color: $accent-green;
  }
  @media (min-width: 769px) {
    display: none;
  }
}

.order-details {
  @media (max-width: 768px) {
    max-height: 0;
    overflow: hidden;
    transition: max-height 0.3s ease-out;

    .order-card--expanded & {
      max-height: 1000px;
      transition: max-height 0.4s ease-in;
    }
  }
}

.order-items {
  padding: 0 25px 20px;
  border-bottom: 1px solid $border-color;

  @media (max-width: 576px) {
    padding: 0 20px 15px;
  }
}

.order-item {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 15px;
  align-items: center;
  padding: 15px 0;
  border-bottom: 1px solid $border-color;

  &:last-child {
    border-bottom: none;
  }

  @media (max-width: 576px) {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
}

.order-item-image {
  width: 60px;
  height: 60px;
  border-radius: 8px;
  overflow: hidden;
  background: $input-bg;
  display: flex;
  align-items: center;
  justify-content: center;

  @media (max-width: 576px) {
    grid-area: image;
    width: 50px;
    height: 50px;
  }

  img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }

  &-placeholder {
    font-size: 1.2rem;
    font-weight: 600;
    color: $text-muted;
  }
}

.order-item-info {
  @media (max-width: 576px) {
    grid-area: info;
  }
}

.order-item-name {
  margin: 0 0 4px;
  font-size: 1rem;
  font-weight: 500;
}

.order-item-quantity {
  margin: 0;
  font-size: 0.9rem;
  color: $text-muted;
}

.order-item-price {
  font-size: 1rem;
  font-weight: 600;
  color: $accent-green;

  @media (max-width: 576px) {
    grid-area: price;
    text-align: right;
  }
}

.order-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 25px;
  gap: 20px;
  flex-wrap: wrap;

  @media (max-width: 576px) {
    padding: 15px 20px;
    flex-direction: column;
    align-items: flex-start;
  }
}

.order-total {
  display: flex;
  gap: 8px;
  font-size: 1.1rem;

  strong {
    color: $accent-green;
    font-size: 1.3rem;
  }
}

.order-actions {
  display: flex;
  gap: 20px;

  @media (max-width: 576px) {
    width: 100%;
    justify-content: flex-end;
  }
}

.btn-text {
  background: none;
  border: none;
  padding: 0;
  font-size: 0.95rem;
  cursor: pointer;
  transition: opacity 0.2s;

  &:hover:not(:disabled) {
    opacity: 0.8;
    text-decoration: underline;
  }

  &:disabled {
    opacity: 0.4;
    cursor: not-allowed;
  }

  &.btn-danger {
    color: #ff6b6b;
  }

  &.btn-repeat {
    color: $accent-green;
  }
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.order-card {
  animation: slideIn 0.3s ease-out backwards;

  @for $i from 1 through 10 {
    &:nth-child(#{$i}) {
      animation-delay: #{$i * 0.05}s;
    }
  }
}
</style>

<script setup>
import { computed, ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { useCartStore } from "../stores/cart";
import { useOrderStore } from "../stores/order";
import { useCatalogStore } from "../stores/catalog";
import { useUserStore } from "../stores/user";
import { storeToRefs } from "pinia";
import Loader from "../components/ui/Loader.vue";

// ROUTER
const router = useRouter();

// STORES
const cartStore = useCartStore();
const { cart, isCartLoading } = storeToRefs(cartStore);
const { updateCart, clearCart, deleteItem, fetchCart } = cartStore;

const orderStore = useOrderStore();
const { createOrder, isOrderLoading } = orderStore;

const catalogStore = useCatalogStore();
const { getProducts } = catalogStore;

const userStore = useUserStore();
const { accessToken, isLoggedIn } = storeToRefs(userStore);

// REFS
const address = ref("");
const errorMessage = ref("");
const isSubmitting = ref(false);

// COMPUTED
const isAddressValid = computed(() => address.value.trim().length >= 5);

const total = computed(() => {
  if (!cart.value?.items) return 0;
  return cart.value.items.reduce(
    (sum, item) => sum + item.product_price * item.quantity,
    0,
  );
});

const cartItemsCount = computed(() => {
  return cart.value?.items?.reduce((sum, item) => sum + item.quantity, 0) || 0;
});

// METHODS
const increaseQuantity = async (item) => {
  if (item.quantity < item.product_info.stock_quantity) {
    item.quantity++;
    try {
      await updateCart(item.id, item.quantity, accessToken.value);
    } catch (err) {
      item.quantity--;
      errorMessage.value = "Не удалось обновить количество";
    }
  }
};

const decreaseQuantity = async (item) => {
  if (item.quantity > 1) {
    item.quantity--;
    try {
      await updateCart(item.id, item.quantity, accessToken.value);
    } catch (err) {
      item.quantity++;
      errorMessage.value = "Не удалось обновить количество";
    }
  }
};

const handleDeleteItem = async (itemId) => {
  try {
    await deleteItem(itemId, accessToken.value);
  } catch (err) {
    errorMessage.value = "Не удалось удалить товар";
  }
};

const handleCreateOrder = async () => {
  if (!isAddressValid.value) {
    errorMessage.value = "Пожалуйста, укажите корректный адрес доставки";
    return;
  }

  if (!cart.value?.items?.length) {
    errorMessage.value = "Корзина пуста";
    return;
  }

  isSubmitting.value = true;
  errorMessage.value = "";

  try {
    await createOrder(address.value, accessToken.value);
    await clearCart(accessToken.value);
    await getProducts(); 

    router.push({ name: "orders" });
  } catch (err) {
    errorMessage.value = err.message || "Ошибка при оформлении заказа";
  } finally {
    isSubmitting.value = false;
  }
};

const continueShopping = () => {
  router.push({ name: "catalog" });
};

onMounted(async () => {
  if (isLoggedIn.value && accessToken.value) {
    try {
      await fetchCart(accessToken.value);
    } catch (err) {
      errorMessage.value = "Не удалось загрузить корзину";
    }
  }
});
</script>

<template>
  <main class="cart-page">
    <div class="container">
      <div class="cart-header">
        <h1 class="cart-title">Ваша корзина</h1>
        <p v-if="cartItemsCount" class="cart-subtitle">
          Товаров: <strong>{{ cartItemsCount }}</strong>
        </p>
      </div>

      <div v-if="!cart.items || cart.items.length === 0" class="cart-empty">
        <div class="cart-empty-icon">🛒</div>
        <h2>Корзина пуста</h2>
        <p>Добавьте товары из каталога, чтобы оформить заказ</p>
        <button class="btn-primary" @click="continueShopping">
          Перейти в каталог
        </button>
      </div>

      <div v-else class="cart-content">
        <div class="cart-items">
          <div v-for="item in cart.items" :key="item.id" class="cart-item">
            <div class="cart-item-info">
              <h3 class="cart-item-name">{{ item.product_info.name }}</h3>
              <p class="cart-item-sku" v-if="item.product_info.article">
                Артикул: {{ item.product_info.article }}
              </p>
              <p class="cart-item-price">{{ item.product_price }} ₽</p>

              <p
                class="cart-item-stock"
                :class="{ 'low-stock': item.product_info.stock_quantity <= 3 }"
              >
                В наличии: {{ item.product_info.stock_quantity }} шт.
              </p>
            </div>

            <div class="cart-item-controls">
              <div class="quantity-control">
                <button
                  class="quantity-btn"
                  @click="decreaseQuantity(item)"
                  :disabled="item.quantity <= 1 || isCartLoading"
                >
                  −
                </button>
                <span class="quantity-value">{{ item.quantity }}</span>
                <button
                  class="quantity-btn"
                  @click="increaseQuantity(item)"
                  :disabled="
                    item.quantity >= item.product_info.stock_quantity ||
                    isCartLoading
                  "
                >
                  +
                </button>
              </div>
            </div>

            <div class="cart-item-total">
              {{ item.product_price * item.quantity }} ₽
            </div>

            <button
              class="btn-text btn-danger"
              @click="handleDeleteItem(item.id)"
              :disabled="isCartLoading"
            >
              Удалить
            </button>
          </div>
        </div>

        <aside class="cart-summary">
          <h3>Итого</h3>

          <div class="summary-row">
            <span>Товары ({{ cartItemsCount }}):</span>
            <strong>{{ total }} ₽</strong>
          </div>

          <div class="summary-row">
            <span>Доставка:</span>
            <span class="free-shipping">Бесплатно</span>
          </div>

          <div class="summary-total">
            <span>К оплате:</span>
            <span class="total-amount">{{ total }} ₽</span>
          </div>

          <div class="delivery-address">
            <label for="address">Адрес доставки</label>
            <input
              id="address"
              type="text"
              v-model="address"
              placeholder="Введите адрес"
              :disabled="isSubmitting"
              class="input"
            />
            <p class="input-hint">Минимум 5 символов</p>
          </div>

          <button
            class="btn-primary btn-checkout"
            :disabled="!isAddressValid || isSubmitting || isCartLoading"
            @click="handleCreateOrder"
            v-if="!isSubmitting"
          >
            {{ isSubmitting ? "Оформление..." : "Оформить заказ" }}
          </button>
          <Loader v-else text="Оформление заказа..." size="md" />

          <button
            class="btn-text btn-clear"
            @click="clearCart(accessToken)"
            :disabled="isCartLoading || isSubmitting"
          >
            Очистить корзину
          </button>
        </aside>
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
$success: #28a745;
$warning: #ffc107;

.cart-page {
  min-height: calc(100vh - 75px);
  padding: 40px 0;
  background: $dark-bg;
  color: $text;
  @media (max-width: 768px) {
    padding: 120px 0;
  }
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

// Заголовок
.cart-header {
  margin-bottom: 30px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 15px;

  @media (max-width: 768px) {
    flex-direction: column;
    align-items: flex-start;
  }
}

.cart-title {
  margin: 0;
  font-size: 2rem;
  font-weight: 700;
}

.cart-subtitle {
  margin: 0;
  color: $text-muted;
  font-size: 1.1rem;
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
  font-size: 0.95rem;

  .error-close {
    background: none;
    border: none;
    color: inherit;
    font-size: 1.5rem;
    cursor: pointer;
    padding: 0 5px;
    line-height: 1;

    &:hover {
      opacity: 0.8;
    }
  }
}

// Пустая корзина
.cart-empty {
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

// Контент корзины
.cart-content {
  display: grid;
  grid-template-columns: 1fr 380px;
  gap: 30px;
  align-items: start;

  @media (max-width: 992px) {
    grid-template-columns: 1fr;
  }
}

// Список товаров
.cart-items {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.cart-item {
  display: grid;
  grid-template-columns: 1fr auto 80px auto;
  gap: 20px;
  align-items: center;
  padding: 20px;
  background: $card-bg;
  border-radius: 12px;
  border: 1px solid $border-color;

  @media (max-width: 768px) {
    grid-template-columns: 70px 1fr;
    grid-template-areas:
      "image info"
      "image controls"
      "total total";
    gap: 15px;
  }
}

.cart-item-info {
  @media (max-width: 768px) {
    grid-area: info;
  }
}

.cart-item-name {
  margin: 0 0 5px;
  font-size: 1.1rem;
  font-weight: 600;
}

.cart-item-sku {
  margin: 0 0 8px;
  font-size: 0.85rem;
  color: $text-muted;
}

.cart-item-price {
  margin: 0 0 5px;
  font-size: 1.1rem;
  font-weight: 600;
  color: $accent-green;
}

.cart-item-stock {
  margin: 0;
  font-size: 0.85rem;
  color: $text-muted;

  &.low-stock {
    color: $warning;
  }
}

.cart-item-controls {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;

  @media (max-width: 768px) {
    grid-area: controls;
    flex-direction: row;
    justify-content: flex-end;
  }
}

.quantity-control {
  display: flex;
  align-items: center;
  gap: 8px;
  background: $input-bg;
  padding: 4px;
  border-radius: 8px;
}

.quantity-btn {
  width: 32px;
  height: 32px;
  border: none;
  background: transparent;
  color: $text;
  font-size: 1.2rem;
  font-weight: 600;
  padding: 0;
  cursor: pointer;
  border-radius: 6px;
  transition: background 0.2s;

  &:hover:not(:disabled) {
    background: $accent-red;
  }

  &:disabled {
    opacity: 0.4;
    cursor: not-allowed;
  }
}

.quantity-value {
  min-width: 30px;
  text-align: center;
  font-weight: 600;
  font-size: 1rem;
}

.btn-text {
  background: none;
  border: none;
  padding: 0;
  font-size: 0.9rem;
  cursor: pointer;
  transition: opacity 0.2s;

  &:hover:not(:disabled) {
    opacity: 0.8;
  }

  &:disabled {
    opacity: 0.4;
    cursor: not-allowed;
  }

  &.btn-danger {
    color: #ff6b6b;
  }

  &.btn-clear {
    color: #ff6b6b;
    display: block;
    margin: 0 auto;
  }

  &.btn-continue {
    color: $accent-green;
  }
}

.cart-item-total {
  font-size: 1.2rem;
  font-weight: 700;
  color: $accent-green;

  @media (max-width: 768px) {
    grid-area: total;
    text-align: right;
    padding-top: 10px;
    border-top: 1px solid $border-color;
  }
}

// Блок итогов
.cart-summary {
  position: sticky;
  top: 95px;
  padding: 25px;
  background: $card-bg;
  border-radius: 16px;
  border: 1px solid $border-color;
  height: fit-content;

  @media (max-width: 992px) {
    position: static;
  }

  h3 {
    margin: 0 0 20px;
    font-size: 1.3rem;
    padding-bottom: 15px;
    border-bottom: 1px solid $border-color;
  }
}

.summary-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 12px;
  font-size: 1rem;

  .free-shipping {
    color: $success;
    font-weight: 500;
  }
}

.summary-total {
  display: flex;
  justify-content: space-between;
  margin: 20px 0;
  padding: 15px 0;
  border-top: 2px solid $border-color;
  border-bottom: 2px solid $border-color;
  font-size: 1.2rem;

  .total-amount {
    font-size: 1.4rem;
    font-weight: 700;
    color: $accent-green;
  }
}

// Адрес доставки
.delivery-address {
  margin: 20px 0;

  label {
    display: block;
    margin-bottom: 8px;
    font-weight: 500;
    font-size: 0.95rem;
  }

  .input {
    width: calc(100% - 30px);
    padding: 12px 15px;
    background: $input-bg;
    border: 1px solid $border-color;
    border-radius: 8px;
    color: $text;
    font-size: 1rem;

    &:focus {
      outline: none;
      border-color: $accent-green;
      box-shadow: 0 0 0 3px rgba(46, 139, 87, 0.2);
    }

    &:disabled {
      opacity: 0.7;
      cursor: not-allowed;
    }

    &::placeholder {
      color: $text-muted;
    }
  }

  .input-hint {
    margin: 5px 0 0;
    font-size: 0.8rem;
    color: $text-muted;
  }
}

// Кнопки
.btn-primary {
  width: 100%;
  padding: 14px;
  background: $accent-green;
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 1.05rem;
  font-weight: 600;
  cursor: pointer;
  transition:
    background 0.2s,
    transform 0.1s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;

  &:hover:not(:disabled) {
    background: lighten($accent-green, 5%);
    transform: translateY(-1px);
  }

  &:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }
}

.btn-checkout {
  margin-bottom: 15px;
}

// Лоадер
.loader {
  width: 20px;
  height: 20px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;

  &-sm {
    width: 16px;
    height: 16px;
    border-width: 2px;
  }

  @keyframes spin {
    to {
      transform: rotate(360deg);
    }
  }
}
</style>

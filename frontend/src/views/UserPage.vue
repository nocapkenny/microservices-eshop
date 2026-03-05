<script setup>
import { ref, onMounted, onUnmounted } from "vue";
import { useRouter } from "vue-router";
import { useUserStore } from "../stores/user";
import { useCartStore } from "../stores/cart";
import { useOrderStore } from "../stores/order";
import Loader from "../components/ui/Loader.vue";

// ROUTER
const router = useRouter();

// STORE
const userStore = useUserStore();
const cartStore = useCartStore();
const orderStore = useOrderStore();

// REFS
const isLogin = ref(true);
const email = ref("");
const password = ref("");
const passwordConfirm = ref("");
const errors = ref({});
const isLoading = ref(false);

// METHODS
const validate = () => {
  const newErrors = {};

  if (!email.value) {
    newErrors.email = "Email обязателен";
  } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value)) {
    newErrors.email = "Некорректный email";
  }

  if (!password.value) {
    newErrors.password = "Пароль обязателен";
  } else if (password.value.length < 8) {
    newErrors.password = "Минимум 8 символов";
  }

  if (!isLogin.value) {
    if (!passwordConfirm.value) {
      newErrors.passwordConfirm = "Подтверждение обязательно";
    } else if (passwordConfirm.value !== password.value) {
      newErrors.passwordConfirm = "Пароли не совпадают";
    }
  }

  errors.value = newErrors;
  return Object.keys(newErrors).length === 0;
};

const handleSubmit = async () => {
  if (!validate()) return;

  isLoading.value = true;
  errors.value = {};

  try {
    if (isLogin.value) {
      userStore.user.email = email.value;
      userStore.user.password = password.value;
      await userStore.loginUser();
      await cartStore.getCart(userStore.accessToken);
      await orderStore.getOrders(userStore.accessToken);
    } else {
      userStore.user.email = email.value;
      userStore.user.password = password.value;
      userStore.user.password_confirm = passwordConfirm.value
      await userStore.registerUser();
    }
    router.push({ name: "catalog" });
  } catch (err) {
    if (err.response?.data?.detail) {
      errors.value.global = err.response.data.detail;
    } else if (err.message) {
      errors.value.global = err.message;
    } else {
      errors.value.global = "Произошла ошибка. Попробуйте позже.";
    }
  } finally {
    isLoading.value = false;
  }
};

const switchMode = () => {
  isLogin.value = !isLogin.value;
  email.value = "";
  password.value = "";
  passwordConfirm.value = "";
  errors.value = {};
};

onMounted(() => {
  if (userStore.isLoggedIn) {
    router.push({ name: "catalog" });
  }
});
</script>

<template>
  <main class="auth-page">
    <div class="auth-card">
      <h1 class="auth-title">
        {{ isLogin ? "Вход в аккаунт" : "Создать аккаунт" }}
      </h1>

      <div v-if="errors.global" class="error-global">
        {{ errors.global }}
      </div>

      <form class="auth-form" @submit.prevent="handleSubmit">
        <!-- Email -->
        <div class="form-group">
          <label for="email">Электронная почта</label>
          <input
            id="email"
            type="email"
            v-model="email"
            autocomplete="email"
            placeholder="example@mail.ru"
            :class="{ 'input-error': errors.email }"
            :disabled="isLoading"
          />
          <div v-if="errors.email" class="error-text">{{ errors.email }}</div>
        </div>

        <!-- Password -->
        <div class="form-group">
          <label for="password">Пароль</label>
          <input
            id="password"
            type="password"
            v-model="password"
            minlength="8"
            placeholder="••••••••"
            :class="{ 'input-error': errors.password }"
            :disabled="isLoading"
          />
          <div v-if="errors.password" class="error-text">
            {{ errors.password }}
          </div>
        </div>

        <!-- Password Confirm -->
        <div v-if="!isLogin" class="form-group">
          <label for="password-confirm">Подтвердите пароль</label>
          <input
            id="password-confirm"
            type="password"
            v-model="passwordConfirm"
            minlength="8"
            placeholder="••••••••"
            :class="{ 'input-error': errors.passwordConfirm }"
            :disabled="isLoading"
          />
          <div v-if="errors.passwordConfirm" class="error-text">
            {{ errors.passwordConfirm }}
          </div>
        </div>

        <button type="submit" class="btn-primary" v-if="!isLoading">
          {{ isLogin ? "Войти" : "Зарегистрироваться" }}
        </button>
        <Loader size="md" v-else />
      </form>

      <div class="auth-switch">
        <p>
          {{ isLogin ? "Нет аккаунта?" : "Уже есть аккаунт?" }}
          <button
            type="button"
            class="link"
            @click="switchMode"
            :disabled="isLoading"
          >
            {{ isLogin ? "Зарегистрироваться" : "Войти" }}
          </button>
        </p>
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

.auth-page {
  min-height: calc(100vh - 75px); 
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
  background: $dark-bg;
}

.auth-card {
  flex: 1;
  max-width: 450px;
  background: $card-bg;
  border-radius: 16px;
  padding: 2.5rem;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.4);

  @media (max-width: 768px) {
    max-width: 100%;
    padding: 2rem;
  }
}

.auth-title {
  margin: 0 0 1.5rem;
  font-size: 1.75rem;
  font-weight: 700;
  text-align: center;
  color: $text;
}

.error-global {
  background: rgba(255, 107, 107, 0.15);
  border: 1px solid #ff6b6b;
  color: #ff6b6b;
  padding: 0.75rem 1rem;
  border-radius: 8px;
  margin-bottom: 1.25rem;
  font-size: 0.9rem;
  text-align: center;
}

.auth-form {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;

  label {
    font-size: 0.95rem;
    font-weight: 500;
    color: $text;
  }

  input {
    padding: 0.85rem 1rem;
    border: 1px solid $border-color;
    border-radius: 10px;
    background: $input-bg;
    color: $text;
    font-size: 1rem;
    transition:
      border-color 0.2s,
      box-shadow 0.2s;

    &:focus {
      outline: none;
      border-color: $accent-red;
      box-shadow: 0 0 0 3px rgba(194, 42, 59, 0.25);
    }

    &:disabled {
      opacity: 0.7;
      cursor: not-allowed;
    }

    &::placeholder {
      color: $text-muted;
    }
  }
}

.input-error {
  border-color: #ff6b6b !important;
  background: #2a1a1a;
}

.error-text {
  color: #ff6b6b;
  font-size: 0.85rem;
  min-height: 1.2em;
}

.btn-primary {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 1rem;
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
  margin-top: 0.5rem;

  &:hover:not(:disabled) {
    background: #d03a4b;
    transform: translateY(-1px);
  }

  &:active:not(:disabled) {
    transform: translateY(0);
  }

  &:disabled {
    opacity: 0.7;
    cursor: not-allowed;
  }
}

.auth-switch {
  margin-top: 2rem;
  text-align: center;
  font-size: 1rem;
  color: $text-muted;

  .link {
    background: none;
    border: none;
    color: $accent-green;
    cursor: pointer;
    font-weight: 600;
    padding: 0;
    text-decoration: none;
    font-size: inherit;

    &:hover:not(:disabled) {
      text-decoration: underline;
      color: lighten($accent-green, 10%);
    }

    &:disabled {
      opacity: 0.6;
      cursor: not-allowed;
    }
  }
}
</style>

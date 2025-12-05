<script setup>
import { ref, defineEmits, watch } from "vue";
import { onMounted, onUnmounted } from "vue";
import { useUserStore } from "../../stores/user";

const emit = defineEmits(["close"]);

// STORE
const userStore = useUserStore();
const { registerUser, loginUser } = userStore;

// REFS
const isLogin = ref(true);
const email = ref("");
const password = ref("");
const passwordConfirm = ref("");
const errors = ref({});

// METHODS
const validate = () => {
  const newErrors = {};

  // Email
  if (!email.value) {
    newErrors.email = "Email обязателен";
  } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value)) {
    newErrors.email = "Некорректный email";
  }

  // Password
  if (!password.value) {
    newErrors.password = "Пароль обязателен";
  } else if (password.value.length < 8) {
    newErrors.password = "Минимум 8 символов";
  }

  // Password confirm (только при регистрации)
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

  try {
    if (isLogin.value) {
      userStore.user.email = email.value;
      userStore.user.password = password.value;
      await loginUser(email.value, password.value);
    } else {
      userStore.user.email = email.value;
      userStore.user.password = password.value;
      userStore.user.password_confirm = passwordConfirm.value;
      await registerUser(email.value, password.value);
    }
    emit("close"); // закрываем после успеха
  } catch (err) {
    // Можно обработать ошибку от API (например, "пользователь уже существует")
    errors.value.global = err.message || "Произошла ошибка";
  }
};

const switchMode = () => {
  isLogin.value = !isLogin.value;
  // Сбрасываем поля и ошибки при переключении
  email.value = "";
  password.value = "";
  passwordConfirm.value = "";
  errors.value = {};
};

const closeModal = () => {
  emit("close");
};

const handleEscape = (e) => {
  if (e.key === "Escape") closeModal();
};

onMounted(() => window.addEventListener("keydown", handleEscape));
onUnmounted(() => window.removeEventListener("keydown", handleEscape));
</script>

<template>
  <div class="modal" @click="closeModal">
    <div class="modal-overlay"></div>
    <div class="modal-content" @click.stop>
      <button class="modal-close" @click="closeModal">&times;</button>

      <h2 class="modal-title">
        {{ isLogin ? "Вход в аккаунт" : "Создать аккаунт" }}
      </h2>

      <!-- Глобальная ошибка (например, от API) -->
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
            :class="{ 'input-error': errors.email }"
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
            minlength="6"
            :class="{ 'input-error': errors.password }"
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
            minlength="6"
            :class="{ 'input-error': errors.passwordConfirm }"
          />
          <div v-if="errors.passwordConfirm" class="error-text">
            {{ errors.passwordConfirm }}
          </div>
        </div>

        <button
          type="submit"
          class="btn-primary"
          :disabled="Object.keys(errors).length > 0 && !errors.global"
        >
          {{ isLogin ? "Войти" : "Зарегистрироваться" }}
        </button>
      </form>

      <div class="auth-switch">
        <p>
          {{ isLogin ? "Нет аккаунта?" : "Уже есть аккаунт?" }}
          <button type="button" class="link" @click="switchMode">
            {{ isLogin ? "Зарегистрироваться" : "Войти" }}
          </button>
        </p>
      </div>
    </div>
  </div>
</template>

<style lang="scss">
$dark-bg: #121212;
$card-bg: #1e1e1e;
$text: #e0e0e0;
$accent-red: #c22a3b;
$accent-green: #2e8b57;
.error-global {
  color: #ff6b6b;
  text-align: center;
  margin-bottom: 1rem;
  font-size: 0.9rem;
}

.input-error {
  border-color: #ff6b6b !important;
  background: #2a1a1a;
}

.error-text {
  color: #ff6b6b;
  font-size: 0.85rem;
  margin-top: 0.25rem;
}
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  z-index: 1000;
  display: flex;
  justify-content: center;
  align-items: center;

  &-overlay {
    position: absolute;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.7);
    backdrop-filter: blur(4px);
  }

  &-content {
    position: relative;
    background: $card-bg;
    color: $text;
    border-radius: 12px;
    padding: 2rem;
    width: 90%;
    max-width: 420px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
    z-index: 1;
    animation: modalSlideIn 0.3s ease-out;

    @keyframes modalSlideIn {
      from {
        opacity: 0;
        transform: translateY(-20px);
      }
      to {
        opacity: 1;
        transform: translateY(0);
      }
    }
  }

  &-close {
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

    &:hover {
      color: #fff;
      background: rgba(255, 255, 255, 0.1);
    }
  }

  &-title {
    margin-top: 0;
    margin-bottom: 1.5rem;
    font-size: 1.5rem;
    font-weight: 600;
    text-align: center;
  }
}

.auth-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;

  label {
    font-size: 0.9rem;
    font-weight: 500;
  }

  input {
    padding: 0.75rem;
    border: 1px solid #333;
    border-radius: 8px;
    background: #2a2a2a;
    color: $text;
    font-size: 1rem;

    &:focus {
      outline: none;
      border-color: $accent-red;
      box-shadow: 0 0 0 2px rgba(194, 42, 59, 0.3);
    }
  }
}

.btn-primary {
  padding: 0.85rem;
  background: $accent-red;
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

.auth-switch {
  margin-top: 1.5rem;
  text-align: center;
  font-size: 0.95rem;
  color: #aaa;

  .link {
    background: none;
    border: none;
    color: $accent-green;
    cursor: pointer;
    font-weight: 600;
    padding: 0;
    text-decoration: none;

    &:hover {
      text-decoration: underline;
    }
  }
}
</style>

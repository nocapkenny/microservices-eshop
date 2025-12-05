import { defineStore } from "pinia";
import { useCartStore } from "./cart";
import { ref } from "vue";
import axios from "axios";

export const useUserStore = defineStore("user", () => {
  const cartStore = useCartStore();
  // STATE
  const user = ref({
    email: null,
    password: null,
    password_confirm: null,
    first_name: "Юзер",
    last_name: "Тест",
    phone: "+7 999 999 99 99",
    date_of_birth: "2000-01-01",
  });
  const isLoggedIn = ref(false);

  const accessToken = ref(localStorage.getItem("access") || null);

  // ACTIONS
  const registerUser = async () => {
    try {
      console.log(user.value);
      const { data } = await axios.post(
        "/api/user/register/",
        user.value
      );
      console.log(data);
      accessToken.value = data.access;
      localStorage.setItem("access", data.access);
      user.value = data.user;
      isLoggedIn.value = true;
      await getUser();
      cartStore.getCart();
    } catch (e) {
      console.log(e);
    }
  };

  const getUser = async () => {
    try {
      const { data } = await axios.get(
        "/api/user/profile/",
        {
          headers: {
            Authorization: `Bearer ${accessToken.value}`,
          },
        }
      );
      user.value = data;
      isLoggedIn.value = true;
      console.log(user.value);
    } catch (e) {
      console.log(e);
    }
  };

  const loginUser = async () => {
    try {
      const { data } = await axios.post(
        "/api/user/login/",
        {
          email: user.value.email,
          password: user.value.password,
        }
      );
      console.log(data);
      accessToken.value = data.access;
      localStorage.setItem("access", data.access);
      user.value = data.user;
      isLoggedIn.value = true;
      cartStore.getCart();
    } catch (e) {
      console.log(e);
    }
  };

  return {
    user,
    registerUser,
    loginUser,
    getUser,
    isLoggedIn,
  };
});

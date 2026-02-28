import { defineStore } from "pinia";
import { useCartStore } from "./cart";
import { ref } from "vue";
import axios from "axios";
import { notyf } from "../plugins/notyf";

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
      console.log(accessToken.value);
      user.value = data.user;
      isLoggedIn.value = true;
      await getUser();
      await cartStore.getCart(accessToken.value);
      notyf.success("Вы успешно зарегистрировались!");
    } catch (e) {
      console.log(e);
      const errors = e.response.data;
      console.log(errors)
      notyf.error(e.response.data[Object.keys(errors)[0]][0])
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
      notyf.error('Ошибка получения данных')
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
      cartStore.getCart(accessToken.value);
      notyf.success("Вы успешно авторизовались!");
    } catch (e) {
      console.log(e);
      notyf.error(e.response.data.error)
    }
  };

  return {
    user,
    registerUser,
    loginUser,
    getUser,
    isLoggedIn,
    accessToken
  };
});

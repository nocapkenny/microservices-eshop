import { createWebHistory, createRouter } from "vue-router";

// Pages
import CartPage from "../views/CartPage.vue";
import OrderPage from "../views/OrderPage.vue";
import CatalogPage from "../views/CatalogPage.vue";
import UserPage from "../views/UserPage.vue";

const routes = [
    { path: '/', component: CatalogPage, name: 'catalog' },
    { path: '/cart', component: CartPage, name: 'cart' },
    { path: '/orders', component: OrderPage, name: 'orders' },
    { path: '/me', component: UserPage, name: 'user' },
]

export const router = createRouter({
    history: createWebHistory(),
    routes
})
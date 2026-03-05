import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { autoAnimatePlugin } from '@formkit/auto-animate/vue'
import { router } from './router/router';
import notyfPlugin from './plugins/notyf';
import './style.css'
import './assets/styles/main.scss'
import App from './App.vue'

const app = createApp(App)
app.use(createPinia())
app.use(router)
app.use(notyfPlugin);
app.use(autoAnimatePlugin)
app.mount('#app')
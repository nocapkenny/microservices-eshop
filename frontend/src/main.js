import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { autoAnimatePlugin } from '@formkit/auto-animate/vue'
import notyfPlugin from './plugins/notyf';
import './style.css'
import './assets/styles/main.scss'
import App from './App.vue'

const app = createApp(App)
app.use(createPinia())
app.use(notyfPlugin);
app.use(autoAnimatePlugin)
app.mount('#app')
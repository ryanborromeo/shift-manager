import './assets/index.css'
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import { useDarkModeStore } from './stores/darkMode.js'

const app = createApp(App)

app.use(createPinia())
app.use(router)

// Initialize dark mode
const darkModeStore = useDarkModeStore()
darkModeStore.set(true) // Set to true for dark mode by default

app.mount('#app')

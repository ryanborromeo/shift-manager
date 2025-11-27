import './assets/index.css'
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import { useDarkModeStore } from './stores/darkMode.js'
import { useSettingsStore } from './stores/settingsStore'
import { useWorkerStore } from './stores/workerStore'
import { useShiftStore } from './stores/shiftStore'

// Create app instance
const app = createApp(App)

// Initialize Pinia
const pinia = createPinia()
app.use(pinia)
app.use(router)

// Initialize dark mode
const darkModeStore = useDarkModeStore()
darkModeStore.set(true) // Set to true for dark mode by default

// Initialize stores and fetch initial data
const initializeApp = async () => {
  try {
    const settingsStore = useSettingsStore()
    await settingsStore.fetchTimezone()
    
    // Pre-fetch data that might be needed globally
    const workerStore = useWorkerStore()
    const shiftStore = useShiftStore()
    
    // Fetch initial data in the background
    Promise.all([
      workerStore.fetchWorkers().catch(console.error),
      shiftStore.fetchShifts().catch(console.error)
    ])
  } catch (error) {
    console.error('Failed to initialize app:', error)
  }
}

// Mount the app
app.mount('#app')

// Initialize app data
initializeApp()

// Global error handler
app.config.errorHandler = (err, instance, info) => {
  console.error('Vue error:', { err, instance, info })
  // Here you could also log errors to an error tracking service
}

// Global properties can be accessed via app.config.globalProperties
app.config.globalProperties.$filters = {
  formatDate(date: string) {
    return new Date(date).toLocaleDateString()
  },
  formatDateTime(date: string) {
    return new Date(date).toLocaleString()
  }
}

export { app, router, pinia }

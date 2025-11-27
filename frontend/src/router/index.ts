import { createRouter, createWebHistory } from 'vue-router'
import WorkersView from '@/views/WorkersView.vue'
import ShiftsView from '@/views/ShiftsView.vue'
import SettingsView from '@/views/SettingsView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: '/workers'
    },
    {
      path: '/workers',
      name: 'workers',
      component: WorkersView,
      meta: {
        transition: 'fade'
      }
    },
    {
      path: '/shifts',
      name: 'shifts',
      component: ShiftsView,
      meta: {
        transition: 'fade'
      }
    },
    {
      path: '/settings',
      name: 'settings',
      component: SettingsView,
      meta: {
        transition: 'fade'
      }
    }
  ]
})

export default router

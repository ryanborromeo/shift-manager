import { createRouter, createWebHistory } from 'vue-router'
import DashboardView from '@/views/DashboardView.vue'
import WorkersView from '@/views/WorkersView.vue'
import ShiftsView from '@/views/ShiftsView.vue'
import SettingsView from '@/views/SettingsView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'dashboard',
      component: DashboardView
    },
    {
      path: '/workers',
      name: 'workers',
      component: WorkersView
    },
    {
      path: '/shifts',
      name: 'shifts',
      component: ShiftsView
    },
    {
      path: '/settings',
      name: 'settings',
      component: SettingsView
    }
  ]
})

export default router

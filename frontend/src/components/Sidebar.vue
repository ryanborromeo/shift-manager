<template>
  <nav class="w-64 bg-gray-900 text-white h-screen flex flex-col">
    <div class="p-6 border-b border-gray-700">
      <h1 class="text-2xl font-bold">Shift Manager</h1>
    </div>
    
    <div class="flex-1 p-4 space-y-2">
      <router-link
        v-for="item in navigationItems"
        :key="item.path"
        :to="item.path"
        v-slot="{ isActive }"
        custom
      >
        <Button
          @click="$router.push(item.path)"
          :class="[
            'w-full justify-start h-9 px-4 py-2',
            isActive 
              ? 'bg-gray-700 text-white' 
              : 'text-gray-300 hover:text-white hover:bg-gray-800'
          ]"
        >
          <component :is="item.icon" class="mr-3 h-5 w-5" />
          {{ item.label }}
        </Button>
      </router-link>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { LayoutDashboard, Users, Calendar, Settings } from 'lucide-vue-next'
import Button from '@/components/ui/button/Button.vue'

const navigationItems = [
  { path: '/', label: 'Dashboard', icon: LayoutDashboard },
  { path: '/workers', label: 'Workers', icon: Users },
  { path: '/shifts', label: 'Shifts', icon: Calendar },
  { path: '/settings', label: 'Settings', icon: Settings }
]
</script>

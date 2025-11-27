<script setup>
import { containerMaxW } from '@/config.js'
import BaseLevel from '@/components/BaseLevel.vue'

const year = new Date().getFullYear()
</script>

<template>
  <footer class="px-6 py-2" :class="containerMaxW">
    <BaseLevel>
      <div class="text-center md:text-left">
        <slot>
          <b>&copy;{{ year }} Shift Manager</b>
        </slot>
      </div>
    </BaseLevel>
  </footer>
</template>

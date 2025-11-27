import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Ref } from 'vue'

export const useDarkModeStore = defineStore('darkMode', () => {
  // Initialize from localStorage, default to true (dark mode)
  const isEnabled: Ref<boolean> = ref(
    typeof localStorage !== 'undefined'
      ? localStorage.getItem('darkMode') === '1' || localStorage.getItem('darkMode') === null
      : true
  )
  
  const isInProgress: Ref<boolean> = ref(false)

  function set(payload: boolean | null = null): void {
    isInProgress.value = true
    isEnabled.value = payload !== null ? payload : !isEnabled.value

    if (typeof document !== 'undefined') {
      document.body.classList[isEnabled.value ? 'add' : 'remove']('dark-scrollbars')

      document.documentElement.classList[isEnabled.value ? 'add' : 'remove'](
        'dark',
        'dark-scrollbars-compat',
      )
    }

    setTimeout(() => {
      isInProgress.value = false
    }, 200)

    // Persist dark mode setting to localStorage
    if (typeof localStorage !== 'undefined') {
      localStorage.setItem('darkMode', isEnabled.value ? '1' : '0')
    }
  }

  return {
    isEnabled,
    isInProgress,
    set,
  }
})

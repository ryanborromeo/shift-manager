<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { mdiCog, mdiContentSave } from '@mdi/js'
import SectionMain from '@/components/SectionMain.vue'
import CardBox from '@/components/CardBox.vue'
import SectionTitleLineWithButton from '@/components/SectionTitleLineWithButton.vue'
import BaseButton from '@/components/BaseButton.vue'
import FormField from '@/components/FormField.vue'
import FormControl from '@/components/FormControl.vue'
import NotificationBar from '@/components/NotificationBar.vue'
import { useSettingsStore } from '@/stores/settingsStore'

const settingsStore = useSettingsStore()
const timezone = ref('')
const isSaving = ref(false)
const successMessage = ref('')
const errorMessage = ref('')

// Common timezone options (IANA timezone names)
const timezoneOptions = [
  { id: 'UTC', label: 'UTC' },
  { id: 'America/New_York', label: 'America/New_York (EST/EDT)' },
  { id: 'America/Chicago', label: 'America/Chicago (CST/CDT)' },
  { id: 'America/Denver', label: 'America/Denver (MST/MDT)' },
  { id: 'America/Los_Angeles', label: 'America/Los_Angeles (PST/PDT)' },
  { id: 'Europe/London', label: 'Europe/London (GMT/BST)' },
  { id: 'Europe/Paris', label: 'Europe/Paris (CET/CEST)' },
  { id: 'Asia/Tokyo', label: 'Asia/Tokyo (JST)' },
  { id: 'Asia/Shanghai', label: 'Asia/Shanghai (CST)' },
  { id: 'Australia/Sydney', label: 'Australia/Sydney (AEST/AEDT)' }
]

onMounted(async () => {
  try {
    await settingsStore.fetchTimezone()
    timezone.value = settingsStore.timezone
  } catch (error) {
    errorMessage.value = 'Failed to load timezone settings'
    console.error('Error fetching timezone:', error)
  }
})

const saveSettings = async () => {
  isSaving.value = true
  successMessage.value = ''
  errorMessage.value = ''
  
  try {
    await settingsStore.updateTimezone(timezone.value)
    successMessage.value = 'Settings saved successfully!'
    setTimeout(() => {
      successMessage.value = ''
    }, 3000)
  } catch (error: any) {
    errorMessage.value = error.response?.data?.detail || 'Failed to save settings'
    setTimeout(() => {
      errorMessage.value = ''
    }, 5000)
  } finally {
    isSaving.value = false
  }
}
</script>

<template>
  <SectionMain>
    <SectionTitleLineWithButton :icon="mdiCog" title="Settings" main>
      <BaseButton
        :icon="mdiContentSave"
        label="Save Changes"
        color="success"
        rounded-full
        :disabled="isSaving"
        @click="saveSettings"
      />
    </SectionTitleLineWithButton>

    <NotificationBar 
      v-if="successMessage" 
      color="success" 
      :outline="false"
    >
      {{ successMessage }}
    </NotificationBar>

    <NotificationBar 
      v-if="errorMessage" 
      color="danger" 
      :outline="false"
    >
      {{ errorMessage }}
    </NotificationBar>

    <CardBox title="Timezone Settings" class="mb-6">
      <FormField 
        label="Application Timezone"
        help="Set the timezone for displaying shift times and scheduling"
      >
        <FormControl
          v-model="timezone"
          :options="timezoneOptions"
          :disabled="settingsStore.loading"
        />
      </FormField>
    </CardBox>
  </SectionMain>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
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
const timezone = computed({
  get: () => settingsStore.timezone,
  set: (val: string) => {
    settingsStore.timezone = val
  }
})
const isSaving = ref(false)
const successMessage = ref('')
const errorMessage = ref('')

const timezoneOptions = computed(() =>
  settingsStore.availableTimezones.map((tz) => ({
    id: tz,
    label: tz
  }))
)

const hasTimezoneInfo = computed(() => Boolean(settingsStore.timezoneInfo))

const formatUtcOffset = (offsetSeconds?: number) => {
  if (offsetSeconds === undefined || offsetSeconds === null) return 'N/A'
  const hours = Math.floor(Math.abs(offsetSeconds) / 3600)
  const minutes = Math.floor((Math.abs(offsetSeconds) % 3600) / 60)
  const sign = offsetSeconds >= 0 ? '+' : '-'
  return `${sign}${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}`
}

const formattedCurrentTime = computed(() => {
  const current = settingsStore.timezoneInfo?.currentLocalTime
  if (!current) return 'Unavailable'
  try {
    return new Date(current).toLocaleString()
  } catch (error) {
    return current
  }
})

const formattedUtcOffset = computed(() => {
  const offset = settingsStore.timezoneInfo?.currentUtcOffset?.seconds
  return formatUtcOffset(offset)
})

const dstStatus = computed(() => {
  const info = settingsStore.timezoneInfo
  if (!info) return 'Unavailable'
  if (!info.hasDayLightSaving) return 'Not observed'
  return info.isDayLightSavingActive ? 'Active' : 'Inactive'
})

onMounted(async () => {
  try {
    await settingsStore.fetchAvailableTimezones()
    await settingsStore.fetchTimezone()
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
    successMessage.value = 'Timezone updated successfully!'
    setTimeout(() => {
      successMessage.value = ''
    }, 3000)
  } catch (error: any) {
    errorMessage.value = error.response?.data?.detail || 'Failed to update timezone'
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
          :disabled="settingsStore.loading || !timezoneOptions.length"
        />
      </FormField>
    </CardBox>

    <CardBox
      v-if="hasTimezoneInfo"
      title="Timezone Details"
      class="mb-6"
    >
      <div class="grid gap-4 md:grid-cols-2">
        <div>
          <p class="text-sm text-gray-500 dark:text-gray-400">Current Local Time</p>
          <p class="text-lg font-semibold">{{ formattedCurrentTime }}</p>
        </div>
        <div>
          <p class="text-sm text-gray-500 dark:text-gray-400">Current UTC Offset</p>
          <p class="text-lg font-semibold">{{ formattedUtcOffset }}</p>
        </div>
        <div>
          <p class="text-sm text-gray-500 dark:text-gray-400">Daylight Saving</p>
          <p class="text-lg font-semibold">{{ dstStatus }}</p>
        </div>
        <div>
          <p class="text-sm text-gray-500 dark:text-gray-400">Timezone Identifier</p>
          <p class="text-lg font-semibold">{{ settingsStore.timezoneInfo?.timeZone ?? 'Unknown' }}</p>
        </div>
      </div>
    </CardBox>
  </SectionMain>
</template>

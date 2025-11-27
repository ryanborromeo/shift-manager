<script setup lang="ts">
import { ref } from 'vue'
import { mdiCog, mdiContentSave, mdiBell, mdiPalette, mdiClock } from '@mdi/js'
import SectionMain from '@/components/SectionMain.vue'
import CardBox from '@/components/CardBox.vue'
import SectionTitleLineWithButton from '@/components/SectionTitleLineWithButton.vue'
import BaseButton from '@/components/BaseButton.vue'
import BaseIcon from '@/components/BaseIcon.vue'
import FormField from '@/components/FormField.vue'
import FormControl from '@/components/FormControl.vue'
import FormCheckRadio from '@/components/FormCheckRadio.vue'

const settings = ref({
  appName: 'Shift Manager',
  timezone: 'UTC',
  dateFormat: 'YYYY-MM-DD',
  emailNotifications: true,
  pushNotifications: false,
  shiftReminders: true,
  theme: 'light',
  language: 'en',
  defaultShiftDuration: 8,
  breakDuration: 30,
  overtimeRate: 1.5
})

const timezoneOptions = [
  { id: 'UTC', label: 'UTC' },
  { id: 'EST', label: 'Eastern Time' },
  { id: 'PST', label: 'Pacific Time' },
  { id: 'CST', label: 'Central Time' }
]

const dateFormatOptions = [
  { id: 'YYYY-MM-DD', label: '2024-01-15' },
  { id: 'MM/DD/YYYY', label: '01/15/2024' },
  { id: 'DD/MM/YYYY', label: '15/01/2024' }
]

const themeOptions = [
  { id: 'light', label: 'Light' },
  { id: 'dark', label: 'Dark' },
  { id: 'auto', label: 'Auto' }
]

const languageOptions = [
  { id: 'en', label: 'English' },
  { id: 'es', label: 'Spanish' },
  { id: 'fr', label: 'French' }
]
</script>

<template>
  <SectionMain>
    <SectionTitleLineWithButton :icon="mdiCog" title="Settings" main>
      <BaseButton
        :icon="mdiContentSave"
        label="Save Changes"
        color="success"
        rounded-full
      />
    </SectionTitleLineWithButton>

    <div class="grid grid-cols-1 gap-6 lg:grid-cols-2">
      <CardBox title="General Settings">
        <FormField label="Application Name">
          <FormControl
            v-model="settings.appName"
            placeholder="Shift Manager"
          />
        </FormField>

        <FormField label="Timezone">
          <FormControl
            v-model="settings.timezone"
            :options="timezoneOptions"
          />
        </FormField>

        <FormField label="Date Format">
          <FormControl
            v-model="settings.dateFormat"
            :options="dateFormatOptions"
          />
        </FormField>
      </CardBox>

      <CardBox title="Notification Settings">
        <FormField label="Email Notifications">
          <FormCheckRadio
            v-model="settings.emailNotifications"
            name="emailNotifications"
            type="switch"
          />
        </FormField>

        <FormField label="Push Notifications">
          <FormCheckRadio
            v-model="settings.pushNotifications"
            name="pushNotifications"
            type="switch"
          />
        </FormField>

        <FormField label="Shift Reminders">
          <FormCheckRadio
            v-model="settings.shiftReminders"
            name="shiftReminders"
            type="switch"
          />
        </FormField>
      </CardBox>

      <CardBox title="Appearance">
        <FormField label="Theme">
          <FormControl
            v-model="settings.theme"
            :options="themeOptions"
          />
        </FormField>

        <FormField label="Language">
          <FormControl
            v-model="settings.language"
            :options="languageOptions"
          />
        </FormField>
      </CardBox>

      <CardBox title="Shift Settings">
        <FormField label="Default Shift Duration">
          <FormControl
            v-model="settings.defaultShiftDuration"
            type="number"
            placeholder="8"
          />
        </FormField>

        <FormField label="Break Duration">
          <FormControl
            v-model="settings.breakDuration"
            type="number"
            placeholder="30"
          />
        </FormField>

        <FormField label="Overtime Rate">
          <FormControl
            v-model="settings.overtimeRate"
            type="number"
            step="0.1"
            placeholder="1.5"
          />
        </FormField>
      </CardBox>
    </div>
  </SectionMain>
</template>

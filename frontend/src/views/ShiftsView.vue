<script setup lang="ts">
import { ref } from 'vue'
import { mdiCalendarClock, mdiPlus, mdiMagnify, mdiCalendar } from '@mdi/js'
import SectionMain from '@/components/SectionMain.vue'
import CardBox from '@/components/CardBox.vue'
import SectionTitleLineWithButton from '@/components/SectionTitleLineWithButton.vue'
import BaseButton from '@/components/BaseButton.vue'
import BaseIcon from '@/components/BaseIcon.vue'
import FormControl from '@/components/FormControl.vue'

const searchQuery = ref('')
</script>

<template>
  <SectionMain>
    <SectionTitleLineWithButton :icon="mdiCalendarClock" title="Shifts" main>
      <BaseButton
        :icon="mdiPlus"
        label="Add Shift"
        color="info"
        rounded-full
      />
    </SectionTitleLineWithButton>

    <CardBox class="mb-6" has-table>
      <div class="mb-4 flex items-center justify-between">
        <FormControl
          v-model="searchQuery"
          placeholder="Search shifts..."
          :icon="mdiMagnify"
          transparent
          borderless
        />
        <BaseButton
          :icon="mdiCalendar"
          label="Calendar View"
          color="light"
          small
        />
      </div>

      <div class="overflow-x-auto">
        <table class="w-full">
          <thead>
            <tr>
              <th class="text-left p-4 font-semibold">Date</th>
              <th class="text-left p-4 font-semibold">Worker</th>
              <th class="text-left p-4 font-semibold">Shift</th>
              <th class="text-left p-4 font-semibold">Department</th>
              <th class="text-left p-4 font-semibold">Status</th>
              <th class="text-left p-4 font-semibold">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr class="border-t dark:border-slate-700">
              <td class="p-4">2024-01-15</td>
              <td class="p-4">John Doe</td>
              <td class="p-4">09:00 - 17:00</td>
              <td class="p-4">Engineering</td>
              <td class="p-4">
                <span class="inline-flex items-center px-2 py-1 text-xs font-medium text-green-800 bg-green-100 rounded-full dark:bg-green-900 dark:text-green-200">
                  Scheduled
                </span>
              </td>
              <td class="p-4">
                <BaseButton color="info" small label="Edit" />
              </td>
            </tr>
            <tr class="border-t dark:border-slate-700">
              <td class="p-4">2024-01-15</td>
              <td class="p-4">Jane Smith</td>
              <td class="p-4">14:00 - 22:00</td>
              <td class="p-4">Marketing</td>
              <td class="p-4">
                <span class="inline-flex items-center px-2 py-1 text-xs font-medium text-blue-800 bg-blue-100 rounded-full dark:bg-blue-900 dark:text-blue-200">
                  In Progress
                </span>
              </td>
              <td class="p-4">
                <BaseButton color="info" small label="Edit" />
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </CardBox>
  </SectionMain>
</template>

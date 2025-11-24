<script setup lang="ts">
import { ref } from 'vue'
import { mdiAccountGroup, mdiPlus, mdiMagnify } from '@mdi/js'
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
    <SectionTitleLineWithButton :icon="mdiAccountGroup" title="Workers" main>
      <BaseButton
        :icon="mdiPlus"
        label="Add Worker"
        color="info"
        rounded-full
      />
    </SectionTitleLineWithButton>

    <CardBox class="mb-6" has-table>
      <div class="mb-4 flex items-center justify-between">
        <FormControl
          v-model="searchQuery"
          placeholder="Search workers..."
          :icon="mdiMagnify"
          transparent
          borderless
        />
      </div>

      <div class="overflow-x-auto">
        <table class="w-full">
          <thead>
            <tr>
              <th class="text-left p-4 font-semibold">Name</th>
              <th class="text-left p-4 font-semibold">Email</th>
              <th class="text-left p-4 font-semibold">Department</th>
              <th class="text-left p-4 font-semibold">Status</th>
              <th class="text-left p-4 font-semibold">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr class="border-t dark:border-slate-700">
              <td class="p-4">John Doe</td>
              <td class="p-4">john.doe@example.com</td>
              <td class="p-4">Engineering</td>
              <td class="p-4">
                <span class="inline-flex items-center px-2 py-1 text-xs font-medium text-green-800 bg-green-100 rounded-full dark:bg-green-900 dark:text-green-200">
                  Active
                </span>
              </td>
              <td class="p-4">
                <BaseButton color="info" small label="Edit" />
              </td>
            </tr>
            <tr class="border-t dark:border-slate-700">
              <td class="p-4">Jane Smith</td>
              <td class="p-4">jane.smith@example.com</td>
              <td class="p-4">Marketing</td>
              <td class="p-4">
                <span class="inline-flex items-center px-2 py-1 text-xs font-medium text-green-800 bg-green-100 rounded-full dark:bg-green-900 dark:text-green-200">
                  Active
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

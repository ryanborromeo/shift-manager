<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { mdiCalendarClock, mdiPlus, mdiMagnify, mdiCalendar } from '@mdi/js'
import SectionMain from '@/components/SectionMain.vue'
import CardBox from '@/components/CardBox.vue'
import SectionTitleLineWithButton from '@/components/SectionTitleLineWithButton.vue'
import BaseButton from '@/components/BaseButton.vue'
import BaseIcon from '@/components/BaseIcon.vue'
import FormControl from '@/components/FormControl.vue'
import { useShiftStore } from '@/stores/shiftStore'
import { useWorkerStore } from '@/stores/workerStore'

const searchQuery = ref('')
const shiftStore = useShiftStore()
const workerStore = useWorkerStore()

// Fetch data on mount
onMounted(async () => {
  try {
    await Promise.all([
      shiftStore.fetchShifts(),
      workerStore.fetchWorkers()
    ])
  } catch (error) {
    console.error('Error fetching shifts:', error)
  }
})

// Helper function to format date
const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString()
}

// Helper function to format time
const formatTime = (dateString: string) => {
  return new Date(dateString).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

// Get worker name by ID
const getWorkerName = (workerId: number) => {
  const worker = workerStore.workers.find(w => w.id === workerId)
  return worker ? worker.name : 'Unknown'
}

// Get worker department by ID
const getWorkerDepartment = (workerId: number) => {
  const worker = workerStore.workers.find(w => w.id === workerId)
  return worker ? worker.department : 'N/A'
}

// Get shift status
const getShiftStatus = (startTime: string, endTime: string) => {
  const now = new Date()
  const start = new Date(startTime)
  const end = new Date(endTime)
  
  if (now < start) {
    return { label: 'Scheduled', color: 'green' }
  } else if (now >= start && now <= end) {
    return { label: 'In Progress', color: 'blue' }
  } else {
    return { label: 'Completed', color: 'gray' }
  }
}

// Filter shifts based on search query
const filteredShifts = computed(() => {
  if (!searchQuery.value) {
    return shiftStore.shifts
  }
  const query = searchQuery.value.toLowerCase()
  return shiftStore.shifts.filter(shift => {
    const workerName = getWorkerName(shift.worker_id).toLowerCase()
    const department = getWorkerDepartment(shift.worker_id).toLowerCase()
    const date = formatDate(shift.start_time).toLowerCase()
    return workerName.includes(query) || department.includes(query) || date.includes(query)
  })
})
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
            <tr v-if="filteredShifts.length === 0">
              <td colspan="6" class="p-8 text-center text-gray-500">
                No shifts found
              </td>
            </tr>
            <tr 
              v-for="shift in filteredShifts" 
              :key="shift.id"
              class="border-t dark:border-slate-700"
            >
              <td class="p-4">{{ formatDate(shift.start_time) }}</td>
              <td class="p-4">{{ getWorkerName(shift.worker_id) }}</td>
              <td class="p-4">{{ formatTime(shift.start_time) }} - {{ formatTime(shift.end_time) }}</td>
              <td class="p-4">{{ getWorkerDepartment(shift.worker_id) }}</td>
              <td class="p-4">
                <span 
                  :class="`inline-flex items-center px-2 py-1 text-xs font-medium rounded-full
                    ${getShiftStatus(shift.start_time, shift.end_time).color === 'green' ? 'text-green-800 bg-green-100 dark:bg-green-900 dark:text-green-200' : ''}
                    ${getShiftStatus(shift.start_time, shift.end_time).color === 'blue' ? 'text-blue-800 bg-blue-100 dark:bg-blue-900 dark:text-blue-200' : ''}
                    ${getShiftStatus(shift.start_time, shift.end_time).color === 'gray' ? 'text-gray-800 bg-gray-100 dark:bg-gray-900 dark:text-gray-200' : ''}
                  `"
                >
                  {{ getShiftStatus(shift.start_time, shift.end_time).label }}
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

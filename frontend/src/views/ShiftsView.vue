<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { mdiCalendarClock, mdiPlus, mdiMagnify, mdiPencil, mdiTrashCan } from '@mdi/js'
import SectionMain from '@/components/SectionMain.vue'
import CardBox from '@/components/CardBox.vue'
import CardBoxModal from '@/components/CardBoxModal.vue'
import SectionTitleLineWithButton from '@/components/SectionTitleLineWithButton.vue'
import BaseButton from '@/components/BaseButton.vue'
import BaseButtons from '@/components/BaseButtons.vue'
import FormControl from '@/components/FormControl.vue'
import FormField from '@/components/FormField.vue'
import NotificationBar from '@/components/NotificationBar.vue'
import { useShiftStore } from '@/stores/shiftStore'
import { useWorkerStore } from '@/stores/workerStore'
import type { Shift } from '@/types'

const searchQuery = ref('')
const shiftStore = useShiftStore()
const workerStore = useWorkerStore()
const isModalActive = ref(false)
const isDeleteModalActive = ref(false)
const modalMode = ref<'create' | 'edit'>('create')
const shiftForm = ref({ 
  worker_id: 0, 
  start: '', 
  end: '' 
})
const selectedShift = ref<Shift | null>(null)
const successMessage = ref('')
const errorMessage = ref('')

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

// Format datetime for input field (ISO 8601 local format)
const formatDateTimeForInput = (dateString: string) => {
  const date = new Date(dateString)
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  const hours = String(date.getHours()).padStart(2, '0')
  const minutes = String(date.getMinutes()).padStart(2, '0')
  return `${year}-${month}-${day}T${hours}:${minutes}`
}

// Get worker name by ID
const getWorkerName = (workerId: number) => {
  const worker = workerStore.workers.find(w => w.id === workerId)
  return worker ? worker.name : 'Unknown'
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
    const date = formatDate(shift.start).toLowerCase()
    return workerName.includes(query) || date.includes(query)
  })
})

// Worker options for dropdown
const workerOptions = computed(() => {
  return workerStore.workers.map(w => ({
    id: w.id,
    label: w.name
  }))
})

const openCreateModal = () => {
  modalMode.value = 'create'
  const now = new Date()
  const defaultStart = new Date(now)
  defaultStart.setHours(9, 0, 0, 0)
  const defaultEnd = new Date(now)
  defaultEnd.setHours(17, 0, 0, 0)
  
  shiftForm.value = {
    worker_id: workerStore.workers[0]?.id || 0,
    start: formatDateTimeForInput(defaultStart.toISOString()),
    end: formatDateTimeForInput(defaultEnd.toISOString())
  }
  isModalActive.value = true
}

const openEditModal = (shift: Shift) => {
  modalMode.value = 'edit'
  selectedShift.value = shift
  shiftForm.value = {
    worker_id: shift.worker_id,
    start: formatDateTimeForInput(shift.start),
    end: formatDateTimeForInput(shift.end)
  }
  isModalActive.value = true
}

const openDeleteModal = (shift: Shift) => {
  selectedShift.value = shift
  isDeleteModalActive.value = true
}

const handleSubmit = async () => {
  successMessage.value = ''
  errorMessage.value = ''
  
  try {
    // Convert datetime-local to ISO 8601 with timezone
    const payload = {
      worker_id: shiftForm.value.worker_id,
      start: new Date(shiftForm.value.start).toISOString(),
      end: new Date(shiftForm.value.end).toISOString()
    }
    
    if (modalMode.value === 'create') {
      await shiftStore.createShift(payload)
      successMessage.value = 'Shift created successfully!'
    } else if (selectedShift.value) {
      await shiftStore.updateShift(selectedShift.value.id, payload)
      successMessage.value = 'Shift updated successfully!'
    }
    isModalActive.value = false
    setTimeout(() => { successMessage.value = '' }, 3000)
  } catch (error: any) {
    errorMessage.value = error.response?.data?.detail || `Failed to ${modalMode.value} shift`
    setTimeout(() => { errorMessage.value = '' }, 5000)
  }
}

const handleDelete = async () => {
  if (!selectedShift.value) return
  
  successMessage.value = ''
  errorMessage.value = ''
  
  try {
    await shiftStore.deleteShift(selectedShift.value.id)
    successMessage.value = 'Shift deleted successfully!'
    isDeleteModalActive.value = false
    setTimeout(() => { successMessage.value = '' }, 3000)
  } catch (error: any) {
    errorMessage.value = error.response?.data?.detail || 'Failed to delete shift'
    setTimeout(() => { errorMessage.value = '' }, 5000)
  }
}
</script>

<template>
  <SectionMain>
    <SectionTitleLineWithButton :icon="mdiCalendarClock" title="Shifts" main>
      <BaseButton
        :icon="mdiPlus"
        label="Add Shift"
        color="info"
        rounded-full
        @click="openCreateModal"
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

    <CardBox class="mb-6" has-table>
      <div class="mb-4 flex items-center justify-between">
        <FormControl
          v-model="searchQuery"
          placeholder="Search shifts..."
          :icon="mdiMagnify"
          transparent
          borderless
        />
      </div>

      <div class="overflow-x-auto">
        <table class="w-full">
          <thead>
            <tr>
              <th class="text-left p-4 font-semibold">Date</th>
              <th class="text-left p-4 font-semibold">Worker</th>
              <th class="text-left p-4 font-semibold">Shift Time</th>
              <th class="text-left p-4 font-semibold">Duration</th>
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
              <td class="p-4">{{ formatDate(shift.start) }}</td>
              <td class="p-4">{{ getWorkerName(shift.worker_id) }}</td>
              <td class="p-4">{{ formatTime(shift.start) }} - {{ formatTime(shift.end) }}</td>
              <td class="p-4">{{ shift.duration_hours?.toFixed(1) || 'N/A' }}h</td>
              <td class="p-4">
                <span 
                  :class="`inline-flex items-center px-2 py-1 text-xs font-medium rounded-full
                    ${getShiftStatus(shift.start, shift.end).color === 'green' ? 'text-green-800 bg-green-100 dark:bg-green-900 dark:text-green-200' : ''}
                    ${getShiftStatus(shift.start, shift.end).color === 'blue' ? 'text-blue-800 bg-blue-100 dark:bg-blue-900 dark:text-blue-200' : ''}
                    ${getShiftStatus(shift.start, shift.end).color === 'gray' ? 'text-gray-800 bg-gray-100 dark:bg-gray-900 dark:text-gray-200' : ''}
                  `"
                >
                  {{ getShiftStatus(shift.start, shift.end).label }}
                </span>
              </td>
              <td class="p-4">
                <BaseButtons type="justify-start" no-wrap>
                  <BaseButton 
                    color="info" 
                    :icon="mdiPencil"
                    small 
                    @click="openEditModal(shift)"
                  />
                  <BaseButton 
                    color="danger" 
                    :icon="mdiTrashCan"
                    small 
                    @click="openDeleteModal(shift)"
                  />
                </BaseButtons>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </CardBox>

    <!-- Create/Edit Modal -->
    <CardBoxModal
      v-model="isModalActive"
      :title="modalMode === 'create' ? 'Add Shift' : 'Edit Shift'"
      button="success"
      :button-label="modalMode === 'create' ? 'Create' : 'Update'"
      has-cancel
      @confirm="handleSubmit"
    >
      <FormField label="Worker" help="Select the worker for this shift">
        <select
          v-model.number="shiftForm.worker_id"
          class="w-full px-3 py-2 h-12 border border-gray-700 rounded bg-white dark:bg-slate-800"
          required
        >
          <option v-for="worker in workerStore.workers" :key="worker.id" :value="worker.id">
            {{ worker.name }}
          </option>
        </select>
      </FormField>

      <FormField label="Start Date & Time" help="When does the shift start?">
        <FormControl
          v-model="shiftForm.start"
          type="datetime-local"
          required
        />
      </FormField>

      <FormField label="End Date & Time" help="When does the shift end?">
        <FormControl
          v-model="shiftForm.end"
          type="datetime-local"
          required
        />
      </FormField>

      <FormField label="End Date & Time" help="When does the shift end?">
        <FormControl
          v-model="shiftForm.end"
          type="datetime-local"
          required
        />
      </FormField>
    </CardBoxModal>

    <!-- Delete Confirmation Modal -->
    <CardBoxModal
      v-model="isDeleteModalActive"
      title="Delete Shift"
      button="danger"
      button-label="Delete"
      has-cancel
      @confirm="handleDelete"
    >
      <p>Are you sure you want to delete this shift for <strong>{{ selectedShift ? getWorkerName(selectedShift.worker_id) : '' }}</strong>?</p>
      <p v-if="selectedShift" class="mt-2 text-sm text-gray-600 dark:text-gray-400">
        {{ formatDate(selectedShift.start) }}: {{ formatTime(selectedShift.start) }} - {{ formatTime(selectedShift.end) }}
      </p>
      <p class="mt-2 text-sm text-gray-600 dark:text-gray-400">This action cannot be undone.</p>
    </CardBoxModal>
  </SectionMain>
</template>

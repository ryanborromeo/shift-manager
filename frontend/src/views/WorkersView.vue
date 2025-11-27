<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { mdiAccountGroup, mdiPlus, mdiMagnify, mdiPencil, mdiTrashCan } from '@mdi/js'
import SectionMain from '@/components/SectionMain.vue'
import CardBox from '@/components/CardBox.vue'
import CardBoxModal from '@/components/CardBoxModal.vue'
import SectionTitleLineWithButton from '@/components/SectionTitleLineWithButton.vue'
import BaseButton from '@/components/BaseButton.vue'
import BaseButtons from '@/components/BaseButtons.vue'
import FormControl from '@/components/FormControl.vue'
import FormField from '@/components/FormField.vue'
import NotificationBar from '@/components/NotificationBar.vue'
import { useWorkerStore } from '@/stores/workerStore'
import type { Worker } from '@/types'

const searchQuery = ref('')
const workerStore = useWorkerStore()
const isModalActive = ref(false)
const isDeleteModalActive = ref(false)
const modalMode = ref<'create' | 'edit'>('create')
const workerForm = ref({ name: '' })
const selectedWorker = ref<Worker | null>(null)
const successMessage = ref('')
const errorMessage = ref('')

// Fetch workers on mount
onMounted(async () => {
  try {
    await workerStore.fetchWorkers()
  } catch (error) {
    console.error('Error fetching workers:', error)
  }
})

// Filter workers based on search query
const filteredWorkers = computed(() => {
  if (!searchQuery.value) {
    return workerStore.workers
  }
  const query = searchQuery.value.toLowerCase()
  return workerStore.workers.filter(worker =>
    worker.name.toLowerCase().includes(query)
  )
})

const openCreateModal = () => {
  modalMode.value = 'create'
  workerForm.value = { name: '' }
  isModalActive.value = true
}

const openEditModal = (worker: Worker) => {
  modalMode.value = 'edit'
  selectedWorker.value = worker
  workerForm.value = { name: worker.name }
  isModalActive.value = true
}

const openDeleteModal = (worker: Worker) => {
  selectedWorker.value = worker
  isDeleteModalActive.value = true
}

const handleSubmit = async () => {
  successMessage.value = ''
  errorMessage.value = ''
  
  try {
    if (modalMode.value === 'create') {
      await workerStore.createWorker(workerForm.value)
      successMessage.value = 'Worker created successfully!'
    } else if (selectedWorker.value) {
      await workerStore.updateWorker(selectedWorker.value.id, workerForm.value)
      successMessage.value = 'Worker updated successfully!'
    }
    isModalActive.value = false
    setTimeout(() => { successMessage.value = '' }, 3000)
  } catch (error: any) {
    errorMessage.value = error.response?.data?.detail || `Failed to ${modalMode.value} worker`
    setTimeout(() => { errorMessage.value = '' }, 5000)
  }
}

const handleDelete = async () => {
  if (!selectedWorker.value) return
  
  successMessage.value = ''
  errorMessage.value = ''
  
  try {
    await workerStore.deleteWorker(selectedWorker.value.id)
    successMessage.value = 'Worker deleted successfully!'
    isDeleteModalActive.value = false
    setTimeout(() => { successMessage.value = '' }, 3000)
  } catch (error: any) {
    errorMessage.value = error.response?.data?.detail || 'Failed to delete worker'
    setTimeout(() => { errorMessage.value = '' }, 5000)
  }
}
</script>

<template>
  <SectionMain>
    <SectionTitleLineWithButton :icon="mdiAccountGroup" title="Workers" main>
      <BaseButton
        :icon="mdiPlus"
        label="Add Worker"
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
              <th class="text-left p-4 font-semibold">ID</th>
              <th class="text-left p-4 font-semibold">Name</th>
              <th class="text-left p-4 font-semibold">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="filteredWorkers.length === 0">
              <td colspan="3" class="p-8 text-center text-gray-500">
                No workers found
              </td>
            </tr>
            <tr 
              v-for="worker in filteredWorkers" 
              :key="worker.id"
              class="border-t dark:border-slate-700"
            >
              <td class="p-4">{{ worker.id }}</td>
              <td class="p-4">{{ worker.name }}</td>
              <td class="p-4">
                <BaseButtons type="justify-start" no-wrap>
                  <BaseButton 
                    color="info" 
                    :icon="mdiPencil"
                    small 
                    @click="openEditModal(worker)"
                  />
                  <BaseButton 
                    color="danger" 
                    :icon="mdiTrashCan"
                    small 
                    @click="openDeleteModal(worker)"
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
      :title="modalMode === 'create' ? 'Add Worker' : 'Edit Worker'"
      button="success"
      :button-label="modalMode === 'create' ? 'Create' : 'Update'"
      has-cancel
      @confirm="handleSubmit"
    >
      <FormField label="Worker Name" help="Enter the full name of the worker">
        <FormControl
          v-model="workerForm.name"
          type="text"
          placeholder="e.g., John Doe"
          required
        />
      </FormField>
    </CardBoxModal>

    <!-- Delete Confirmation Modal -->
    <CardBoxModal
      v-model="isDeleteModalActive"
      title="Delete Worker"
      button="danger"
      button-label="Delete"
      has-cancel
      @confirm="handleDelete"
    >
      <p>Are you sure you want to delete <strong>{{ selectedWorker?.name }}</strong>?</p>
      <p class="mt-2 text-sm text-gray-600 dark:text-gray-400">This action cannot be undone.</p>
    </CardBoxModal>
  </SectionMain>
</template>

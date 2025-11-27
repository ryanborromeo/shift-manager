<script setup lang="ts">
import { 
  mdiAccountGroup, 
  mdiCashMultiple, 
  mdiTrendingUp,
  mdiChartTimelineVariant,
  mdiReload,
  mdiGithub
} from '@mdi/js'
import { computed, onMounted } from 'vue'
import SectionMain from '@/components/SectionMain.vue'
import CardBoxWidget from '@/components/CardBoxWidget.vue'
import CardBox from '@/components/CardBox.vue'
import BaseLevel from '@/components/BaseLevel.vue'
import SectionTitleLineWithButton from '@/components/SectionTitleLineWithButton.vue'
import CardBoxTransaction from '@/components/CardBoxTransaction.vue'
import CardBoxClient from '@/components/CardBoxClient.vue'
import BaseButton from '@/components/BaseButton.vue'
import { useMainStore } from '@/stores/main.js'
import { useWorkerStore } from '@/stores/workerStore'
import { useShiftStore } from '@/stores/shiftStore'

const mainStore = useMainStore()
const workerStore = useWorkerStore()
const shiftStore = useShiftStore()

// Fetch data on component mount
onMounted(async () => {
  try {
    await Promise.all([
      workerStore.fetchWorkers(),
      shiftStore.fetchShifts()
    ])
  } catch (error) {
    console.error('Error fetching dashboard data:', error)
  }
})

// Helper function to format relative dates
const getRelativeDate = (dateString: string) => {
  const date = new Date(dateString)
  const now = new Date()
  const diffTime = Math.abs(now.getTime() - date.getTime())
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
  
  if (diffDays === 0) return 'Today'
  if (diffDays === 1) return 'Yesterday'
  if (diffDays < 7) return `${diffDays} days ago`
  if (diffDays < 30) return `${Math.floor(diffDays / 7)} weeks ago`
  return date.toLocaleDateString()
}

// Transform shifts to transaction format
const transactionBarItems = computed(() => {
  return shiftStore.shifts.slice(0, 4).map((shift, index) => {
    const worker = workerStore.workers.find(w => w.id === shift.worker_id)
    const startTime = new Date(shift.start)
    const endTime = new Date(shift.end)
    const hours = (endTime.getTime() - startTime.getTime()) / (1000 * 60 * 60)
    const amount = hours * 25 // Assuming $25/hour rate
    
    return {
      id: shift.id,
      amount: parseFloat(amount.toFixed(2)),
      date: getRelativeDate(shift.start),
      business: `${startTime.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })} - ${endTime.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}`,
      type: new Date(shift.start) > new Date() ? 'Scheduled' : 'Completed',
      name: worker ? worker.name : 'Unknown',
      account: 'N/A'
    }
  })
})

// Transform workers to client format
const clientBarItems = computed(() => {
  return workerStore.workers.slice(0, 4).map(worker => {
    const workerShifts = shiftStore.shifts.filter(s => s.worker_id === worker.id)
    const totalHours = workerShifts.reduce((acc, shift) => {
      const start = new Date(shift.start_time)
      const end = new Date(shift.end_time)
      return acc + (end.getTime() - start.getTime()) / (1000 * 60 * 60)
    }, 0)
    
    return {
      id: worker.id,
      name: worker.name,
      login: worker.email,
      date: new Date(worker.created_at).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' }),
      progress: Math.min(Math.round((totalHours / 160) * 100), 100) // 160 hours = full month
    }
  })
})

// Calculate total workers count
const totalWorkers = computed(() => workerStore.workers.length)

// Calculate total hours or shifts
const totalShifts = computed(() => shiftStore.shifts.length)

// Calculate performance metric
const performanceMetric = computed(() => {
  const completedShifts = shiftStore.shifts.filter(s => new Date(s.end_time) < new Date()).length
  const totalShiftsCount = shiftStore.shifts.length
  return totalShiftsCount > 0 ? Math.round((completedShifts / totalShiftsCount) * 100) : 0
})
</script>

<template>
  <SectionMain>
    <SectionTitleLineWithButton :icon="mdiChartTimelineVariant" title="Overview" main>
      <BaseButton
        href="https://github.com/justboil/admin-one-vue-tailwind"
        target="_blank"
        :icon="mdiGithub"
        label="Star on GitHub"
        color="contrast"
        rounded-full
        small
      />
    </SectionTitleLineWithButton>

    <div class="grid grid-cols-1 gap-6 mb-6 lg:grid-cols-3">
      <CardBoxWidget
        color="text-emerald-500"
        :icon="mdiAccountGroup"
        :number="totalWorkers"
        label="Workers"
      />
      <CardBoxWidget
        color="text-blue-500"
        :icon="mdiChartTimelineVariant"
        :number="totalShifts"
        label="Shifts"
      />
      <CardBoxWidget
        color="text-red-500"
        :icon="mdiTrendingUp"
        :number="performanceMetric"
        suffix="%"
        label="Completion Rate"
      />
    </div>

    <div class="grid grid-cols-1 gap-6 mb-6 lg:grid-cols-2">
      <div class="flex flex-col justify-between">
        <CardBoxTransaction
          v-for="(transaction, index) in transactionBarItems"
          :key="index"
          :amount="transaction.amount"
          :date="transaction.date"
          :business="transaction.business"
          :type="transaction.type"
          :name="transaction.name"
          :account="transaction.account"
        />
      </div>
      <div class="flex flex-col justify-between">
        <CardBoxClient
          v-for="client in clientBarItems"
          :key="client.id"
          :name="client.name"
          :login="client.login"
          :date="client.date"
          :progress="client.progress"
        />
      </div>
    </div>
  </SectionMain>
</template>

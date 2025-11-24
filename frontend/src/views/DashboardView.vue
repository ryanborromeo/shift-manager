<script setup lang="ts">
import { 
  mdiAccountGroup, 
  mdiCashMultiple, 
  mdiTrendingUp,
  mdiChartTimelineVariant,
  mdiReload,
  mdiGithub
} from '@mdi/js'
import { computed, ref } from 'vue'
import SectionMain from '@/components/SectionMain.vue'
import CardBoxWidget from '@/components/CardBoxWidget.vue'
import CardBox from '@/components/CardBox.vue'
import BaseLevel from '@/components/BaseLevel.vue'
import SectionTitleLineWithButton from '@/components/SectionTitleLineWithButton.vue'
import CardBoxTransaction from '@/components/CardBoxTransaction.vue'
import CardBoxClient from '@/components/CardBoxClient.vue'
import BaseButton from '@/components/BaseButton.vue'
import { useMainStore } from '@/stores/main.js'

const mainStore = useMainStore()

// Sample transaction data
const transactionBarItems = computed(() => [
  {
    id: 1,
    amount: 375.53,
    date: '3 days ago',
    business: 'Morning Shift',
    type: 'Scheduled',
    name: 'John Doe',
    account: 'Engineering'
  },
  {
    id: 2,
    amount: 470.26,
    date: '3 days ago',
    business: 'Evening Shift',
    type: 'Scheduled',
    name: 'Jane Smith',
    account: 'Marketing'
  },
  {
    id: 3,
    amount: 971.34,
    date: '5 days ago',
    business: 'Night Shift',
    type: 'Completed',
    name: 'Bob Wilson',
    account: 'Operations'
  },
  {
    id: 4,
    amount: 374.63,
    date: '7 days ago',
    business: 'Weekend Shift',
    type: 'Completed',
    name: 'Alice Brown',
    account: 'Customer Service'
  }
])

// Sample client data
const clientBarItems = ref([
  {
    id: 1,
    name: 'John Doe',
    login: 'john.doe',
    date: 'Mar 3, 2025',
    progress: 70
  },
  {
    id: 2,
    name: 'Jane Smith',
    login: 'jane.smith',
    date: 'Dec 1, 2025',
    progress: 68
  },
  {
    id: 3,
    name: 'Bob Wilson',
    login: 'bob.wilson',
    date: 'May 18, 2025',
    progress: 49
  },
  {
    id: 4,
    name: 'Alice Brown',
    login: 'alice.brown',
    date: 'May 4, 2025',
    progress: 38
  }
])
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
        trend="12%"
        trend-type="up"
        color="text-emerald-500"
        :icon="mdiAccountGroup"
        :number="512"
        label="Workers"
      />
      <CardBoxWidget
        trend="12%"
        trend-type="down"
        color="text-blue-500"
        :icon="mdiCashMultiple"
        :number="7770"
        prefix="$"
        label="Sales"
      />
      <CardBoxWidget
        trend="Overflow"
        trend-type="alert"
        color="text-red-500"
        :icon="mdiChartTimelineVariant"
        :number="256"
        suffix="%"
        label="Performance"
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

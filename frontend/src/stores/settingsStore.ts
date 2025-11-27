import { defineStore } from 'pinia';
import { ref } from 'vue';
import { api } from '@/services/api';
import type { TimezoneSettings } from '@/types';

export const useSettingsStore = defineStore('settings', () => {
  const timezone = ref<string>('UTC');
  const loading = ref(false);
  const error = ref<string | null>(null);

  // Fetch timezone settings
  const fetchTimezone = async () => {
    loading.value = true;
    error.value = null;
    try {
      const response = await api.getTimezone();
      timezone.value = response.data.timezone;
      return response.data;
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to fetch timezone settings';
      throw err;
    } finally {
      loading.value = false;
    }
  };

  // Update timezone settings
  const updateTimezone = async (newTimezone: string) => {
    loading.value = true;
    error.value = null;
    try {
      const response = await api.updateTimezone(newTimezone);
      timezone.value = response.data.timezone;
      return response.data;
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to update timezone settings';
      throw err;
    } finally {
      loading.value = false;
    }
  };

  return {
    timezone,
    loading,
    error,
    fetchTimezone,
    updateTimezone,
  };
});

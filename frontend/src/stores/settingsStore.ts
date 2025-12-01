import { defineStore } from 'pinia';
import { ref } from 'vue';
import { api } from '@/services/api';
import type { TimeZoneInfo } from '@/types';

const DEFAULT_TIMEZONE = 'Etc/UTC';

export const useSettingsStore = defineStore('settings', () => {
  const timezone = ref<string>(DEFAULT_TIMEZONE);
  const timezoneInfo = ref<TimeZoneInfo | null>(null);
  const availableTimezones = ref<string[]>([]);
  const loading = ref(false);
  const error = ref<string | null>(null);

  const withRequest = async <T>(fn: () => Promise<T>) => {
    loading.value = true;
    error.value = null;
    try {
      return await fn();
    } catch (err: any) {
      error.value = err.response?.data?.detail || err.message || 'Unexpected error communicating with backend';
      throw err;
    } finally {
      loading.value = false;
    }
  };

  const fetchAvailableTimezones = () =>
    withRequest(async () => {
      const response = await api.getAvailableTimezones();
      availableTimezones.value = response.data;
      if (!availableTimezones.value.includes(timezone.value)) {
        timezone.value = availableTimezones.value[0] ?? DEFAULT_TIMEZONE;
      }
      return availableTimezones.value;
    });

  const fetchTimezone = () =>
    withRequest(async () => {
      const response = await api.getTimezone();
      timezone.value = response.data.timezone;
      timezoneInfo.value = response.data;
      return response.data;
    });

  const updateTimezone = async (newTimezone: string) =>
    withRequest(async () => {
      const response = await api.updateTimezone(newTimezone);
      timezone.value = response.data.timezone;
      timezoneInfo.value = response.data;
      return { timezone: timezone.value, info: response.data };
    });

  return {
    timezone,
    timezoneInfo,
    availableTimezones,
    loading,
    error,
    fetchAvailableTimezones,
    fetchTimezone,
    updateTimezone,
  };
});

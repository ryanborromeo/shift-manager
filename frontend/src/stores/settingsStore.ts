import { defineStore } from 'pinia';
import { ref } from 'vue';
import { timeApi } from '@/services/timeApi';
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
      error.value = err.response?.data?.detail || err.message || 'Unexpected error communicating with Time API';
      throw err;
    } finally {
      loading.value = false;
    }
  };

  const fetchAvailableTimezones = () =>
    withRequest(async () => {
      const response = await timeApi.getAvailableTimezones();
      availableTimezones.value = response.data;
      if (!availableTimezones.value.includes(timezone.value)) {
        timezone.value = availableTimezones.value[0] ?? DEFAULT_TIMEZONE;
      }
      return availableTimezones.value;
    });

  const fetchTimezone = (targetTimezone?: string) =>
    withRequest(async () => {
      const tz = targetTimezone || timezone.value || DEFAULT_TIMEZONE;
      if (!tz) {
        throw new Error('Timezone is required');
      }
      const response = await timeApi.getTimezoneInfo(tz);
      timezone.value = tz;
      timezoneInfo.value = response.data;
      return response.data;
    });

  const updateTimezone = async (newTimezone: string) => {
    const data = await fetchTimezone(newTimezone);
    return { timezone: timezone.value, info: data };
  };

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

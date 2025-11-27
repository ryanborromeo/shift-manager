import { defineStore } from 'pinia';
import { ref } from 'vue';
import { api } from '@/services/api';
import type { Shift, ShiftCreate, ShiftUpdate } from '@/types';

export const useShiftStore = defineStore('shift', () => {
  const shifts = ref<Shift[]>([]);
  const currentShift = ref<Shift | null>(null);
  const loading = ref(false);
  const error = ref<string | null>(null);

  // Fetch all shifts
  const fetchShifts = async () => {
    loading.value = true;
    error.value = null;
    try {
      const response = await api.getShifts();
      shifts.value = response.data;
      return response.data;
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to fetch shifts';
      throw err;
    } finally {
      loading.value = false;
    }
  };

  // Fetch a single shift by ID
  const fetchShift = async (id: number) => {
    loading.value = true;
    error.value = null;
    try {
      const response = await api.getShift(id);
      currentShift.value = response.data;
      return response.data;
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to fetch shift';
      throw err;
    } finally {
      loading.value = false;
    }
  };

  // Create a new shift
  const createShift = async (shiftData: ShiftCreate) => {
    loading.value = true;
    error.value = null;
    try {
      const response = await api.createShift(shiftData);
      shifts.value.push(response.data);
      return response.data;
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to create shift';
      throw err;
    } finally {
      loading.value = false;
    }
  };

  // Update an existing shift
  const updateShift = async (id: number, shiftData: ShiftUpdate) => {
    loading.value = true;
    error.value = null;
    try {
      const response = await api.updateShift(id, shiftData);
      const index = shifts.value.findIndex(s => s.id === id);
      if (index !== -1) {
        shifts.value[index] = response.data;
      }
      if (currentShift.value?.id === id) {
        currentShift.value = response.data;
      }
      return response.data;
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to update shift';
      throw err;
    } finally {
      loading.value = false;
    }
  };

  // Delete a shift
  const deleteShift = async (id: number) => {
    loading.value = true;
    error.value = null;
    try {
      await api.deleteShift(id);
      shifts.value = shifts.value.filter(s => s.id !== id);
      if (currentShift.value?.id === id) {
        currentShift.value = null;
      }
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to delete shift';
      throw err;
    } finally {
      loading.value = false;
    }
  };

  // Reset the current shift
  const resetCurrentShift = () => {
    currentShift.value = null;
  };

  // Get shifts for a specific worker
  const getShiftsByWorker = (workerId: number) => {
    return shifts.value.filter(shift => shift.worker_id === workerId);
  };

  return {
    shifts,
    currentShift,
    loading,
    error,
    fetchShifts,
    fetchShift,
    createShift,
    updateShift,
    deleteShift,
    resetCurrentShift,
    getShiftsByWorker,
  };
});

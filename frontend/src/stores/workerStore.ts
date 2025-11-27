import { defineStore } from 'pinia';
import { ref } from 'vue';
import { api } from '@/services/api';
import type { Worker, WorkerCreate, WorkerUpdate } from '@/types';

export const useWorkerStore = defineStore('worker', () => {
  const workers = ref<Worker[]>([]);
  const currentWorker = ref<Worker | null>(null);
  const loading = ref(false);
  const error = ref<string | null>(null);

  // Fetch all workers
  const fetchWorkers = async () => {
    loading.value = true;
    error.value = null;
    try {
      const response = await api.getWorkers();
      workers.value = response.data;
      return response.data;
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to fetch workers';
      throw err;
    } finally {
      loading.value = false;
    }
  };

  // Fetch a single worker by ID
  const fetchWorker = async (id: number) => {
    loading.value = true;
    error.value = null;
    try {
      const response = await api.getWorker(id);
      currentWorker.value = response.data;
      return response.data;
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to fetch worker';
      throw err;
    } finally {
      loading.value = false;
    }
  };

  // Create a new worker
  const createWorker = async (workerData: WorkerCreate) => {
    loading.value = true;
    error.value = null;
    try {
      const response = await api.createWorker(workerData);
      workers.value.push(response.data);
      return response.data;
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to create worker';
      throw err;
    } finally {
      loading.value = false;
    }
  };

  // Update an existing worker
  const updateWorker = async (id: number, workerData: WorkerUpdate) => {
    loading.value = true;
    error.value = null;
    try {
      const response = await api.updateWorker(id, workerData);
      const index = workers.value.findIndex(w => w.id === id);
      if (index !== -1) {
        workers.value[index] = response.data;
      }
      if (currentWorker.value?.id === id) {
        currentWorker.value = response.data;
      }
      return response.data;
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to update worker';
      throw err;
    } finally {
      loading.value = false;
    }
  };

  // Delete a worker
  const deleteWorker = async (id: number) => {
    loading.value = true;
    error.value = null;
    try {
      await api.deleteWorker(id);
      workers.value = workers.value.filter(w => w.id !== id);
      if (currentWorker.value?.id === id) {
        currentWorker.value = null;
      }
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to delete worker';
      throw err;
    } finally {
      loading.value = false;
    }
  };

  // Reset the current worker
  const resetCurrentWorker = () => {
    currentWorker.value = null;
  };

  return {
    workers,
    currentWorker,
    loading,
    error,
    fetchWorkers,
    fetchWorker,
    createWorker,
    updateWorker,
    deleteWorker,
    resetCurrentWorker,
  };
});

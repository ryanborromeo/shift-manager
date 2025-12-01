// Worker related types
export interface Worker {
  id: number;
  name: string;
}

export interface WorkerCreate {
  name: string;
}

export interface WorkerUpdate {
  name: string;
}

// Shift related types
export interface Shift {
  id: number;
  worker_id: number;
  start: string;
  end: string;
  duration_hours?: number;
}

export interface ShiftCreate {
  worker_id: number;
  start: string;
  end: string;
}

export interface ShiftUpdate {
  worker_id: number;
  start: string;
  end: string;
}

// Timezone related types (backend-provided via zoneinfo)
export interface TimezoneOffset {
  seconds: number;
  milliseconds: number;
}

export interface TimeZoneInfo {
  timezone: string;
  currentLocalTime: string;
  currentUtcOffset: TimezoneOffset;
  standardUtcOffset: TimezoneOffset;
  hasDayLightSaving: boolean;
  isDayLightSavingActive: boolean;
}

// API response types
export interface ApiResponse<T> {
  data: T;
  message?: string;
  status: number;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  size: number;
  pages: number;
}

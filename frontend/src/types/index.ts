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

// Time API related types
export interface Offset {
  seconds?: number;
  milliseconds?: number;
  ticks?: number;
  nanoseconds?: number;
}

export interface Duration {
  days?: number;
  nanosecondOfDay?: number;
  hours?: number;
  minutes?: number;
  seconds?: number;
  milliseconds?: number;
  subsecondTicks?: number;
  subsecondNanoseconds?: number;
  bclCompatibleTicks?: number;
  totalDays?: number;
  totalHours?: number;
  totalMinutes?: number;
  totalSeconds?: number;
  totalMilliseconds?: number;
  totalTicks?: number;
  totalNanoseconds?: number;
}

export interface DstInterval {
  dstName?: string | null;
  dstOffsetToUtc?: Offset;
  dstOffsetToStandardTime?: Offset;
  dstStart?: string | null;
  dstEnd?: string | null;
  dstDuration?: Duration;
}

export interface TimeZoneInfo {
  timeZone?: string | null;
  currentLocalTime?: string;
  currentUtcOffset?: Offset;
  standardUtcOffset?: Offset;
  hasDayLightSaving?: boolean;
  isDayLightSavingActive?: boolean;
  dstInterval?: DstInterval | null;
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

import { ref } from 'vue';
import type { AxiosError } from 'axios';
import type { ApiErrorResponse, HttpValidationError } from '@/types/errors';
import { isValidationError } from '@/types/errors';

export interface ApiError {
  message: string;
  status?: number;
  details?: any;
  validationErrors?: Array<{ field: string; message: string }>;
}

export function useApiError() {
  const error = ref<ApiError | null>(null);
  const hasError = ref(false);

  const handleError = (err: unknown): ApiError => {
    const axiosError = err as AxiosError<ApiErrorResponse | HttpValidationError>;
    const responseData = axiosError.response?.data;
    
    const apiError: ApiError = {
      message: 'An unexpected error occurred',
      status: axiosError.response?.status,
      details: responseData || {}
    };

    // Handle different types of error responses
    if (responseData) {
      // Handle validation errors
      if (isValidationError(responseData)) {
        apiError.message = 'Validation error';
        apiError.validationErrors = responseData.detail.map(err => ({
          field: err.loc.join('.'),
          message: err.msg
        }));
      } 
      // Handle standard error responses with detail or message
      else if ('detail' in responseData && responseData.detail) {
        apiError.message = responseData.detail;
      } else if ('message' in responseData && responseData.message) {
        apiError.message = responseData.message;
      }
    } else if (axiosError.message) {
      apiError.message = axiosError.message;
    }

    error.value = apiError;
    hasError.value = true;

    // Log the error for debugging
    console.error('API Error:', {
      message: apiError.message,
      status: apiError.status,
      details: apiError.details,
      validationErrors: apiError.validationErrors
    });

    return apiError;
  };

  const resetError = (): void => {
    error.value = null;
    hasError.value = false;
  };

  return {
    error,
    hasError,
    handleError,
    resetError
  };
}

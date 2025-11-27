export interface ApiErrorResponse {
  detail?: string;
  message?: string;
  status_code?: number;
  [key: string]: any;
}

export interface ValidationError {
  loc: (string | number)[];
  msg: string;
  type: string;
}

export interface HttpValidationError {
  detail: ValidationError[];
}

export function isValidationError(error: any): error is HttpValidationError {
  return error && Array.isArray(error.detail) && error.detail.every(
    (e: any) => e.loc && e.msg && e.type
  );
}

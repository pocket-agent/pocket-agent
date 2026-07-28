import type { GoogleUser } from "@/lib/google-auth";

export interface Env {
  GOOGLE_CLIENT_ID: string;
  ALLOWED_ORIGINS?: string;
  ENVIRONMENT?: string;
  /** Reserved for cloud-relay chat mode (not enabled yet) */
  GEMINI_API_KEY?: string;
  GEMINI_MODEL?: string;
  /** Proxy target when routing to Pocket Node */
  POCKET_NODE_URL?: string;
}

export interface Variables {
  userId?: string;
  googleUser?: GoogleUser;
}

export interface SuccessResponse<T> {
  success: true;
  data: T;
}

export interface ErrorResponse {
  success: false;
  error: {
    message: string;
    code?: string;
    details?: Record<string, unknown>;
  };
}

export type ApiResponse<T> = SuccessResponse<T> | ErrorResponse;

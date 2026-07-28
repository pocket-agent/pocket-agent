import { Env } from "@/types";
import { extractJWT } from "@/utils/jwt";

const DEFAULT_POCKET_NODE_URL = "http://127.0.0.1:8787";

export function pocketNodeBaseUrl(env: Env): string {
  const url = env.POCKET_NODE_URL?.trim() || DEFAULT_POCKET_NODE_URL;
  return url.replace(/\/$/, "");
}

export async function proxyToPocketNode(
  env: Env,
  path: string,
  init: RequestInit,
  authToken: string
): Promise<Response> {
  const url = `${pocketNodeBaseUrl(env)}${path.startsWith("/") ? path : `/${path}`}`;
  const headers = new Headers(init.headers);
  headers.set("Authorization", `Bearer ${authToken}`);

  return fetch(url, {
    ...init,
    headers,
  });
}

export function bearerFromRequest(authHeader: string | null): string | null {
  return extractJWT(authHeader);
}

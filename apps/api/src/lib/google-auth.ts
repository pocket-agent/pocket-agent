import { createRemoteJWKSet, jwtVerify } from "jose";
import { Env } from "@/types";

const GOOGLE_JWKS = createRemoteJWKSet(
  new URL("https://www.googleapis.com/oauth2/v3/certs")
);

const GOOGLE_ISSUERS = ["https://accounts.google.com", "accounts.google.com"];

export interface GoogleUser {
  sub: string;
  email?: string;
  email_verified?: boolean;
  name?: string;
  picture?: string;
  given_name?: string;
  family_name?: string;
}

/**
 * Verify a Google OAuth ID token (JWT) from the Authorization header.
 * Frontend obtains this via Google Identity Services / OAuth using GOOGLE_CLIENT_ID.
 */
export async function verifyGoogleIdToken(
  token: string,
  env: Env
): Promise<GoogleUser | null> {
  const clientId = env.GOOGLE_CLIENT_ID?.trim();
  if (!clientId) {
    console.error("GOOGLE_CLIENT_ID is not configured");
    return null;
  }

  try {
    const { payload } = await jwtVerify(token, GOOGLE_JWKS, {
      issuer: GOOGLE_ISSUERS,
      audience: clientId,
    });

    if (!payload.sub) {
      return null;
    }

    return {
      sub: payload.sub,
      email: payload.email as string | undefined,
      email_verified: payload.email_verified as boolean | undefined,
      name: payload.name as string | undefined,
      picture: payload.picture as string | undefined,
      given_name: payload.given_name as string | undefined,
      family_name: payload.family_name as string | undefined,
    };
  } catch (error) {
    console.error("Google ID token verification failed:", error);
    return null;
  }
}

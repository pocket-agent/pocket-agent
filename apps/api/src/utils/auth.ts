import { Context } from "hono";
import { verifyGoogleIdToken, GoogleUser } from "@/lib/google-auth";
import { extractJWT } from "./jwt";
import { Env, Variables } from "@/types";

export const getAuthenticatedUser = async (
  c: Context<{ Bindings: Env; Variables: Variables }>
): Promise<GoogleUser | null> => {
  const token = extractJWT(c.req.header("Authorization") || null);

  if (!token) {
    return null;
  }

  return verifyGoogleIdToken(token, c.env);
};

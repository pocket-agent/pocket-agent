import { Hono } from "hono";
import { successResponse } from "@/utils/response";
import { Env, Variables } from "@/types";

/**
 * GET /auth — confirms Bearer Google ID token is valid (same middleware as /me).
 */
export const authRouter = new Hono<{ Bindings: Env; Variables: Variables }>();

authRouter.get("/", (c) => {
  const user = c.get("googleUser");

  return c.json(
    successResponse({
      authenticated: true,
      id: user?.sub,
      email: user?.email,
      email_verified: user?.email_verified,
    })
  );
});

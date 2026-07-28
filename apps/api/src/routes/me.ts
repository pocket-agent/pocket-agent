import { Hono } from "hono";
import { successResponse } from "@/utils/response";
import { Env, Variables } from "@/types";

export const meRouter = new Hono<{ Bindings: Env; Variables: Variables }>();

meRouter.get("/", (c) => {
  const user = c.get("googleUser");

  return c.json(
    successResponse({
      id: user?.sub,
      email: user?.email,
      user_metadata: {
        name: user?.name,
        picture: user?.picture,
        given_name: user?.given_name,
        family_name: user?.family_name,
        email_verified: user?.email_verified,
      },
      app_metadata: {},
    })
  );
});

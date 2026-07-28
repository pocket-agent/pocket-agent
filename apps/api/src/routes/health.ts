import { Hono } from "hono";
import { Env, Variables } from "@/types";

export const healthRouter = new Hono<{ Bindings: Env; Variables: Variables }>();

healthRouter.get("/", (c) => {
  return c.json({
    success: true,
    data: {
      status: "ok",
      timestamp: new Date().toISOString(),
      service: "pocket-agent-api",
    },
  });
});

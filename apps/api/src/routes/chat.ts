import { zValidator } from "@hono/zod-validator";
import { Hono } from "hono";
import { z } from "zod";
import { bearerFromRequest, proxyToPocketNode } from "@/lib/pocket-node";
import { errorResponse } from "@/utils/response";
import { Env, Variables } from "@/types";

const historyItemSchema = z.object({
  role: z.enum(["user", "assistant"]),
  content: z.string().min(1).max(10000),
});

const messageBodySchema = z.object({
  message: z.string().min(1, "message is required").max(10000),
  history: z.array(historyItemSchema).max(100).optional(),
});

export const chatRouter = new Hono<{ Bindings: Env; Variables: Variables }>();

/** POST /chat — proxy to Pocket Node */
chatRouter.post("/", zValidator("json", messageBodySchema), async (c) => {
  const token = bearerFromRequest(c.req.header("Authorization") || null);
  if (!token) {
    return c.json(errorResponse("Unauthorized", "UNAUTHORIZED"), { status: 401 });
  }

  const body = c.req.valid("json");

  try {
    const upstream = await proxyToPocketNode(
      c.env,
      "/chat",
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      },
      token
    );

    const text = await upstream.text();
    return new Response(text, {
      status: upstream.status,
      headers: {
        "Content-Type": upstream.headers.get("Content-Type") ?? "application/json",
      },
    });
  } catch (error) {
    console.error("Pocket Node proxy failed:", error);
    return c.json(
      errorResponse("Pocket Node is not reachable", "INTERNAL_SERVER_ERROR"),
      { status: 502 }
    );
  }
});

/**
 * Extract Bearer token from Authorization header.
 */
export const extractJWT = (authHeader: string | null): string | null => {
  if (!authHeader) return null;

  const parts = authHeader.split(" ");
  if (parts.length !== 2 || parts[0] !== "Bearer") {
    return null;
  }

  const token = parts[1]?.trim();
  return token || null;
};

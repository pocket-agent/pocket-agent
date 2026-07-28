# Cloudflare Workers Deployment Guide

This guide covers deploying the Cloudflare Hono Supabase backend to Cloudflare Workers.

## Prerequisites

- Cloudflare account
- Domain registered (or use workers.dev subdomain)
- Wrangler CLI installed: `npm install -g @cloudflare/wrangler`
- Cloudflare account ID and API token

## Initial Setup

### 1. Get Cloudflare Account Details

```bash
# Log in to Cloudflare
wrangler login

# Get your account ID
wrangler whoami
```

Update `wrangler.toml`:

```toml
account_id = "your-account-id"
```

### 2. Configure wrangler.toml

```toml
name = "cf-hono-supabase-gemini-api-template"
type = "service"
main = "src/index.ts"
compatibility_date = "2024-01-15"

# Production environment
[env.production]
routes = [
  { pattern = "api.yourdomain.com/*", custom_domain = true }
]
vars = { ENVIRONMENT = "production" }

# Staging environment
[env.staging]
routes = [
  { pattern = "staging-api.yourdomain.com/*", custom_domain = true }
]
vars = { ENVIRONMENT = "staging" }

# Build settings
[build]
command = "npm run build"
cwd = "./"
watch_paths = ["src/**/*.ts"]
```

### 3. Set Environment Secrets

Environment variables with sensitive data should be set as secrets:

```bash
# Production secrets
wrangler secret put SUPABASE_URL --env production
wrangler secret put SUPABASE_ANON_KEY --env production
wrangler secret put SUPABASE_SERVICE_ROLE_KEY --env production
wrangler secret put ALLOWED_ORIGINS --env production

# Staging secrets
wrangler secret put SUPABASE_URL --env staging
wrangler secret put SUPABASE_ANON_KEY --env staging
wrangler secret put SUPABASE_SERVICE_ROLE_KEY --env staging
wrangler secret put ALLOWED_ORIGINS --env staging
```

When prompted, enter the values:

```
SUPABASE_URL: https://your-project.supabase.co
SUPABASE_ANON_KEY: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
SUPABASE_SERVICE_ROLE_KEY: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
ALLOWED_ORIGINS: https://yourdomain.com,https://staging.yourdomain.com
```

### 4. Configure Custom Domain (Optional)

If using a custom domain:

1. Update your domain's DNS settings in Cloudflare
2. Add CNAME record pointing to your worker
3. Configure in `wrangler.toml` as shown above

For workers.dev subdomain (free):

```bash
wrangler publish
```

Your API will be available at: `https://cf-hono-supabase-gemini-api-template.your-username.workers.dev`

## Deployment

### Deploy to Staging

```bash
npm run deploy -- --env staging
```

Verify deployment:

```bash
curl https://staging-api.yourdomain.com/health
```

### Deploy to Production

```bash
npm run deploy -- --env production
```

Verify deployment:

```bash
curl https://api.yourdomain.com/health
```

## Monitoring

### View Logs

```bash
# Real-time logs
wrangler tail --env production

# Tail with detailed output
wrangler tail --env production --format json
```

### Monitor Errors

Errors are logged to Cloudflare's dashboard:

1. Go to Workers → Your Worker → Logs
2. Check for any errors or exceptions
3. View request/response details

## Performance Optimization

### 1. Enable Caching

For read-only endpoints, add cache headers:

```typescript
// In route handler
c.res.headers.set('Cache-Control', 'public, max-age=300');
```

### 2. Database Connection Pooling

Supabase connections are automatically pooled. To optimize:

- Reuse Supabase client instances
- Keep queries efficient
- Use indexes on frequently queried columns

### 3. Bundle Size

Check your bundle size:

```bash
wrangler publish --dry-run
```

If bundle is too large (>1MB):

1. Remove unused dependencies
2. Use tree-shaking compatible imports
3. Consider code splitting

## Limits and Quotas

Cloudflare Workers has these limits:

- **CPU Time**: 50ms per request (free) / 400ms (paid)
- **Memory**: 128MB
- **Request Size**: 100MB
- **Response Size**: 100MB
- **Requests**: Unlimited (free tier)

To stay within limits:

1. Keep request processing under 50ms
2. Optimize database queries
3. Use pagination for large datasets
4. Cache frequently accessed data

## Troubleshooting

### Authentication Failing

Check that secrets are set correctly:

```bash
# List secrets (shows names, not values)
wrangler secret list --env production
```

### CORS Errors

Verify ALLOWED_ORIGINS is set:

```bash
wrangler secret get ALLOWED_ORIGINS --env production
```

Should include your frontend URL.

### Database Connection Issues

1. Verify Supabase URL and keys are correct
2. Check Supabase project is running
3. Verify IP whitelist (if enabled)

### Worker Timeouts

If requests timeout:

1. Check request processing time with logs
2. Optimize database queries
3. Move heavy operations to background jobs (Durable Objects)
4. Consider batch requests

### DNS Resolution

If custom domain isn't working:

1. Wait 5-10 minutes for DNS propagation
2. Verify DNS record points to worker
3. Check Cloudflare dashboard for errors

## Rollback

To rollback to previous version:

```bash
# View deployment history
wrangler deployments list

# Rollback to specific deployment
wrangler rollback --env production --message "Rolled back due to error"
```

## Environment-Specific Config

### Development (Local)

```env
SUPABASE_URL=https://dev.supabase.co
ENVIRONMENT=development
```

### Staging

```env
SUPABASE_URL=https://staging.supabase.co
ENVIRONMENT=staging
```

### Production

```env
SUPABASE_URL=https://prod.supabase.co
ENVIRONMENT=production
```

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Deploy to Cloudflare Workers

on:
  push:
    branches:
      - main

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      
      - run: npm ci
      - run: npm run type-check
      - run: npm run lint
      
      - run: npx wrangler publish --env production
        env:
          CLOUDFLARE_API_TOKEN: ${{ secrets.CLOUDFLARE_API_TOKEN }}
          CLOUDFLARE_ACCOUNT_ID: ${{ secrets.CLOUDFLARE_ACCOUNT_ID }}
```

Set in GitHub Secrets:
- `CLOUDFLARE_API_TOKEN`
- `CLOUDFLARE_ACCOUNT_ID`

## Cost Estimation

Cloudflare Workers pricing:

- **Free Tier**:
  - 100,000 requests/day
  - Full CPU time limit: 50ms per request
  - Unlimited outbound bandwidth

- **Paid Tier** ($15-200/month):
  - Increased CPU time: 400ms per request
  - Regional features
  - Priority support

For typical usage, the free tier should be sufficient. Upgrade if you need:
- Higher CPU time limits
- Custom domains without workers.dev subdomain
- DDoS protection

## Next Steps

1. Deploy to staging for testing
2. Test all endpoints with real JWT tokens
3. Configure monitoring and alerting
4. Deploy to production
5. Monitor performance and errors

## Support

- [Cloudflare Workers Docs](https://developers.cloudflare.com/workers/)
- [Wrangler CLI Reference](https://developers.cloudflare.com/workers/wrangler/install-and-update/)
- [Cloudflare Community](https://community.cloudflare.com/)

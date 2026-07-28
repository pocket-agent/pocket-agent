# Initialize from template

After **Use this template**, personalize the repository by copying files from `templates/` to the repo root.

## Run

Requires **Node.js 18+** only.

```bash
chmod +x scripts/init-from-template.sh   # once
./scripts/init-from-template.sh
```

Or:

```bash
npm run init
node scripts/init-from-template.mjs
```

**Step 1 — Maintainer:** Git identity from `git config` and `gh` CLI (accept or manual).  
**Step 2 — Repository:** owner, repo, worker name (`wrangler.toml`), and Dependabot bundler (npm).

```bash
./scripts/init-from-template.sh --yes
./scripts/init-from-template.sh --no-cleanup
```

After init, the `scripts/` folder is removed. Pair with [react-supabase-auth-template](https://github.com/open-templates/react-supabase-auth-template) using the same GitHub owner.

See [`templates/ABOUT_TEMPLATES.md`](../templates/ABOUT_TEMPLATES.md).

# About this folder

Adopter-ready files with placeholders (`owner-username`, `repo-name`, `author-*`, `paired-repo-name`).

Copied to the repo root by:

```bash
./scripts/init-from-template.sh
```

| File here | Destination |
|-----------|-------------|
| `package.json` | `package.json` |
| `README.md` | `README.md` |
| `LICENSE` | `LICENSE` |
| `CHANGELOG.md` | `CHANGELOG.md` |
| `INSTRUCTIONS.md` | `INSTRUCTIONS.md` |
| `wrangler.toml` | `wrangler.toml` |
| `dependabot.yml` | `.github/dependabot.yml` |
| `CODEOWNERS` | `.github/CODEOWNERS` |

Workflows under `.github/workflows/` are not copied — they use `github.repository_owner` at runtime.

#!/usr/bin/env node

import { initFromTemplate } from './lib/template-init/index.js';
import { CF_HONO_GEMINI_API_MANIFEST } from './lib/template-init/manifests/cf-hono-gemini-api.js';
import { printHelp } from './lib/template-init/parse-args.js';
import { brandHeader, error as printError } from './lib/template-init/terminal.js';

const args = process.argv.slice(2);
if (args.includes('--help') || args.includes('-h')) {
  brandHeader('cf hono supabase gemini api template');
  printHelp('cf-hono-supabase-gemini-api-template');
  process.exit(0);
}

initFromTemplate({
  manifest: CF_HONO_GEMINI_API_MANIFEST,
  includePackageName: false,
  includeAuthorStep: true,
  includeBundler: true,
  defaultBundler: 'npm',
  templateLabel: 'cf hono supabase gemini api template',
  authorStep: {
    stepTitle: 'maintainer (Git owner)',
    selectMessage: 'How should we set the package maintainer?',
    acceptLabel: 'Accept detected Git owner',
  },
  scriptsCleanup: 'all',
  extraReplacements: [['paired-repo-name', 'react-supabase-auth-template']],
  nextSteps: 'npm install, cp .env.example .dev.vars, then npm run dev',
}).catch((err) => {
  printError(`Init failed: ${err.message}`);
  process.exit(1);
});

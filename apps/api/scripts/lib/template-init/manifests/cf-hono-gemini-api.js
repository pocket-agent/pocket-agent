import { COMMON_MANIFEST } from './common.js';

/** @type {[string, string][]} */
export const CF_HONO_GEMINI_API_MANIFEST = [
  ...COMMON_MANIFEST.filter(([from]) => from !== 'INSTRUCTIONS.md'),
  ['package.json', 'package.json'],
  ['README.md', 'README.md'],
  ['INSTRUCTIONS.md', 'INSTRUCTIONS.md'],
  ['wrangler.toml', 'wrangler.toml'],
];

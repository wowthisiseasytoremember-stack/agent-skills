const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

/**
 * Audit Branding Skill Script
 *
 * Uses `ripgrep` (if available) or `grep` to find legacy project names across the codebase.
 */

const LEGACY_NAMES = [
  'iFlip',
  'FlipScale',
  'Flippd',
  'SmartFlipInventoryAR'
];

const IGNORE_DIRS = [
  '.git',
  '.github',
  'node_modules',
  'Documentation/_legacy_archive',
  'Docs/Audit',
  'skills_dev',
  '.aider.tags.cache.v4'
];

function auditBranding() {
  console.log("🔍 Auditing codebase for legacy branding...");

  LEGACY_NAMES.forEach(name => {
    console.log(`
--- Searching for: "${name}" ---`);
    const excludeStr = IGNORE_DIRS.map(dir => `--exclude-dir=${dir}`).join(' ');

    try {
      // Use grep -r to find matches, ignoring case-sensitive binary files and specified dirs
      const cmd = `grep -rnI "${name}" . ${excludeStr} | head -n 20`;
      const output = execSync(cmd, { encoding: 'utf-8' });

      if (output.trim()) {
        console.log(output);
      } else {
        console.log(`No matches found for "${name}".`);
      }
    } catch (error) {
      if (error.status === 1) {
        console.log(`No matches found for "${name}".`);
      } else {
        console.log(`Error searching for "${name}": ${error.message}`);
      }
    }
  });
}

auditBranding();

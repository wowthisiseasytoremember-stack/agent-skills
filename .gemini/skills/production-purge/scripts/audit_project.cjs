const fs = require('fs');
const path = require('path');

/**
 * Audit Project for Non-Production Files
 *
 * Scans the current directory for files that are typically excluded from App Store submission.
 */

const EXCLUSION_PATTERNS = [
  /\.md$/,                 // All Markdown files
  /\.sh$/,                 // Shell scripts
  /\.py$/,                 // Python scripts
  /\.cjs$/,                // Node.js scripts
  /\.env$/,                // Environment variables
  /\.aider/,               // Aider tool files
  /\.zsh_history/,         // History files
  /PLAN_.*\.md/,           // Specific planning files
  /TODO.*/,                // Todo lists
  /ROADMAP.*/,             // Roadmaps
  /AUDIT_.*\.md/,          // Audit reports
  /\.zip$/,                // Zip archives
  /Lexend\.zip/,           // Specific large asset
  /requirements\.txt/,     // Python requirements
  /image_processing_README\.md/ // Extra docs
];

const IGNORE_FILES = [
  'README.md',             // Usually kept as root doc
  'CLAUDE.md',             // Agent-specific context
  'CONVENTIONS.md',        // Project conventions
  'ARCHITECTURE.md',       // Architecture overview
  'MASTER_PLAN.md',        // Consolidated plan
  'AUDIT_SUMMARY.md'       // Consolidated audit
];

const IGNORE_DIRS = [
  '.git',
  '.github',
  'node_modules',
  'SmartFlipInventoryAR',  // Main project folder
  'SmartFlipWatch',        // Watch app folder
  'SmartFlipInventoryARTests',
  'SmartFlipInventoryARUITests',
  'skills_dev',            // Development folder
  'Documentation',         // Documentation archive
  'Docs',                  // Current documentation
  'Config',                // Config directory
  'Scripts',               // Scripts directory
  'FLIPPD'                 // Research directory
];

function auditDir(dir) {
  let results = [];
  const files = fs.readdirSync(dir);

  for (const file of files) {
    const fullPath = path.join(dir, file);
    const stats = fs.statSync(fullPath);

    if (stats.isDirectory()) {
      if (!IGNORE_DIRS.includes(file)) {
        results.push({ type: 'DIR', path: fullPath });
      }
    } else {
      if (IGNORE_FILES.includes(file)) continue;

      const isMatch = EXCLUSION_PATTERNS.some(pattern => pattern.test(file));
      if (isMatch) {
        results.push({ type: 'FILE', path: fullPath });
      }
    }
  }

  return results;
}

const auditResults = auditDir(process.cwd());

if (auditResults.length === 0) {
  console.log("Success: No non-production files found in the root directory.");
} else {
  console.log("Audit Found Identified Items:");
  auditResults.forEach(item => {
    console.log(`- [${item.type}] ${item.path}`);
  });
}

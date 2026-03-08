#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// Configuration
const BRIDGE_FILES = [
  'CLAUDE.md',
  '.cursorrules',
  '.windsurfrules',
  'CODEX.md',
  'ANTIGRAVITY.md'
];

const STACK_CONVENTIONS = {
  'react-ts': `* **Default Tech Stack:** React (TypeScript) with Vanilla CSS.
* **Styling:** Prefer Vanilla CSS for maximum flexibility. Avoid TailwindCSS unless explicitly requested.
* **Architecture:** Component-based; Use Hooks for state management.`,
  'node-express': `* **Default Tech Stack:** Node.js (Express) with TypeScript.
* **Architecture:** Service-Controller pattern; Wrap third-party APIs in a service layer.`,
  'swift-ios': `* **Default Tech Stack:** Modern Swift (SwiftUI/Combine/Async-Await).
* **Architecture:** Clean Boundaries; Wrap third-party APIs in a service layer.`,
  'python-fastapi': `* **Default Tech Stack:** Python (FastAPI).
* **Architecture:** Dependency Injection; Type hinting for all endpoints.`
};

// Main Scaffolding Logic
async function main() {
  const args = process.argv.slice(2);
  const projectName = args[0] || 'new-project';
  const stack = args[1] || 'generic';
  const projectPath = path.resolve(process.cwd(), projectName);

  console.log(`🚀 Scaffolding new project: ${projectName} (${stack})`);

  try {
    // 1. Create Project Directory
    if (!fs.existsSync(projectPath)) {
      fs.mkdirSync(projectPath, { recursive: true });
    } else {
      console.warn(`⚠️ Warning: Directory ${projectName} already exists.`);
    }

    // 2. Setup Mandate File (GEMINI.md)
    const geminiTemplatePath = path.join(__dirname, '..', 'assets', 'GEMINI.md.template');
    let geminiContent = fs.readFileSync(geminiTemplatePath, 'utf8');

    const conventions = STACK_CONVENTIONS[stack] || '* **Architecture:** Standard clean architecture with clear separation of concerns.';
    
    geminiContent = geminiContent
      .replace(/{{PROJECT_NAME}}/g, projectName)
      .replace(/{{PROJECT_DESCRIPTION}}/g, `Standard foundation for ${projectName} initialized by Project Scaffolder.`)
      .replace(/{{STACK_SPECIFIC_CONVENTIONS}}/g, conventions);

    fs.writeFileSync(path.join(projectPath, 'GEMINI.md'), geminiContent);
    console.log('✅ Created GEMINI.md');

    // 3. Setup Bridge Files
    const bridgeTemplatePath = path.join(__dirname, '..', 'assets', 'bridge', 'BRIDGE.md.template');
    const bridgeContent = fs.readFileSync(bridgeTemplatePath, 'utf8');

    BRIDGE_FILES.forEach(file => {
      fs.writeFileSync(path.join(projectPath, file), bridgeContent);
      console.log(`✅ Created ${file}`);
    });

    // 4. Initialize Stack Dependencies
    process.chdir(projectPath);
    if (stack === 'react-ts' || stack === 'node-express') {
      console.log('📦 Initializing npm project...');
      execSync('npm init -y', { stdio: 'inherit' });
    } else if (stack === 'python-fastapi') {
      console.log('🐍 Initializing python project...');
      // Minimal python init (requirements.txt)
      fs.writeFileSync('requirements.txt', 'fastapi\nuvicorn\n');
    }

    // 5. Setup Basic Configs
    const gitignore = `.env
node_modules/
dist/
.DS_Store
*.log`;
    fs.writeFileSync('.gitignore', gitignore);
    console.log('✅ Created .gitignore');

    console.log(`\n✨ Project ${projectName} is ready!`);
    console.log(`📍 Location: ${projectPath}`);
    console.log('👉 Start by reviewing your GEMINI.md for architectural mandates.');

  } catch (error) {
    console.error(`❌ Error during scaffolding: ${error.message}`);
    process.exit(1);
  }
}

main();

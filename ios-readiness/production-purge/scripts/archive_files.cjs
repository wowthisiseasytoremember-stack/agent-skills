const fs = require('fs');
const path = require('path');

/**
 * Move Non-Production Files to Archive
 *
 * Moves a provided list of items into a specified archive directory.
 */

const ARCHIVE_DIR_NAME = '_SubmissionArchive';
const PROJECT_ROOT = process.cwd();
const ARCHIVE_PATH = path.join(PROJECT_ROOT, ARCHIVE_DIR_NAME);

// Ensure archive directory exists
if (!fs.existsSync(ARCHIVE_PATH)) {
  fs.mkdirSync(ARCHIVE_PATH);
}

// Arguments are expected to be the paths of files/folders to move
const itemsToMove = process.argv.slice(2);

if (itemsToMove.length === 0) {
  console.log("No items provided to move.");
  process.exit(1);
}

itemsToMove.forEach(itemPath => {
  const fullItemPath = path.isAbsolute(itemPath) ? itemPath : path.resolve(itemPath);
  const itemName = path.basename(fullItemPath);
  const targetPath = path.join(ARCHIVE_PATH, itemName);

  if (fs.existsSync(fullItemPath)) {
    try {
      // Use fs.renameSync if on same device, or move manually if not
      fs.renameSync(fullItemPath, targetPath);
      console.log(`Success: Moved [${itemName}] to ${ARCHIVE_DIR_NAME}/`);
    } catch (error) {
      console.log(`Error moving [${itemName}]: ${error.message}`);
    }
  } else {
    console.log(`Warning: [${itemName}] does not exist, skipping.`);
  }
});

import os
import re
import json
from datetime import datetime

# CONFIGURATION
TARGET_DIR = r"C:\Users\wowth\Desktop\projects\FlipScale"
INDEX_OUTPUT = os.path.join(TARGET_DIR, "CODEBASE_INDEX.json")
AUDIT_OUTPUT = os.path.join(TARGET_DIR, "ARCHITECTURE_AUDIT.md")
DEPENDENCY_GRAPH_OUTPUT = os.path.join(TARGET_DIR, "DEPENDENCY_GRAPH.json")

# PATTERNS
SYMBOL_PATTERN = re.compile(r"(struct|class|actor|enum|protocol)\s+([A-Z][a-zA-Z0-9_]+)")
IMPORT_PATTERN = re.compile(r"import\s+([a-zA-Z0-9_]+)")
# Improved pattern to catch var name: Double
DOUBLE_PATTERN = re.compile(r"(var|let)\s+([a-zA-Z0-9_]*?(price|cost|amount|profit|roi|fee|revenue|balance|tax|total|shipping))\s*?:\s*?Double", re.IGNORECASE)
SWIFTUI_IMPORT = "import SwiftUI"

def generate_dependency_graph(root_path):
    dependency_graph = {}
    for root, dirs, files in os.walk(root_path):
        if any(x in root for x in [".build", ".git", ".ai"]):
            continue
        for file in files:
            if file.endswith(".swift"):
                file_path = os.path.join(root, file)
                
                module_name = ""
                # Determine module name based on file path heuristic
                if "Sources" in file_path and "FlipScale" in file_path:
                    # If the file is in 'Sources/FlipScale', it's part of the main app module
                    module_name = "FlipScaleApp" 
                elif "Modules" in file_path:
                    # For files within Modules, the parent folder is the module name
                    parts = file_path.split(os.sep)
                    try:
                        module_index = parts.index("Modules")
                        module_name = parts[module_index + 1]
                    except ValueError:
                        module_name = "UnknownModule"
                else:
                    module_name = "UnknownModule"
                
                if module_name not in dependency_graph:
                    dependency_graph[module_name] = []

                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                        for match in IMPORT_PATTERN.finditer(content):
                            imported_module = match.group(1)
                            if imported_module not in dependency_graph[module_name] and imported_module != module_name:
                                dependency_graph[module_name].append(imported_module)
                except Exception as e:
                    print(f"Error reading {file_path} for dependency graph: {e}")
    
    # Clean up empty lists and sort dependencies
    cleaned_graph = {k: sorted(v) for k, v in dependency_graph.items() if v}

    with open(DEPENDENCY_GRAPH_OUTPUT, "w", encoding="utf-8") as f:
        json.dump(cleaned_graph, f, indent=2)
    print(f"✅ Dependency Graph generated: {DEPENDENCY_GRAPH_OUTPUT}")

def scan_codebase(root_path):
    index = {
        "generated_at": datetime.now().isoformat(),
        "symbols": [],
        "files": [],
        "violations": []
    }
    
    audit_report = [
        "# 🏗️ ARCHITECTURE AUDIT REPORT",
        f"**Generated at:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "---",
        "## 🚨 ARCHITECTURAL VIOLATIONS",
        "| File | Violation | Context |",
        "| :--- | :--- | :--- |"
    ]
    
    violations_found = []

    for root, dirs, files in os.walk(root_path):
        # Skip build and hidden directories
        if any(x in root for x in [".build", ".git", ".ai"]):
            continue
            
        for file in files:
            if file.endswith(".swift") or file.endswith(".md"):
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, root_path)
                
                index["files"].append({
                    "path": rel_path,
                    "extension": os.path.splitext(file)[1]
                })
                
                if file.endswith(".swift"):
                    try:
                        with open(file_path, "r", encoding="utf-8") as f:
                            lines = f.readlines()
                            content = "".join(lines)
                            
                            # 1. Extract Symbols
                            for match in SYMBOL_PATTERN.finditer(content):
                                # Manually count newlines to get line number
                                line_no = content[:match.start()].count('\n') + 1
                                index["symbols"].append({
                                    "type": match.group(1),
                                    "name": match.group(2),
                                    "file": rel_path,
                                    "line": line_no
                                })
                            
                            # 2. Detect Violations: Double for Money
                            if "Models" in rel_path or "Services" in rel_path:
                                for i, line in enumerate(lines):
                                    if DOUBLE_PATTERN.search(line):
                                        v = f"**Double for Money:** `{line.strip()}`"
                                        violations_found.append([rel_path, "Precision", v])
                                        index["violations"].append({
                                            "file": rel_path,
                                            "line": i + 1,
                                            "type": "Precision",
                                            "content": line.strip()
                                        })
                            
                            # 3. Detect Violations: SwiftUI in Services
                            if "Services" in rel_path and SWIFTUI_IMPORT in content:
                                v = f"**SwiftUI in Service:** Isolated business logic must not import UI frameworks."
                                violations_found.append([rel_path, "Isolation", v])
                                index["violations"].append({
                                    "file": rel_path,
                                    "type": "Isolation",
                                    "content": "SwiftUI Import"
                                })
                    except Exception as e:
                        print(f"Error reading {file_path}: {e}")

    # Add violations to report
    if not violations_found:
        audit_report.append("| None | ✅ | No violations detected. |")
    else:
        for v in violations_found:
            audit_report.append(f"| {v[0]} | {v[1]} | {v[2]} |")

    # Add Symbol Summary
    audit_report.append("\n## 📋 SYMBOL SUMMARY")
    audit_report.append(f"- **Total Files:** {len(index['files'])}")
    audit_report.append(f"- **Total Symbols:** {len(index['symbols'])}")
    audit_report.append(f"- **Total Violations:** {len(index['violations'])}")
    
    # Save Outputs
    with open(INDEX_OUTPUT, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2)
        
    with open(AUDIT_OUTPUT, "w", encoding="utf-8") as f:
        f.write("\n".join(audit_report))

    print(f"✅ Codebase Map generated: {INDEX_OUTPUT}")
    print(f"✅ Architecture Audit generated: {AUDIT_OUTPUT}")
    
    generate_dependency_graph(root_path)

if __name__ == "__main__":
    scan_codebase(TARGET_DIR)

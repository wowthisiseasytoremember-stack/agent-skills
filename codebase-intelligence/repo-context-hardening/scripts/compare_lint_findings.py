#!/usr/bin/env python3
import json
import sys

def load_findings(json_path):
    with open(json_path, 'r') as f:
        data = json.load(f)
    findings = []
    for level in ('error', 'warning'):
        for f in data.get('findings', []):
            if f.get('level') == level:
                # Identity: (level, code, path, message)
                findings.append((
                    f['level'],
                    f.get('code', ''),
                    f.get('path', ''),
                    f.get('message', '')
                ))
    return set(findings)

def main():
    if len(sys.argv) != 3:
        print("Usage: compare_lint_findings.py <pre_json> <post_json>", file=sys.stderr)
        sys.exit(1)
    
    pre_file = sys.argv[1]
    post_file = sys.argv[2]
    
    pre_findings = load_findings(pre_file)
    post_findings = load_findings(post_file)
    
    new_findings = post_findings - pre_findings
    
    if new_findings:
        print("New lint findings detected:", file=sys.stderr)
        for finding in sorted(new_findings):
            print(f"  {finding}", file=sys.stderr)
        sys.exit(1)
    else:
        print("No new lint findings.", file=sys.stderr)
        sys.exit(0)

if __name__ == '__main__':
    main()
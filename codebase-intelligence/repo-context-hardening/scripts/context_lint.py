#!/usr/bin/env python3
import argparse
import json
import os
import re
import sys
from urllib.parse import urlparse

def is_http_url(url):
    try:
        result = urlparse(url)
        return result.scheme in ("http", "https")
    except:
        return False

def extract_links(markdown_text):
    # Pattern for [text](url) and [text][ref] and [ref]: url
    # We'll handle [text](url) and [text][ref] and then later resolve [ref] from the reference-style links.
    # This is a simple implementation; for completeness we should also handle <url> and [text] [ref] etc.
    # But for the purpose of this canary, we focus on the common case.
    link_pattern = re.compile(r'\[([^\]]*)\]\(([^)]+)\)')
    ref_pattern = re.compile(r'\[([^\]]*)\]\[([^\]]*)\]')
    # We'll also look for reference-style link definitions: [ref]: url
    ref_def_pattern = re.compile(r'^\[([^\]]*)\]:\s*(\S+)', re.MULTILINE)
    
    links = []  # each link: (text, url, line_number, raw)
    refs = {}   # ref name -> url
    
    # First, collect reference definitions
    for match in ref_def_pattern.finditer(markdown_text):
        ref_name, url = match.groups()
        refs[ref_name] = url
    
    # Then, find inline links
    for match in link_pattern.finditer(markdown_text):
        text, url = match.groups()
        links.append((text, url, match.start(), match.group(0)))
    
    # Then, find reference-style links
    for match in ref_pattern.finditer(markdown_text):
        text, ref_name = match.groups()
        if ref_name in refs:
            url = refs[ref_name]
            links.append((text, url, match.start(), match.group(0)))
        # If ref_name is empty, it's a collapsed link [text][] -> ref_name = text
        elif ref_name == '':
            if text in refs:
                url = refs[text]
                links.append((text, url, match.start(), match.group(0)))
    
    return links, refs

def check_links_in_file(file_path, root_dir):
    """Return list of broken links in the given markdown file.
    Each broken link is a dict: {level, code, path, message}
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return [{
            "level": "error",
            "code": "FILE_READ_ERROR",
            "path": os.path.relpath(file_path, root_dir),
            "message": f"Failed to read file: {e}"
        }]
    
    links, refs = extract_links(content)
    broken = []
    
    for text, url, pos, raw in links:
        # Skip empty URLs
        if not url.strip():
            continue
        # Skip http/https URLs
        if is_http_url(url):
            continue
        # Skip mailto and other schemes
        if url.startswith('mailto:') or url.startswith('tel:'):
            continue
        
        # Resolve relative URL relative to the directory of the markdown file
        link_dir = os.path.dirname(file_path)
        target_path = os.path.normpath(os.path.join(link_dir, url))
        
        # Check if the target exists
        if not os.path.exists(target_path):
            broken.append({
                "level": "error",
                "code": "BROKEN_LINK",
                "path": os.path.relpath(file_path, root_dir),
                "message": f"Broken link: {url} (resolved to {target_path})"
            })
    
    return broken

def main():
    parser = argparse.ArgumentParser(description='Lint repository context for broken links in Markdown files.')
    parser.add_argument('--root', required=True, help='Root directory to scan')
    parser.add_argument('--json', required=True, help='Output JSON file path')
    args = parser.parse_args()
    
    root_dir = os.path.abspath(args.root)
    if not os.path.isdir(root_dir):
        print(f"Error: root directory '{root_dir}' does not exist or is not a directory", file=sys.stderr)
        sys.exit(1)
    
    all_findings = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Skip hidden directories and common non-content directories
        dirnames[:] = [d for d in dirnames if not d.startswith('.') and d not in ('node_modules', '__pycache__', '.git')]
        for filename in filenames:
            if filename.endswith('.md'):
                file_path = os.path.join(dirpath, filename)
                findings = check_links_in_file(file_path, root_dir)
                all_findings.extend(findings)
    
    # Deduplicate findings by (level, code, path, message)
    unique_findings = []
    seen = set()
    for f in all_findings:
        key = (f['level'], f['code'], f['path'], f['message'])
        if key not in seen:
            seen.add(key)
            unique_findings.append(f)
    
    # Sort for consistent output
    unique_findings.sort(key=lambda x: (x['path'], x['message']))
    
    counts = {
        "error": sum(1 for f in unique_findings if f['level'] == 'error'),
        "warning": sum(1 for f in unique_findings if f['level'] == 'warning')
    }
    
    output = {
        "counts": counts,
        "findings": unique_findings
    }
    
    with open(args.json, 'w') as f:
        json.dump(output, f, indent=2)
    
    # Exit with 0 if no errors, but we don't fail on warnings
    sys.exit(0 if counts["error"] == 0 else 1)

if __name__ == '__main__':
    main()
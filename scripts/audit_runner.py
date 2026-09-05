import os
import re
import json

repo_path = r"C:\Users\HP\erpnext-env\erpnext-saudi-demo"

patterns = {
    "copyright": re.compile(r"copyright|\(c\)|©", re.IGNORECASE),
    "license_mention": re.compile(r"license|agpl|gpl|mit|apache|bsd|lgpl|mpl", re.IGNORECASE),
    "author_maintainer": re.compile(r"author|maintainer|contributor|developer|created by", re.IGNORECASE),
    "email_pattern": re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"),
    "repo_urls": re.compile(r"github\.com/[^\s\"\'>\)]+|gitlab\.com/[^\s\"\'>\)]+"),
    "lavaloon": re.compile(r"lavaloon", re.IGNORECASE),
    "frappe_erpnext": re.compile(r"frappe\.io|erpnext\.com|frappeframework\.com", re.IGNORECASE),
    "accore": re.compile(r"accore", re.IGNORECASE)
}

findings = {k: [] for k in patterns}
file_summary = {}

for root, dirs, files in os.walk(repo_path):
    if ".git" in dirs:
        dirs.remove(".git")
    for f in files:
        fpath = os.path.join(root, f)
        rel_path = os.path.relpath(fpath, repo_path)
        file_summary[rel_path] = []
        try:
            with open(fpath, "r", encoding="utf-8", errors="ignore") as fp:
                for line_no, line in enumerate(fp, 1):
                    sline = line.strip()
                    for k, pat in patterns.items():
                        m = pat.search(sline)
                        if m:
                            item = {
                                "file": rel_path,
                                "line": line_no,
                                "match": m.group(0),
                                "content": sline[:140]
                            }
                            findings[k].append(item)
                            file_summary[rel_path].append((k, line_no, sline[:100]))
        except Exception as e:
            pass

print("=== SUMMARY OF MATCHES BY CATEGORY ===")
for k, v in findings.items():
    print(f"{k}: {len(v)} occurrences")

print("\n=== TOP SPECIFIC FINDINGS FOR EMAILS ===")
emails_seen = set()
for item in findings["email_pattern"]:
    m = patterns["email_pattern"].findall(item["content"])
    for em in m:
        if em not in emails_seen:
            emails_seen.add(em)
            print(f"  {em} -> found in {item['file']}:{item['line']}")

print("\n=== TOP SPECIFIC FINDINGS FOR REPO URLS ===")
repos_seen = set()
for item in findings["repo_urls"]:
    m = patterns["repo_urls"].findall(item["content"])
    for r in m:
        if r not in repos_seen:
            repos_seen.add(r)
            print(f"  {r} -> found in {item['file']}:{item['line']}")

print("\n=== SPECIFIC FINDINGS FOR LAVALOON ===")
for item in findings["lavaloon"][:30]:
    print(f"  {item['file']}:{item['line']} -> {item['content']}")

print("\n=== SPECIFIC FINDINGS FOR COPYRIGHT ===")
for item in findings["copyright"][:30]:
    print(f"  {item['file']}:{item['line']} -> {item['content']}")

with open(r"C:\Users\HP\erpnext-env\erpnext-saudi-demo\audit_full_results.json", "w", encoding="utf-8") as out:
    json.dump(findings, out, indent=2)

print("\nFull results written to audit_full_results.json")

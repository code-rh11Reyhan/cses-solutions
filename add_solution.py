#!/usr/bin/env python3
"""
CSES Auto-Tracker
------------------
Run this every time you solve a CSES problem. It will:
  1. File your solution into solutions/<category>/<number>-<slug>.<ext>
  2. Update solutions.json (the database)
  3. Regenerate README.md with a clean, grouped, stats-tracked table
  4. git add, commit, and push (unless you pass --no-push)

Usage (flags):
    python3 add_solution.py --file sol.cpp --number 1068 \
        --problem "Weird Algorithm" --category "Introductory Problems" \
        --difficulty Easy

Usage (interactive — just run it and answer prompts):
    python3 add_solution.py --file sol.cpp

First-time setup: see SETUP.md
"""

import argparse
import json
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent
DB_PATH = REPO_ROOT / "solutions.json"
README_PATH = REPO_ROOT / "README.md"
SOLUTIONS_DIR = REPO_ROOT / "solutions"

CSES_CATEGORIES = [
    "Introductory Problems",
    "Sorting and Searching",
    "Dynamic Programming",
    "Graph Algorithms",
    "Range Queries",
    "Tree Algorithms",
    "Mathematics",
    "String Algorithms",
    "Geometry",
    "Advanced Techniques",
    "Additional Problems",
]

DIFFICULTY_EMOJI = {
    "easy": "🟢",
    "medium": "🟡",
    "hard": "🔴",
}


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def load_db() -> list:
    if DB_PATH.exists():
        with open(DB_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_db(db: list) -> None:
    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(db, f, indent=2)


def run(cmd, check=True):
    result = subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True)
    if check and result.returncode != 0:
        print(f"  [warn] command failed: {' '.join(cmd)}")
        if result.stderr.strip():
            print(f"  [warn] {result.stderr.strip()}")
    return result


def prompt(msg, default=None, choices=None):
    suffix = f" [{default}]" if default else ""
    while True:
        val = input(f"{msg}{suffix}: ").strip()
        if not val and default is not None:
            val = default
        if not val:
            print("  This field is required.")
            continue
        if choices and val not in choices:
            # allow free text too, just warn
            print(f"  (not in standard list, using as custom category)")
        return val


def build_readme(db: list) -> str:
    total = len(db)
    by_category = {}
    for entry in db:
        by_category.setdefault(entry["category"], []).append(entry)

    lines = []
    lines.append("# CSES Problem Set — Solutions\n")
    lines.append(
        f"![Solved](https://img.shields.io/badge/solved-{total}%2F300-blue) "
        f"![Last Updated](https://img.shields.io/badge/updated-{date.today().isoformat()}-informational)\n"
    )
    lines.append(
        "Automated solution tracker for the [CSES Problem Set](https://cses.fi/problemset/). "
        "Every entry below is filed in automatically the moment a problem is solved — "
        "see `add_solution.py`.\n"
    )
    lines.append("## Progress\n")
    lines.append(f"**{total} / 300** problems solved.\n")

    # ordered category summary
    lines.append("| Category | Solved |")
    lines.append("|---|---|")
    for cat in CSES_CATEGORIES:
        count = len(by_category.get(cat, []))
        if count:
            lines.append(f"| {cat} | {count} |")
    # any custom categories not in the standard list
    for cat in by_category:
        if cat not in CSES_CATEGORIES:
            lines.append(f"| {cat} | {len(by_category[cat])} |")
    lines.append("")

    lines.append("## Solutions\n")
    ordered_cats = [c for c in CSES_CATEGORIES if c in by_category] + [
        c for c in by_category if c not in CSES_CATEGORIES
    ]
    for cat in ordered_cats:
        entries = sorted(by_category[cat], key=lambda e: e["number"])
        lines.append(f"### {cat}\n")
        lines.append("| # | Problem | Difficulty | Solution | Solved On |")
        lines.append("|---|---|---|---|---|")
        for e in entries:
            diff_emoji = DIFFICULTY_EMOJI.get(e.get("difficulty", "").lower(), "")
            diff_label = f"{diff_emoji} {e['difficulty']}".strip() if e.get("difficulty") else "—"
            cses_link = f"[{e['number']}](https://cses.fi/problemset/task/{e['number']})"
            sol_link = f"[{Path(e['filepath']).name}]({e['filepath']})"
            lines.append(
                f"| {cses_link} | {e['name']} | {diff_label} | {sol_link} | {e['date']} |"
            )
        lines.append("")

    lines.append("---\n*Generated automatically by `add_solution.py`. Do not edit by hand — it will be overwritten.*")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="File a solved CSES solution into the repo and push it.")
    parser.add_argument("--file", required=True, help="Path to your solution source file")
    parser.add_argument("--number", type=int, help="CSES task number")
    parser.add_argument("--problem", help="Problem name")
    parser.add_argument("--category", help="CSES category")
    parser.add_argument("--difficulty", default="", help="Easy / Medium / Hard (optional)")
    parser.add_argument("--notes", default="", help="Optional notes about your approach")
    parser.add_argument("--no-push", action="store_true", help="Commit locally but don't git push")
    parser.add_argument("--message", help="Custom commit message")
    args = parser.parse_args()

    src = Path(args.file).expanduser().resolve()
    if not src.exists():
        print(f"Error: file not found: {src}")
        sys.exit(1)

    number = args.number or int(prompt("CSES problem number (e.g. 1068)"))
    problem = args.problem or prompt("Problem name (e.g. Weird Algorithm)")
    category = args.category or prompt(
        f"Category ({', '.join(CSES_CATEGORIES)})", choices=CSES_CATEGORIES
    )
    fully_specified = bool(args.number and args.problem and args.category)
    if args.difficulty:
        difficulty = args.difficulty
    elif fully_specified:
        difficulty = ""
    else:
        difficulty = input("Difficulty (Easy/Medium/Hard, optional): ").strip()

    if args.notes:
        notes = args.notes
    elif fully_specified:
        notes = ""
    else:
        notes = input("Notes (optional): ").strip()

    db = load_db()

    # dedupe: same number overwrites previous entry (resubmission)
    db = [e for e in db if e["number"] != number]

    cat_slug = slugify(category)
    prob_slug = slugify(problem)
    target_dir = SOLUTIONS_DIR / cat_slug
    target_dir.mkdir(parents=True, exist_ok=True)
    target_path = target_dir / f"{number}-{prob_slug}{src.suffix}"
    target_path.write_bytes(src.read_bytes())

    entry = {
        "number": number,
        "name": problem,
        "category": category,
        "difficulty": difficulty,
        "notes": notes,
        "date": date.today().isoformat(),
        "filepath": str(target_path.relative_to(REPO_ROOT)),
    }
    db.append(entry)
    save_db(db)

    readme = build_readme(db)
    README_PATH.write_text(readme, encoding = "utf-8")

    print(f"\n✔ Filed: {entry['filepath']}")
    print(f"✔ README.md regenerated ({len(db)} problems tracked)")

    # git operations
    run(["git", "add", "-A"])
    commit_msg = args.message or f"Solved {number}: {problem}"
    commit_result = run(["git", "commit", "-m", commit_msg], check=False)
    if commit_result.returncode != 0:
        print("  [info] nothing new to commit (or git commit failed — check output above)")
    else:
        print(f"✔ Committed: \"{commit_msg}\"")

    if not args.no_push:
        push_result = run(["git", "push"], check=False)
        if push_result.returncode == 0:
            print("✔ Pushed to GitHub")
        else:
            print("  [warn] push failed — run `git push` manually to see the error (auth/remote not set up?)")
    else:
        print("  (skipped push, --no-push set)")


if __name__ == "__main__":
    main()
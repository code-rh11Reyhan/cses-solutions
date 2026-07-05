# CSES Auto-Tracker — Setup

## 1. Create the GitHub repo
On GitHub, create a new repo, e.g. `cses-solutions`. Don't initialize it with a README (we generate our own).

## 2. Clone it locally and drop in these files
```bash
git clone git@github.com:<your-username>/cses-solutions.git
cd cses-solutions
```
Copy `add_solution.py` into this folder. That's it — `solutions.json`, `README.md`, and the `solutions/` folder are all created automatically on first run.

## 3. Make sure `git push` works without typing a password
Easiest: use SSH remotes (`git@github.com:...`) with an SSH key added to your GitHub account.
If you're using HTTPS, set up a [personal access token](https://github.com/settings/tokens) and cache it:
```bash
git config --global credential.helper store
```
(Do this once — after that `git push` won't prompt you.)

## 4. Solve a problem, then run:
```bash
python3 add_solution.py --file mysolution.cpp --number 1068 --problem "Weird Algorithm" --category "Introductory Problems" --difficulty Easy
```
That's it. It files the code, updates the README table + progress badge, commits, and pushes.

### Interactive mode
Forget the flags — just run:
```bash
python3 add_solution.py --file mysolution.cpp
```
and it'll ask you for the rest.

### Handy alias (optional)
Add this to your `~/.bashrc` / `~/.zshrc`:
```bash
alias solved="python3 ~/path/to/cses-solutions/add_solution.py"
```
Then from anywhere:
```bash
solved --file ~/code/1068.cpp --number 1068 --problem "Weird Algorithm" --category "Introductory Problems"
```

## Standard CSES categories (for `--category`)
- Introductory Problems
- Sorting and Searching
- Dynamic Programming
- Graph Algorithms
- Range Queries
- Tree Algorithms
- Mathematics
- String Algorithms
- Geometry
- Advanced Techniques
- Additional Problems

You can also pass a custom category — it'll just show up as its own section.

## Notes
- Re-running with the same `--number` overwrites that entry (handles resubmissions/optimizations cleanly).
- `--no-push` commits locally without pushing, if you want to batch several before syncing.
- `README.md` and `solutions.json` are regenerated every run — don't hand-edit `README.md`, your edits will be overwritten.
- Zero external dependencies — pure Python 3 standard library.
### **Prompts & Requests You Made**

1. **Graph logic**
   * Asked if your cost logic was correct: if the algorithm returns `False`, then those nodes shouldn’t be used in weight calculations.
   * Asked whether to change the test or the algorithm (decided to rewrite for consistency).
   * Asked if heuristics should be split into a separate file (`heuristics.py`).
   * Requested a **full `heuristics.py` file**.
   * Reported an error: `from core import heuristics as h` couldn’t find the module → asked to update A* and Greedy algorithms to support **multiple heuristics**.
   * Asked for updates to **all files** showing how and where to plug in heuristics for later extension.
   * Asked if you were **missing any algorithms** and requested a list of potentially useful ones for the project.
   * Asked for updates to your **log**.
2. **Git / Branching**
   * Noted a pull request from `dev` → `main` had **merge conflicts**, and asked for a single command to force-push.
   * Asked if `git push origin main --force` would work as a one-liner.
   * Asked whether your **main branch** should serve as a stable backup while `dev` is your working branch.
   * Created `github notes.md` and noted `git push origin dev` said “everything up to date.”
3. **Other project-related questions**
   * Asked whether the cost was “correctly implemented” (in tests).
   * Checked consistency of algorithm/test return values.
   * Wanted to confirm if **heuristics should be separated** .
   * Wanted **block placeholders** to easily extend heuristics later.

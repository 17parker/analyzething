Setup steps

Create dev branch locally and push it

# from inside your repo
git checkout -b dev
git push -u origin dev


Switch between branches

Work normally on dev:

git checkout dev


When ready to publish a stable version, merge into main:

git checkout main
git pull origin main        # make sure main is up to date
git merge dev               # bring in changes
git push origin main        # update GitHub stable branch

Recommended habits

Always commit and push to dev while you’re coding.

Treat main as “release only” — merge when you reach a checkpoint (e.g., features completed, passing tests).

If you want to be extra clean, run your test suite before merging into main.

Optional GitHub settings

Make main the default branch on GitHub (so people see the stable branch first).

Protect main (Settings → Branches) so you can’t accidentally push there directly.

Require merges only.

Allow yourself to override if needed.

1. Check what Git sees
git status


You should see something like:

Untracked files:
  docs/github_notes.md

2. Add the file
git add docs/github_notes.md

3. Commit the file
git commit -m "Add GitHub workflow notes"

4. Push to your dev branch
git push origin dev


Now your docs/github_notes.md will show up on GitHub in the dev branch.

⚡ Pro tip:
If you want all new files to be picked up in one shot:

git add .
git commit -m "Update project files"
git push origin dev
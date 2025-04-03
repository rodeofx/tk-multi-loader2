## Retrieve updates from upstream
This repository is a fork of https://github.com/shotgunsoftware/tk-multi-loader2.

Here is the steps to follow if you want to retrieve the upstream updates into this repository:
* Go on our `master` branch and pull it
* Make sure the upstream is set
  * `git remote add upstream https://github.com/shotgunsoftware/tk-multi-loader2.git`
  * `git fetch upstream`
* Rebase `upstream/master` into our `master`
* If you want to limit the update to a specific commit or tag
  * `git reset <commmit hash or tag>`
* Push the `master` to update the remote side
* Go on our `master_rdo` branch and pull it
* Rebase our `master` into our `master_rdo`
* Resolve potential conflicts
* Make the other code change you need
* Squash all your commits with previous "RodeoFx edits" commit (we want to keep all our changes in a single commit)
* Push your work
* Create a new tag with a `_rdo` suffix
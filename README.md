## Stow Lite

Implements a behavior very similar to a small subset of [GNU stow][stow] operations. It is sufficient for my needs when working on Windows.
[stow]: http://www.gnu.org/software/stow/

If the name of any file or directory in the stow directory matches one of the regular expressions in `.stow-local-ignore`, then it is ignored. If a directory is not ignored, then it is symlinked using Windows' `mklink` command. There is no way to ignore certain files/directories in a symlinked directory. No attempt is made to determine ownership of files; files will be overwritten with no warning.

> Please note that this tool's behavior is different from stow's default behavior.

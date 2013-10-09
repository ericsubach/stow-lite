## Stow Lite

Implements a behavior very similar to a small subset of [GNU stow][stow] operations. It is sufficient for my needs when working on Windows.
[stow]: http://www.gnu.org/software/stow/

If the name of any file or directory in the stow directory matches one of the regular expressions in .stow-local-ignore, then it is ignored. If a directory is not ignored, then it is linked. There is no way to ignore certain files/directories in a linked directory. Please note that this is different from stow's default behavior.

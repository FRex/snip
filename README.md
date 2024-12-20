# snip

A script using [junegunn/fzf](https://github.com/junegunn/fzf)
and (optionally) [sharkdp/bat](https://github.com/sharkdp/bat) to present a list of files
from a directory and dump a chosen file to stdout, for purpose of managing
small repetable snippets of text or code. If option `-w` is passed then file is instead
copied to current directory using `shutil.copy` instead of being printed.

Requires (and works on any) Python 3.6 or above, as tested using
[https://github.com/FRex/anypython](https://github.com/FRex/anypython),
due to usage of [f-strings](https://docs.python.org/3/reference/lexical_analysis.html#f-strings).

Also requires having [junegunn/fzf](https://github.com/junegunn/fzf), but
[sharkdp/bat](https://github.com/sharkdp/bat) is optional (`cat` will be used if it's not available).

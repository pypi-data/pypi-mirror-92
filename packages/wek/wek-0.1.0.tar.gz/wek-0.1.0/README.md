# wek

[![PyPI version](https://badge.fury.io/py/wek.svg)](https://badge.fury.io/py/wek)
[![GitHub license](https://img.shields.io/github/license/kmaork/wek)](https://github.com/kmaork/wek/blob/master/LICENSE.txt)

Is your windows machine too sleepy? Use `wek` to temporarily prevent it from fading away!

1. Install wek: `pip install wek`
2. Press WinKey+R, type wek and run. A popup window will show up, and as long as this window is not closed, your machine won't go to sleep.

`wek` asks your system to stay awake by calling a windows API function. Wek's main function, `wek()`, consists of just three lines of code.
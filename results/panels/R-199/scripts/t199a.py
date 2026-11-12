import sys
sys.path[:0]=["scripts/records"]
import build_r199 as b
for l in ["so Omar (my neighbour) keeps tortoises in the yard","Ivan is my brother and just got a kitten called Mochi",
 "so Ivan (my brother) finally switched to a Pixel","Ivan is my brother, and they rent on the seventh floor",
 "so Ivan (my brother) finally switched to a Pixel.", "So Ivan (my brother) finally switched to a Pixel"]:
    print(repr(l),"->",repr(b.reworded(l)))
for s,w in b.WORDINGS.items():
    if "kitten" in s or "yard" in s: print(s, w)

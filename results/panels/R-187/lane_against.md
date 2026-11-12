# R-187 against lane (claude-opus-5-5; read the draft, R-185, R-186, the R-185 lanes, build_r187.py, build_r185.py, check_r185.py and named functions of build_r178.py; edited nothing, ran nothing)

(1) The code mostly does what the draft says: `K1.builder_item` is replaced at module level and `main`'s `f2_item`
looks it up at call time; with share None (source finding, found_before) the moved-row path is skipped; the cache is
filled once per row; the counted search and the final row's search use the same query (6.37's `source.query`).
Gaps: R-102 rows do not go through `builder_item`, so a moved R-102 row would silently keep same_type (stop with an
error instead, and say so in advance); `f2_item` still returns K2's share, so the `never_told_share_*` tally counts
picked shared_word rows as same_type; a moved row with an empty search is replaced by `fresh_never_told` in
same_type, not its picked share; `picked` goes only to stdout (put it in the provenance file); picks are measured on
the F2 conversation, and moved rows that later get F3 end up as a different conversation (a small mismatch). Not
verified: whether extra searches against the scratch index change later searches.

(2) Not gaming in the sense of the shortcut: each moved row is matched to its own K1 count, so passage count does not
start to predict a decline. But the rule selects on the number line 4 measures, so line 4 is close to a pass by
construction and no longer an independent check. The record must say this.

(3) shared_word rows could bring back "passage names the asked person, target declines" if the shared word is a
person or relation. Line 1 catches that; K2 has 27 against 24 to 30, so 3 rows of headroom. A failure there is the
more likely risk.

(4) The draft omits (2), the F3 mismatch, the hard stop for unbuilt moved rows, the tally and replacement-share
defects, and that K2.1 was designed using the failed line's own statistic.

Verdict: ready with changes: stop the build if any moved row skips `builder_item`; write `picked` into the provenance
and fix the share tally; give `fresh_never_told` the picked share; disclose that line 4 is near-automatic; disclose
that F3 rows are counted on the F2 version.

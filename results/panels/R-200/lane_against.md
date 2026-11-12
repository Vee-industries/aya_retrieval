# R-200 (K1.3) build: the case against

Lane: against. Read build_r200.py, build_r199.py, check_r199.py. Probes ran only on K1's rows
(data/screens/k1_r178.jsonl). build_r200.main() was not run, and no K1.3 set or K1.3 statistics were made.

Verdict: GO WITH CHANGES. Line 1 and one-wording-per-row hold. Line 5 is not covered by the quota and is
likely to FAIL by chance.

## Findings

1. Line 5 is likely to fail by chance (check_r199.py:192-197, 220-227; build_r200.py:112-115). The quota
   gets each role's 25% right but leaves the all-template share inside each count of lines to chance.
   K1's row counts: found rows with 1/2/3/4 asked-type lines = 185/179/169/29; never_told = 51/43/50.
   With p = 0.25 per line, the expected standard error of the found minus never_told difference is about
   6.9 points at n=1 (P(|diff| > 5) about 47%), 4.1 points at n=2 (about 22%) and 2.0 points at n=3
   (about 1%). The chance of passing all three is about 41%. A 25% template share has more spread than
   K1.2's draw, so K1.2 passing line 5 says nothing here.
   Fix: stratify the quota by (role, number of asked-type lines in the row) for search rows. That makes
   n=1 exact, because each n=1 row has one line and so its all-template status is its line's status. For
   n>=2, choose the all-template rows per (side, n) directly at a fixed share, then fill each role's
   remaining quota from the other rows. Or decide in advance and record that line 5 at n>=2 is left to
   chance.

2. Returned lines of other fact types are left to chance (build_r200.py:111, role "other"). Lines in a
   search output that are not of the asked type go into the same "other" pool as facts that appear only
   in the chat. K1 has 252 such lines in found outputs and 79 in never_told outputs. Their template
   share by side is left to chance: the expected standard error of the difference is about 5.6 points.
   No check line looks at these lines, so a gap between found and never_told outputs could go
   unnoticed. Fix: give them their own roles ("found_other_type" and "never_told_other_type"), or at
   least report the share for each side.

3. Correction to a docstring claim (build_r200.py:13-14). "K1.2's code unchanged" is not exact, and
   neither change is a bug:
   (a) a fact kept in the template wording is now left byte-for-byte as K1 had it, where K1.2 rebuilt
       it from groupdict;
   (b) the draw excludes the template (WORDINGS[statement], not (statement, *WORDINGS));
   (c) the seed is (row, fact), not the fact's span, so the same fact takes different wordings in
       different rows. K1.2's docstring promised "one wording wherever it appears" (build_r199.py:7-8).
       That promise now holds only within a row.
   Reword the docstring.

4. No bug found for question (1). Probes on K1:
   - every role key from roles() is found by fact() in the row, and no asked-type line has a fact key
     that differs from its role key (0 of 1,453);
   - for every fact text in K1 and every wording in WORDINGS[statement], check_r199.mapped() gives back
     K1's text byte for byte, and check_r199.match() returns kind "more" with the same template and the
     same groups (0 failures);
   - every statement has a non-empty WORDINGS entry, so the bare [] at build_r200.py:125 raises no
     KeyError;
   - 0 rows have a fact key under two patterns, 0 texts state more than one fact, and tool_output()
     agrees with startswith("Tool result for") on every turn;
   - asked_other occurs only on the found side (110), so pooling it across sides does no harm.

5. No new cue found between answers and decoys (check line 4). Each of answer, found_decoy and
   never_told_decoy is exactly 25% template, up to rounding of half an occurrence. There are no duplicate
   output lines, so (row, fact) occurrences equal the lines that line 4 counts. The same hash both orders
   the quota and seeds the wording choice. Random(seed) makes that harmless, but a separate salt would be
   cleaner.

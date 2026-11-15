# Lane 2: Statistician and experimental designer (hostile)
Verdict: submit after fixes

Commit 48c6586. Scripts: `...\scratchpad\panel4\l02\recheck_s3.py` and `extra_s3.py`. Both are read-only and read `results/s3/` only. Every S3 count, interval and Appendix C split reproduces, and so do fourteen printed sign-test p values.

## Round-2 findings: status
F1 fixed: HF 15 and ARTICLE 88 now carry the scope.
F2 partly: the papers give C1 seed 82's 50 of 60; ABSTRACT 27 still says only "labelled".
F3 fixed. F4 fixed. F6 fixed.
F5 not fixed (optional): K1 minus C1 on (c), -5.9 [-9.7, -2.5], is still not printed.
Round-1 F6 not fixed: HF 26-27 and ARTICLE 126 still say "a sealed test opened once (the first sealed test and S3)".
Round-1 F8 not fixed: ARTICLE 316-320 and 340 still do not say that rule 1's pooled sign test counts each base row eight times.
Round-1 F9 not fixed: ARTICLE 579-581 and Appendix C's coherence line do not say the sheet held C1 seed 82 only (R-281). The other (a) lines pool three seeds.

## New findings (most severe first)
F1. [MAJOR] HF_ARTICLE.md:9-10, "code that searches every turn recalls as much or more": on set 2, code has 47 against 6.37's 53 (p = 0.45). A result with no measured difference does not show "as much".
    Evidence: ARTICLE 6.2 tables.
    Fix: "shows no measured difference on the two outside sets and recalls more on S3".
F2. [MAJOR] ARTICLE.md:410-411, README.md:286-288, MODEL_CARD.md:121-122: "gaps under about 15 points on a kind of 40 are below what this test resolves" uses the wrong quantity. 15.5 is the half-width of one rate (`make_article.py:374-376`). For a difference between two arms it is about 22 points, and the power to detect a gap is lower still. README 288 then turns this into "no measured loss against base".
    Fix: "about 20 points" for the difference, or "not powered to show equality".
F3. [MAJOR] ARTICLE.md:418, "base / 6.37: 37 against 38, 35 against 39": the order is reversed. In `R-146/blind.json` and `R-157/blind2.json`, `statement` reads seed 82: 37, base 38 and seed 82: 35, base 39 (`make_article.py:1418-1419` fills seed 82 first). This was already wrong in 83576b9.
    Fix: change the label in `article_template.md:387` to "6.37 / base".
F4. [MINOR] ARTICLE.md:432-435: two different 233s sit in adjacent sentences (answerable questions among the judged 248, and declines out of 470).
    Fix: "the 233 answerable questions of the judged 248".
F5. [MINOR] ARTICLE.md:61, headline table: the S3 recall row puts C1 in the "Trained" column, and the shipped 6.37 (347 of 1,242, 27.9%) is missing.
    Fix: add the 6.37 count to that cell.

## What holds up
Every S3 line reproduces from `results/s3/`. No multiplicity adjustment is needed for a rule that requires every line to hold.
Appendix A's per-seed recall sums to section 6.1's pooled counts in all four conditions (835, 843, 863 and 858 of 960). The largest p, 3.2e-4, matches `R-168/refs.json`.
The outside-set wrong-answer stages add up (81 and 67), and so do the LongMemEval split counts.

Not checked: the LongMemEval-S files (closed to this panel) and the figure intervals.

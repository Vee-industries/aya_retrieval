# Panel R-102: the messy arm's replacement rule, now that the battery has fired

Read RECORDS.md R-099 first (repo `C:/Users/Gaming/Desktop/hackathons/Lexsi Sprint/aya_retrieval`, read-only). R-099
registered: measure v6 first; a messy form is a gap if, paired over seeds 82 and 83 on one pool, it costs at least 8
of 192 recall answers, or at least 4 of 96 on `statement`, `never_told` or `in_view`; if a gap, one messy arm of
about 150 appended rows built by `stress.py`'s transforms, only for the forms that showed a gap; the held-out
`phone_style` form is never trained on and is the arm's primary measure; item 6: the arm replaces the shipping model
only if it passes every existing gate at 82, 83 and 91 to 93 and gains on the phone form by at least 8 of 192 (probe)
or 16 of 192 (`hard_dev`). Cutoffs: arm not started by Sun Nov 8 12:00 = dropped; nothing starts after Mon Nov 9 12:00.

The shipping model is v6 (17m seed 82); the slip-fix track ended (R-101).

## Battery result (v6, seeds 82 + 83 pooled, messy minus plain, same adapter and items)

| Form | probe recall /192 | probe in_view, never_told, statement /96 | hd recall /192 | hd in_view, never_told, statement /96 |
|---|---|---|---|---|
| lower-case typing (`user_style`) | -3 | -1, +2, -1 | -2 | -3, -1, -1 |
| phone typing (`phone_style`, held out) | **-14** | 0, +2, **-6** | **-25** | -3, +1, -1 |
| fact corrected later (`corrected`) | **-187** | (recall only) | **-146** | (recall only) |
| earlier question in view (`asked_before`) | -2 | -1, +2, -3 | -7 | **-4**, 0, 0 |

Gaps by the registered rule: corrections (both pools), phone (both pools), asked-before (`hard_dev` `in_view`, -4,
exactly on the line). Not a gap: lower-case typing.

Corrections, checked by reading replies: the search returns both the original and the correcting passage, and v6
answers the old value ("Your daughter Gustav got a koi tattoo." when the correction said lighthouse). Base on
corrections and on phone typing is being scored now; not in yet.

## The problem

Under item 4 the arm trains on corrections (and perhaps asked-before) rows. Phone typing cannot be trained on. Item
6 lets the arm replace v6 only by gaining on the phone form, which correction rows are not designed to move. So the
registered rule tests the arm on something it does not target, and the largest gap found (corrections) has no
measure that could let a fix ship.

## Options (others welcome)

- **A. Keep R-099 as written.** The arm runs; it can replace v6 only with a phone-form gain; otherwise it is a
  development finding in the write-up.
- **B. Change item 6 before the arm is built or run** (Kevin's decision, disclosed as a change made after the battery
  but before any arm result): add a held-out correction form, written and hashed now, never trained on (for example
  correction openings and wordings `corrected` never uses, or the correction in a different position), as the
  arm's primary measure, with the phone form as a guard (not below v6). Existing gates unchanged.
- **C. Drop the arm**; the battery goes in the write-up as a measured weakness.

## Hard constraints

Never open `src/aya_retrieval/pool_independent.py`, anything under `docs/independent_pool/`, or lines 452 onward of
`src/aya_retrieval/pools.py`. Run no code; write nothing outside your reply. The standard (RECORDS.md, and the rule
that rules are not loosened after results; any change is the researcher's, made before the results it decides).

## Questions

1. A, B, C or another? Why, given the standard on changing registered rules?
2. If B: what is the held-out correction form, what gain counts (pool, size, given R-091's seed spread), and what
   guards stay?
3. Should the arm include asked-before rows (a gap by exactly the line) or corrections only?
4. Does it fit the clock (arm build and seeds 82, 83, then 91 to 93 before Monday 12:00; each seed about 55 minutes)?

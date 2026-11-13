# K4 design: against lane (short read)

Date 2026-11-12. Read-only: no repo edits, no git, no GPU. Read: RECORDS.md R-206 to R-208, `docs/k4/WRITER_BRIEF.md`,
`scripts/records/build_k3.py` (`chat_rows`, `balance`) and the 64 K3 writer chats. Scripts and outputs are in
`C:/Users/Gaming/scratch/claude/C--Users-Gaming--claude-spares-spare-wcSF8M/3f7d989b-d009-44ac-9f86-64e88058f022/scratchpad/r208_lane/`
(`sim.py`, `older_me.py`, each with a `.out`).

**Verdict: ready with listed changes.** None of the findings breaks the build. Finding 1 changes what Demo2 can show
about K4 and has to go into the record before K4's Demo2 run. Findings 2 to 4 are build or check changes that can be
made while the writers write.

## 1. The brief's examples are Demo2's own misses, so Demo2 stops being a blind check for K4

- The brief names five "close pairs". The first two, "what someone teaches against what they study" and "where
  someone is moving against where they will work", are exactly K3.2's two Demo2 misses (R-208: "studying geology" for
  a person who teaches it; Ollie's move for where Ollie will work).
- The third, "a pet's name against its breed", is Demo2's Q3.
- Writers copy the brief's examples. K4's Demo2 bomb rule (never-told at least 3 of 4) will then be scored on
  questions of the very kind the training rows name. A pass there would not show the near-miss skill generalizes.
- S3 has a never-told kind that shares a word with another fact of the same person, and Demo2's brief mirrored it
  (R-201). R-208 does not disclose that K4 is aimed at that kind.
- What to change:
  - Record now, before Demo2 runs on K4: the brief's examples are Demo2's misses, so K4's Demo2 never-told result is
    not blind and counts only as a regression check.
  - Report K4's near-miss rows by pair type. Read Demo2 alongside the count of training rows that use the teach/study
    and move/work pairs.
  - Disclose the S3 item type.
  - The writers have the brief already, so it cannot change for this build. Any later near-miss writing should use
    examples outside Demo2.

## 2. Near-miss outputs will often not hold the asked person's stored fact, and the line that would show this is only reported

- 727 facts in messages 1 to 21 of the 64 chats: **369 (51%) are about the user** and 358 about named people. The
  brief allows "a person (or the user, 'me')".
- Named people:
  - The person's reference appears in its own fact line in 323 of 358.
  - A query of that reference alone returns the stored fact in the top 5 in **328 of 358 (92%)**.
  - A named near miss whose question names the person will usually hold the stored fact, as wanted.
- The user: a near-miss query has no person word, and the brief forbids reusing the fact message's words. So the
  stored fact can come back only through Y words, or a second query, that happen to match X's message. In K3's own
  older questions about the user, 95 of the 106 found were found only by the writer's second query.
- A user near miss whose output lacks the stored X fact is a plain never_told row. It does nothing for the Demo2
  failure, and the line "near_miss rows whose output holds the asked person's stored fact" only reports this.
- What to change:
  - Make that a keep rule: a near_miss row is kept only when its output holds the asked person's stored X message,
    using the annotations' `fact.person` and `stored_category`. Report how many are dropped by person ("me" against
    named).
  - Add a validity check the annotations allow: no fact in messages 1 to 24 has the asked person together with the
    asked category Y (a writer mistake would be a false "not told" label), and the stored X fact exists for that
    person.

## 3. Two near misses to one contrast, with the balance run over the new rows alone, push toward declining a returned fact

- Per chat, the design writes 2 near_miss (decline) to 1 contrast (value). Contrast rows built as older rows that are
  not found also decline. In K3's own older rows, 34 of 140 about the user and 6 of 116 about others declined. So the
  new rows will be about 2 to 3 declines per value row.
- The balance keeps that ratio at each passage count, because it is computed over the new rows alone.
- So, in the new rows, "the output holds the asked person's fact under close-category words" means decline about two
  times in three.
- K3.2 already declined two facts its search had found on Demo2 (R-208). Found and declined was K1's main loss
  (R-203: hard_dev 63; outside writers 29 and 22).
- Near miss and contrast differ only in the category word. If writers use each close pair in one direction (for
  example "teaches" always as the never-said Y), that word alone predicts the label.
- What to change:
  - Make value and decline rows equal within the rows whose output holds the asked person's stored fact. For example,
    one near miss and one contrast per person and fact, or a cut to 1 to 1 by hashed order, registered before the
    build.
  - Report, per category word, the share of rows that decline, so a one-way pair shows up.

## 4. Line 6 as changed holds by construction

- K3.2's natural rows already have check_false 79 against check_true 56. K4 adds no check rows, so "check_false at
  least as many as check_true" cannot fail.
- The user third counts natural fact rows. The new contrast rows can move it only a little.
- Fine as a guard, but say it checks nothing about the new rows. The real checks for K4 are the lines in findings 2
  and 3.

## Smaller

- Second queries are written by a writer who has read the source. That is why 95 user-fact rows were found. At test,
  the model writes its second query without seeing the source. This is a K3 property that K4 extends to contrast rows;
  disclose it.
- Each chat's view (messages 22 to 24) now repeats in about 14 rows, over 64 views.
- R-208's prediction (about 150 rows) has no breakdown by kind or by person. Add one.

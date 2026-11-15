# R-294 synthesis: does Kevin's aggregate ruling put C1 forward over 6.37?

Asked by Kevin in chat, 15 November 2026 ("yeah panel it"); his position: "i think that my call about aggregate winning
still holds and i made that call before seeing these results and we can run 6.37 on the other demos for the full
comparison". Three lanes, at most two in flight: method (Sonnet), against (Opus, told to build the strongest case for
Kevin's position because the orchestrator leaned toward keeping 6.37), sources (Sonnet). Brief: `brief.md`. Every lane is
the same model family as the orchestrator, so their agreement is not independent confirmation (STANDARD rule 22).

## Recommendation (binding unless Kevin overrides it)

Put forward 6.37 seed 82, the shipped model, by the registered ship rule. All three lanes reach this, the against lane
included.

## Answers

1. R-278 (commit 10:54, 14 November) read R-276's demo test as the totals over Demo4 and Demo5 for C1 against K1.3. It
   decided which candidate went into S3. It names neither 6.37 nor the ship rule. The ship rule (R-178 item 5, changed
   by R-191 before S3 opened, computed by R-281) decides what ships: all of (a), (b) and (c), else "6.37 seed 82 stays
   shipped". R-280, written after R-278 at Kevin's "Yes, run S3", restates that rule with no demo term.
2. The aggregate call came before S3's first result (14:29) and verdict (18:49), and after both models' demo readings
   (disclosed in R-278). Putting C1 forward now would read a new scope into it after the sealed result: a change to
   clause (c) after the result it decides, which STANDARD rule 2 does not allow ("Rules are not loosened after
   results; any change of rule is the researcher's, made before the results it would decide"; "A miss by one judged
   line is a miss"). The against lane tried three readings that would put C1 forward without a change ("not
   significantly above base", seed 82 alone, an aggregate over S3's lines); each fails as written (R-281 fixed the
   point-rate reading at 14:16, before any S3 file; R-178 and R-281 pool seeds 82, 83 and 94; R-178 requires all of
   (a), (b) and (c)).
3. Running 6.37 on Demo4 and Demo5 is valid as a measurement (neither demo is sealed) and can decide nothing: the ship
   rule has no demo term; 6.37 was never a pick candidate. If run, it is registered first as a report row that decides
   nothing, labelled exploratory, n = 6 older and 4 never-told a demo, with Demo5 already read twice (R-277).
4. Both papers state: the ship rule and its dates; C1's pass of (a), (b) and two parts of (c) and its miss, 51 of 708
   (7.2%) against 14 of 236 (5.9%), +1.3 points, chat-resampled 95% interval -3.1 to +5.7, per seed 11, 29 and 11 of
   236, a miss under the rule as written and not a measured difference; base's rate is a floor (the flag misses
   invented values, R-295); C1 against 6.37 in counts (copies 5 against 195 of 894; N-hit 51 against 286 of 708;
   plain never-told 344 against 238 of 360; recall 364 against 347 of 1,242, +1.4 points, -3.1 to +5.9); 6.37's own
   fault rates above base's; R-276 and R-278 set after the demo readings and deciding only the pick; K1 and K2.1 as
   report arms with no ship claim; and Kevin's view that the aggregate should win, stated as his view and not applied.

## The strongest objection, carried

Shipping 6.37 ships the model with the worse fault rates (40.4% N-hit against C1's 7.2%) over a 1.3-point gap S3
cannot resolve; on substance C1 is the better model for users. Answered, not dismissed: R-178 chose this outcome before
S3 ("S3's numbers on 6.37 go in as its measured weakness"); rule 8 lets both papers give C1's advantage in full without
a ship claim; loosening the rule after the result would take the meaning out of every earlier sealed verdict in the
record. If Kevin overrides, the papers must call it a rule change after the sealed result (a deviation row, rule 26) and
must not say C1 passed S3.

## Checked by the orchestrator

R-277 commit 10:48:29 and R-278 commit 10:54:10 (`git log`); R-281's scorer commits at 14:16 and 14:20 before the first
S3 result at 14:29 (lane 2 of R-295, and R-282); the interval -3.1 to +5.7 and the per-seed counts, rerun from lane 2's
script on the committed S3 files.

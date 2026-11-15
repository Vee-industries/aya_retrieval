# Panel: does Kevin's aggregate ruling put C1 forward over 6.37?

You are one lane of a three-lane panel. Kevin Vaillancourt, the researcher, asked for it in chat ("yeah panel it"); its
recommendation binds unless he overrides it. Plain words; no metaphors. Read only; never edit anything in the
repository.

## Kevin's position, in his words (chat, 15 November 2026)

"i think that my call about aggregate winning still holds and i made that call before seeing these results and we can
run 6.37 on the other demos for the full comparison"

## Facts (each checkable in the record)

Repository: `C:\Users\Gaming\Desktop\hackathons\Lexsi Sprint\aya_retrieval`. `RECORDS.md` is 815 KB: find an entry with
`grep -n "^## R-NNN " RECORDS.md` and print only its lines with `sed -n`. Read at least R-178, R-191, R-276, R-277,
R-278, R-279, R-280, R-281 and R-287. Git times: `git log --format="%h %ci %s" | grep R-27` and the like.

- 6.37 (seed 82) was submitted on 10 November and is the shipped model.
- R-178 (12 November) registered S3, a sealed test, and the ship rule: the pick replaces 6.37 only if it passes (a),
  (b) and (c); otherwise 6.37 stays shipped. R-191 (12 November, before S3 opened) changed (a)'s standard from 6.37 to
  base. R-281 fixed how each line is computed, before any S3 file was read.
- R-276 (14 Nov, 10:40): Kevin ruled a candidate must beat K1.3 on the demos. R-277 (10:48): under it C1 failed (Demo5
  older 2 against K1.3's 3); K1.3 stayed the pick. R-278 (10:54): Kevin, on seeing those readings: "hmm it has a higher
  point spread"; asked whether to judge by the totals over Demo4 and Demo5: "yes". C1 then led on both totals (older 5
  of 12 against 4; never-told 6 of 8 against 5), trained more seeds and became the pick (R-279, pick recall 775 against
  742).
- R-280 (14:12): Kevin: "Yes, run S3" on C1. R-287 (18:49): S3 result. C1 passes (a) and (b) and two parts of (c); it
  fails (c)'s "not above base's": N-hit false answers 51 of 708 (7.2%) against base's 14 of 236 (5.9%). By R-178, 6.37
  stays shipped.
- On S3, against 6.37 (three seeds pooled each): copies of a wrong answer in view 195 to 5 of 894; N-hit false answers
  286 to 51 of 708; plain never-told declines 238 to 344 of 360; recall 347 to 364 of 1,242 (C1 minus 6.37 +1.4
  points, chat-resampled 95% interval -3.1 to +5.9); in view 161 to 160 of 180; statement 180 to 166 of 180. 6.37 is
  worse than base on the fault measures (copies 21.8% against 3.7%; N-hit 40.4% against 5.9%).
- A review panel today found: S3 cannot tell C1 from base on the failed clause (C1 minus base +1.3 points, 95% interval
  -3.1 to +5.7); per seed, C1's N-hit is 11, 29 and 11 of 236 (only seed 83 above base); the never-told and N-hit
  scorers miss invented values, and base invents many, so base's 5.9% is a floor; report arms K1 and K2.1 (two seeds,
  no coherence) meet every measured S3 line.
- 6.37 was never run on Demo4 or Demo5. Demo5 has been read twice (C1, K1.3) and partly seen by the orchestrator
  through a judge's marks (R-277). Each demo has 6 older and 4 never-told keyed questions.
- Kevin's standard: `C:\Users\Gaming\Desktop\Claude's House\STANDARD.md`, rules 2 (goalposts before the data; "Rules
  are not loosened after results; any change of rule is the researcher's, made before the results it would decide"),
  8 and 13. The form is due 16 November 06:59 ET.

## The questions

1. What did R-278 decide, and what did the ship rule (R-178, R-191, R-281) decide? Does R-278 govern which model is put
   forward, or only which candidate went into S3?
2. Was Kevin's aggregate call made before the results it would now decide? If Kevin now rules that C1 is put forward
   over 6.37, is that a rule change after the sealed result under rule 2? Is there any reading of the registered
   rules, as written before S3 opened, under which C1 is put forward without a change?
3. Is running 6.37 on Demo4 and Demo5 now valid, and what could its result decide?
4. Your recommendation: which model is put forward in the submission, and exactly what both papers must say about it.

## Your report

Write it to the file named in your lane message, at most about 700 words:

```
# Lane: <name>
Recommendation: <one line>
## Answers to questions 1 to 4 (each with the record ids or rule text it rests on)
## The strongest point against your recommendation, and why it does not change it (or does)
```

Your final message is only the report's path and its recommendation line.

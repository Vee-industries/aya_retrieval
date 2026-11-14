Recommendation: run A then B changed: run A first, because B is A plus rows and so A is B's only control; run B only if A clears hard_dev, check that every answer row's value is in the real search output, and record any Demo5 pass from here on as a second read.

# Against lane: C2 and OPT, 2026-11-14

Sources: the brief's counts and the OP4 lane's page. "Estimate" marks arithmetic on those counts.

## 1. A: lever or draw?

- Demo4 older: K1.3 1, C0 2, OP 2, C1 3. Each change is one question of 6, on one seed. Demo4 cannot tell a lever from a draw.
- hard_dev is the better signal. The repeat (OP to C1) raised recall 60 to 68 of 96: not-found fell 9 to 5 and reading errors fell 27 to 23. So the repeat helped search and reading about equally. It was not a reading fix.
- Cost: never_told fell 48 to 46. The line is 44, so 2 items are left. If C2 loses the same 2 (estimate), it lands on the line. Both demos are at 3 of 4 never-told, also on the line, so one more false answer fails gate 2 or 3.
- A simpler explanation for the recall gains: hard_dev uses the training template family (the brief says so for B), so extra epochs may only fit template wording. The part that reaches the natural demos is one item per step, which is a draw at n = 6.
- Verdict: A is a lever on hard_dev. On the demos it is unknown. Each epoch so far has moved the model toward answering and away from declining.

## 2. Is B different from OP in a way that matters?

- B starts from C1 and runs the same stage on OP's set, plus new rows. So B contains all of A. A B result with no A beside it cannot give credit to the rows.
- B aims at reading errors, the same class OP's 18 answer rows aimed at. Reading errors went 32 to 27 with OP's rows and 27 to 23 with no new rows. A plain epoch removed nearly as many (4) as OP's rows did (5). B's rows have to beat a plain epoch, and only A measures that.
- Dose (estimate): if C1 misreads the training draw at hard_dev's rate (23 of 96), 240 items give about 23 answer rows and about 2 never-told corrections (46 of 48 right). Balanced, that is about 23 a side, near OP's 36. Training templates have been seen, so the real count is probably lower. Not checked.
- Row validity: a row that pairs "the template's correct reply" with "the real output" is only right if the value is in the output, in a passage about the right person. Otherwise the row teaches the model to state a value its search did not return, which is false retrieval. Check every answer row, drop the failures and count them. Not known whether `check_k3.py` tests for this. Not checked.
- Demo4's misreads (Q1, Q4) were declines with the source ranked second, behind a passage about someone else. Nothing says whether training templates produce that case. Count B's answer rows with the source not first, and those with another person's passage above it.
- Never-told risk: most of the decline side is declines the model already gets right. The new pressure is all on the answering side, and it comes on top of A's third epoch. B's risk is at least A's (estimate, direction only). If A fails never_told, B is expected to fail too.
- Replication: B needs its own on-policy draw and build for seeds 83 and 94. A adds only a stage. Not checked whether either fits by 20:00.

## 3. Route to Demo5's older line

C1 has 2 of 6 and needs one more. The misses are Q1 and Q3 (wrong, with the source in the output), Q2 (ran out of calls) and Q4 (not found). Neither option targets running out of calls or not-found. Either could flip one misread: B directly, but from the template family; A through general fit. One item on 6 cannot be told apart from a draw. C1 has read Demo5 once, and its misses are now in this panel's question. So the next read is the second, and the lever was chosen with the first read known. Each further try read on Demo5 raises the chance that one passes by draw. Not checked whether a fresh held-out demo exists. Demo4 is already at 4 reads.

## 4. Stop rules, controls, order

1. Order (estimate, GPU in series): C1 on the training draw (10 min, because B's rows come from C1), then A (45 min), then B (45 min). Write B's code on the CPU while A trains. That is about 100 GPU minutes, before 14:00.
2. A fails gate 1: no C3, no smaller retry, no B (B carries A's dose). K1.3 stays the pick.
3. A passes gate 1 but misses Demo4 (older under 3 or never-told under 3): C1's demo gain was a draw. Run B; A is its control.
4. A passes Demo4: read Demo5 and record it as read 2. Pass: seed 82 is done, seeds 83 and 94 take the C2 recipe, and B is not run today. Fail: run B.
5. B: count rows before training. Under 10 answer rows (the floor the OP4 lane used), do not train and report it.
6. Log on every gate: misreads, not-found and out-of-calls (as given for C1), never_told and false retrieval. For B, also log rows dropped and rows with the source not first.
7. Stop the day for seed 82 when A and B have both failed a gate, or when 14:00 passes. K1.3 stays the pick.

Prediction (estimate): A has hard_dev never_told 44 to 46 and recall about 70 to 74, Demo4 older 3, Demo5 older 2 or 3.

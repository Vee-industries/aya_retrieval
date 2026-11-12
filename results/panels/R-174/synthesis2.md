# Panel R-174 synthesis (orchestrator, 2026-11-12)
Lanes: lane2_method.md, lane2_against.md (both claude-opus-5-5).

Checked by the orchestrator: "sister broke skiing injury" and "brother new job" each occur in 3 rows of
data/screens/fix17cs37.jsonl. v5_82 and fix15_82 demo turns 12 and 14: both searched "brother new job" on BOTH
turns (so copied training queries predate 6.37; the against lane said only that they declined) and both replied
"I don't have that from you. What is it?". 6.37 answers with an unrelated stored fact instead. Base rerun = 2026-11-05
base.json on 15 of 15 turns.

Rulings:
1. Run order: the demo ran and was read before any registration. Not a minor slip (against lane). R-175 records it
   with the against lane's disclosure sentence, and that the publish-whole decision came after the run (the
   orchestrator told Kevin "it can't be cut" after reading it). No rerun of 6.37, no script change, no second demo set.
2. Demo block ships whole: all 15 turns, both models, built by a committed script from the committed JSONs; v5 and
   fix 15 rows for turns 12 and 14; the method lane's grading rule (fact as written in the script), so base's
   "a leaky faucet" is wrong too; the training-query finding with file and counts; the disclosures (script dated
   2026-11-04, before 6.37; visible in development; 3 pottery training rows; an illustration, not a measurement).
   The raw JSONs go in byte for byte as results/demo/fix17cs37_82.json and results/demo/base_r175.json.
3. New limit in every write-up: on the demo, 6.37 sent queries copied from its training set on two of four questions
   and answered with an unrelated fact; v5 and fix 15 declined on those turns.
4. Order: demo block, then CI (with the HF_TOKEN step; Kevin adds the secret himself; README states what CI covers),
   then notebook Part A; Part B only after a 3080 dry run with accelerate/safetensors pins, a CUDA check, a Python
   check, outputs outside results/demo/, and Kevin's Colab pass. Notebook is first to drop.
5. First CI run: on a branch, after telling Kevin a red run is visible in the public Actions tab.

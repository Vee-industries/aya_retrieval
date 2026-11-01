# The standard this project is built to

Set by Kevin Vaillancourt, October 2026, for research built with an AI assistant. It is meant to
apply to every such project, not just this one. Each rule says what it requires and how this
repository meets it.

## 1. Every result traces back

Every results file records the UTC time, the exact command, the git commit, whether the working
tree had uncommitted changes, the package versions, the seeds, and the model revisions used.
Work is committed after every step. Experiments run only from a committed, clean tree.

*Here:* `src/aya_retrieval/provenance.py` writes this record into every file under
`results/`. Models are pinned to exact Hugging Face commits and load only from the local cache.

## 2. The goalposts are set before the data exists

Hypotheses, measures, thresholds, sample sizes and the figure list are written down and
committed before the experiment runs. The commit timestamp is the proof. Anything changed
after seeing data is disclosed item by item, with the reason.

*Here:* the pre-registration is an entry in `RECORDS.md`, committed before the first run.

## 3. Controls gate every result

Every experiment runs a negative control (where the effect must not appear) and a positive
control (where it must). If either fails, the run's results are not reported. Every check is
first shown to reject a known-bad input; a check that cannot fail is not believed.

*Here:* every run stops before loading the model unless the search scorer accepts a real call
and rejects known-bad replies.

## 4. No hand-typed numbers

Every number and figure in the report is generated from the results files by a script. An
automated check fails if the report and the data disagree.

## 5. One command reproduces everything

A single script regenerates every result, table and figure, with the expected run time and
the hardware stated.

## 6. A complete, dated record

`RECORDS.md` logs every decision, run and result in order: what was done, when, with what
command, and what came out. Failures and reversals are recorded too. Entries are labelled by
phase (here PRE-SPRINT or SPRINT) so prior work is never confused with new work.

## 7. Who did what is stated plainly

The researcher makes the research decisions and writes the claims. The AI assistant's role
(implementation, checking, typesetting, or whatever it actually was) is stated plainly, and
decisions are attributed in the record.

## 8. Claims match the evidence exactly

Nothing is overstated, and nothing the data supports is softened. Each claim carries its
number, its uncertainty and its limits.

## 9. Scientific figures

Every figure is drawn by a script from results files and shows its uncertainty. Each caption
gives the sample size and seeds. Controls appear as reference bands. Colours are
colourblind-safe and consistent across figures. Output is vector PDF for print and PNG for
screens.

## 10. Code a stranger can trust

The code uses a standard package layout, with types, docstrings and a test suite. Each entry
point is a script that documents its own usage. Dependencies are declared, and there are no
hidden steps.

## 11. Open and within reach

Where the question allows, the work uses open-weight models on hardware an individual can own,
so anyone can rerun it without a budget or an API account.

*Here:* Tiny Aya runs unquantised on one 10 GB consumer GPU.

## 12. Show the work, not the clutter

The repository holds what a reader needs to follow and rerun the work, and nothing else. There
is one README, one record and one report; scratch work stays out.

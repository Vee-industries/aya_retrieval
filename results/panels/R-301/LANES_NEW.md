# The three new lanes of round 3

11. Graphic designer. Open every figure the papers show (`figures/*.png`; the short paper shows recall_out_of_view,
   demo_contamination and s3_faults; the long paper also whole_chat_or_search, never_told_slide, s3_recall,
   training_memory and s3_misses). For each: does it read at a glance at the size a reader sees it, are labels,
   legends, axis ranges and units clear and consistent across figures, is any text clipped or overlapping, are the
   colours consistent and safe for colour-blind readers, does the figure show its uncertainty, and does it earn its
   place? Name the smallest change to `scripts/make_figures.py` for each problem (function and line).

12. Layout judge. Judge the documents as a reader sees them rendered as Markdown on GitHub and Hugging Face: the order
   and depth of headings, section lengths, paragraph lengths, tables (width, too many columns, cells too long to
   read), lists, where figures sit relative to the text that cites them, links and pointers (does every "Appendix A",
   "section 9", "Figure 5" point at what it names), and the first screen of each document. Cover the short paper, the
   abstract, the long paper and the README's first 150 lines.

13. Cold reader. You know nothing about this project. Read only the short paper (`docs/submission/HF_ARTICLE.md`),
   then the abstract (`docs/submission/ABSTRACT.md`), as a technical reader with ten minutes. Do not read RECORDS.md,
   the panels, the brief's "Facts" or anything else first. Then answer, in your own words: what was built; what it is
   good at and bad at; which model is shipped and why; what you would use for your own chat assistant; and every
   sentence you had to read twice, every term you did not understand, every place you lost the thread. Only then may
   you open the long paper to check whether it answers your questions.

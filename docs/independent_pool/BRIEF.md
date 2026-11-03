# Brief: write an independent, hard test pool

You are writing test material for a research project, and nobody on the project will read it before
the final test. Write it yourself, from this brief alone.

## What it is for

A small language model chats with a friend. The chat is long (58 or 419 messages) and the model only
sees the last 3 exchanges. Everything earlier sits behind a search tool. The friend's newest message is
one of five kinds:
- **older**: asks about a fact the friend told long ago (out of view). The model must search, then answer.
- **confirm**: asks whether they ever told the model a fact ("did i ever mention ..."). Same as older.
- **in_view**: asks about a fact still in the last 3 exchanges. The model should answer without searching.
- **never_told**: asks about a fact of that type that was never said. The model should say it was not told.
- **statement**: ordinary chat with nothing to look up.

Each chat also holds **decoys**: the same type of fact about other people. The test checks whether the
model gives the right person's fact.

Your pool is the material these chats are built from. **Make it hard**, the way real people text:
- **Fact statements**: chatty, run-on, with the fact buried mid-sentence among other news. Vary the
  sentence shapes. The person and the relation can sit far apart in the sentence.
- **Questions**: real texting style. Lower case, little or no punctuation, contractions, filler words.
  Ask sideways rather than directly.
  - `new_words` must not use the fact type's obvious keyword (for a tattoo, not "tattoo").
  - `indirect` is a statement about forgetting, with no question mark, and must not use the idioms
    "drawing a blank", "blanking", "tip of my tongue" or "cannot think".
  - `confirm` asks whether the friend ever told it.
- **Values**: plausible and close to each other within a type, so they are easy to mix up, but no value
  may contain another as a substring ("rose" and "rosemary" are not allowed).
- **Small talk**: everyday and varied. Subjects may sit near the fact topics, but no fact value may
  ever appear in small talk.

## Exact format

Write one Python file at:
`C:\Users\Gaming\scratch\claude\C--Users-Gaming-Desktop-Claude-s-House\389594c2-8513-47d9-80f1-1a28b96837f7\scratchpad\indie\pool_independent.py`

It must contain:

```python
from aya_retrieval.pools import FactTemplate, Pool, SmallTalkMood

INDEPENDENT = Pool(
    people=(...),            # at least 10 first names, one capitalised word each
    relations=(...),         # at least 8 relation words, lower case, e.g. "landlady" (choose your own)
    facts={                  # at least 6 fact types, each keyed by a short name
        "<type>": FactTemplate(
            values=(...),                 # at least 6 values for this type
            statement="...",              # uses exactly {person} {relation} {value}
            same_words="...",             # a direct question naming the person: exactly {person}
            new_words="...",              # asks by relation, different words: exactly {relation}
            indirect="...",               # a statement about forgetting: exactly {relation}
            confirm="...",                # "did i ever tell you..." style: exactly {relation}
            query="...",                  # search words a good search would use: exactly {who}
            answer="...",                 # a plain answer sentence: {person} and {value} (and {relation} if you like)
        ),
        ...
    },
    subjects=(...),          # at least 32 small-talk subjects, e.g. "the bus stop"
    moods=(                  # at least 3 moods
        SmallTalkMood(
            user_lines=(...),   # at least 5, each uses exactly {subject}
            replies=(...),      # at least 5, may use {subject}
        ),
        ...
    ),
    acknowledgements=(...),  # at least 6 short replies to a friend's news, no placeholders
    statements=(...),        # at least 6 pairs (line, reply): line uses {person} and/or {relation},
                             # reply has no placeholders; ordinary chat, nothing to look up
    unknown_replies=(...),   # at least 3 ways to say "you haven't told me that", no placeholders
)
```

## Avoid

`avoid.json` in the same folder lists names, relations, values and subjects that other pools already
use. Do not use any of them, in any capitalisation.

## Check it

Run, from `C:\Users\Gaming\Desktop\hackathons\Lexsi Sprint\aya_retrieval`:

```
"C:/Users/Gaming/Desktop/hackathons/Lexsi Sprint/venv/Scripts/python.exe" "C:/Users/Gaming/scratch/claude/C--Users-Gaming-Desktop-Claude-s-House/389594c2-8513-47d9-80f1-1a28b96837f7/scratchpad/indie/check_pool.py" "C:/Users/Gaming/scratch/claude/C--Users-Gaming-Desktop-Claude-s-House/389594c2-8513-47d9-80f1-1a28b96837f7/scratchpad/indie/pool_independent.py" "C:/Users/Gaming/scratch/claude/C--Users-Gaming-Desktop-Claude-s-House/389594c2-8513-47d9-80f1-1a28b96837f7/scratchpad/indie/avoid.json"
```

Fix and re-run until it prints `PASS`.

## Rules

- Read only this brief, `avoid.json` and `check_pool.py`. Do not open any other file in the project
  or the scratch folder, and do not search the project. The point is that your writing is independent.
- In your final reply, do **not** quote or describe any of your pool's content (no names, relations,
  fact types, values or phrasings). Report only: that the checker printed PASS, and how many people,
  relations, fact types, values per type and subjects you wrote.

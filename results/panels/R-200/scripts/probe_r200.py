import importlib.util, json, re, sys
from collections import Counter
from pathlib import Path
here = Path("scripts/records")
spec = importlib.util.spec_from_file_location("build_r200", here / "build_r200.py")
m = importlib.util.module_from_spec(spec); sys.modules["build_r200"] = m; spec.loader.exec_module(m)
K12, CHECK = m.K12, m.CHECK
rows = [json.loads(l) for l in Path("data/screens/k1_r178.jsonl").read_text(encoding="utf-8").splitlines()]
# 1 statements without WORDINGS / template inside WORDINGS
for p, s in K12.PATTERNS:
    w = K12.WORDINGS.get(s)
    if not w: print("NO WORDINGS", s)
    elif s in w: print("TEMPLATE IN WORDINGS", s)
# 2 role keys vs fact keys
missing = Counter(); roleset = Counter(); outfacts_other = 0; multi = 0
for row in rows:
    ro = m.roles(row)
    keys_seen = {}
    for t in row["turns"]:
        for text, rep in m.texts(t):
            g = m.fact(text)
            if g:
                keys_seen.setdefault(g[0], set()).add(g[1].re.pattern)
    for k, r in ro.items():
        roleset[r] += 1
        if k not in keys_seen: missing[r] += 1
    if row["kind"] in m.NEEDS_SEARCH:
        q, out, rep = CHECK.search_turns(row)
        for line in re.findall(r"^User: (.*)$", out, re.M):
            c = CHECK.match(line); f = m.fact(line)
            if c and q.endswith(CHECK.QUERIES[c[1]]):
                if not f or f[0] != c[2].group(0).casefold(): outfacts_other += 1
            # two output lines of the same key in one row with different roles?
    # same key in two lines in one output
print("roles", dict(roleset), "role keys not found by fact()", dict(missing), "asked-type lines whose fact key != role key", outfacts_other)
# 3 every wording maps back for every K1 fact text
bad = Counter(); ex = []
for row in rows:
    for t in row["turns"]:
        for text, rep in m.texts(t):
            g = m.fact(text)
            if not g: continue
            key, found = g
            st = next(s for p, s in K12.PATTERNS if p.pattern == found.re.pattern)
            orig_map = CHECK.mapped(text, rep)
            if orig_map != text:
                bad["template text not fixed by mapped"] += 1
                if len(ex) < 4: ex.append(("tmpl", text, orig_map))
            c0 = CHECK.match(text)
            for w in K12.WORDINGS.get(st, ()):
                new = w.format(**found.groupdict())
                if rep and found.start() == 0 and found.group(0)[0].isupper(): new = new[0].upper() + new[1:]
                nt = text[:found.start()] + new + text[found.end():]
                if CHECK.mapped(nt, rep) != text:
                    bad["drawn not mapped back"] += 1
                    if len(ex) < 8: ex.append(("drawn", text, nt, CHECK.mapped(nt, rep)))
                c1 = CHECK.match(nt)
                if not c1 or c1[0] != "more" or c1[1] != c0[1] or c1[2].groupdict() != c0[2].groupdict():
                    bad["drawn match differs"] += 1
                    if len(ex) < 8: ex.append(("match", nt, c1 and c1[:2]))
print(dict(bad)); [print(e) for e in ex]

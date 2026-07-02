# Skill Finder — Worked Examples

End-to-end walk-throughs of the layered model in `SKILL.md`
(**Catalog → skills.sh → Web Search → ClawHub → SkillsMP**, early-stop at the first
good match; **Layers 1–2 fire in parallel** — see SKILL.md ⚡ note). All examples resolve
paths **once** per SKILL.md "Paths" (anchored on this skill's base directory):

```bash
SF="<this skill's load-time base directory>"   # ends in …/skills/skill-finder
INSTALL="$SF/scripts/install-skill-from-github.py"
CACHE="${SF%/agents/*}/skills/remote_skills_cache.json"
# See SKILL.md "Paths" for the rule (never glob across agents/*) + the fallback.
```

---

## Example 1 — Layer 1 catalog hit (fastest path)

**User:** "有没有能帮我做关税查询的 skill？"

Fuzzy need → resolve via the catalog cache first.

```bash
cat "$CACHE" | python3 -c '
import json, sys
q = "tariff hs code 关税".lower().split()
data = json.load(sys.stdin)
scored = []
for s in data["skills"]:
    text = (s["name"] + " " + s.get("description", "")).lower()
    hits = sum(1 for w in q if w in text)
    if hits:
        scored.append((hits, s["name"], s.get("description", "")[:150]))
for hits, name, desc in sorted(scored, reverse=True)[:8]:
    print(f"  [{hits}] {name}\n      {desc}\n")
'
```

```
  [2] tariff-search
      Tariff calculation and HS code classification via the TurtleClassify API...
```

Not yet in `<available_skills>` → install. **Preferred** (the `skill` tool is available):

```
skill({ action: "install", skill_id: "tariff-search" })
```

> Found **tariff-search** in the internal catalog (tariff + HS-code lookup) and installed it. No external search needed.

*If the `skill` tool were unavailable → use the internal-catalog ZIP fallback in `registries.md`.*

**Early-stop:** a catalog hit ends the search. Never fan out to skills.sh / web / registries.

---

## Example 2 — Layer 1 hit, already installed

**User:** "find a skill for Gmail"

```bash
# catalog search for "gmail email" → gmail-assistant
```

`gmail-assistant` is already in `<available_skills>`.

> **gmail-assistant** is already installed and enabled — it sends, searches, and manages Gmail. Want me to do something specific with it?

No install, no search.

---

## Example 3 — Layer 2 skills.sh hit (the common external path)

**User:** "find a react testing skill"

**Layers 1 ‖ 2 (one turn):** fire the catalog search and `npx skills find "react-testing"`
together. Catalog → 0 hits; the parallel **skills.sh** search hits (clean, ready-to-install):

```bash
npx skills find "react-testing"
```
```
vercel-labs/agent-skills@react-testing-library
└ https://skills.sh/vercel-labs/agent-skills/react-testing-library
```

Map `owner/repo` → `--repo`, skill name → `--path`. **Confirmation gate** (third-party):

> Found **react-testing-library** (official RTL patterns) on skills.sh, repo
> `vercel-labs/agent-skills`. Install into this agent's skills dir?

**User:** "装"

```bash
python3 "$INSTALL" \
  --repo vercel-labs/agent-skills --path react-testing-library --agent-skills
```

**Early-stop:** a clean skills.sh hit ends the search — no web search or registry tail needed.

---

## Example 4 — Layer 3 web search (recall, when skills.sh misses)

**User:** "帮我找个能每日追踪 arxiv 前沿论文的 skill"

**Layers 1 ‖ 2 (one turn):** catalog `arxiv research papers 论文` → 0; parallel
`npx skills find "arxiv"` (kebab-case) → no clean match. Both miss → web search.

**Layer 3 — web search.** Bias the query toward installable repos:

```
daily arxiv paper tracking agent skill SKILL.md github
```

A result points at `https://github.com/DeevsDeevs/agent-system/tree/main/skills/arxiv-search`.
**Build `--repo`/`--path` from the URL itself**, not the user's wording:
`DeevsDeevs/agent-system` + subdir `skills/arxiv-search`.

**Verify before trusting** — dry-run confirms a real `SKILL.md` exists there:

```bash
python3 "$INSTALL" \
  --repo DeevsDeevs/agent-system --path skills/arxiv-search --agent-skills --dry-run
# → "Would install arxiv-search …"  ✅ real skill
```

**Confirmation gate** → on "装", install (drop `--dry-run`):

```bash
python3 "$INSTALL" \
  --repo DeevsDeevs/agent-system --path skills/arxiv-search --agent-skills
```

**Early-stop:** a verified web-search hit ends the search — no registry tail needed.

---

## Example 5 — Layer 4 registry tail (skills.sh + web both miss)

**User:** "find a skill for HS-code / customs classification" *(niche, not on skills.sh, web search only surfaced blog posts)*

Layers 1–3 missed → **read `reference/registries.md`** and walk the tail.

**Tier 1 — ClawHub:**
```bash
clawhub -h >/dev/null 2>&1 || npm i -g clawhub
clawhub search "customs classification"   # → 0 results → go to SkillsMP
```

**Tier 2 — SkillsMP** (keyword search, **no API key**):
```bash
curl -s "https://skillsmp.com/api/v1/skills/search?q=customs+hs+code&limit=5" \
  -H "Accept: application/json" \
  | jq -r '.data.skills[] | "\(.name) by \(.author) ⭐\(.stars)\n  \(.githubUrl)\n"'
```
The API gives **no relevance score** and is noisy — rank by `stars`, pick the best,
confirm, then install straight from its `githubUrl` (it's a full `/tree/...` URL, so
`--url` alone suffices):
```bash
python3 "$INSTALL" --url "<best githubUrl>" --agent-skills
```

---

## Example 6 — no match anywhere

**User:** "find skill for quantum entanglement simulation"

Layers 1–4 + 2 keyword retries (`quantum computing`, `physics simulation`) → nothing usable.

> I searched the internal catalog, skills.sh, the web, and the registry tail
> (ClawHub / SkillsMP) with three query variants and found no real match. I can:
> 1. Do this directly with my general capabilities, or
> 2. Build a custom skill with **skill-creator** (it scaffolds + evals properly).

If `skill-creator` isn't installed, find/install it first (it's first-party — Layer 1).
Fall back to `npx skills init <name>` only if `skill-creator` can't be obtained.

---

## Appendix — skills.sh query cheatsheet (empirical)

`npx skills find` substring-matches your query against kebab-case skill *slugs*
(case-insensitive). A **spaced** query instead triggers fuzzy/description matching —
noisier, lower-install results, and it can silently drop part of your intent
(`pdf docker` → only docker skills, pdf dropped). Measured contrasts:

| Query | Top result | Installs | Verdict |
|---|---|---|---|
| `code-review` | `obra/superpowers@requesting-code-review` | 111K | ✅ hyphenated concept, in order |
| `code review` | `alinaqi/claude-bootstrap@code-review` | 449 | ✗ spaced → marginal |
| `codereview` | `openhands/skills@codereview-roasted` | 121 | ✗ no hyphen → misses `code-review` slugs |
| `review-code` | `nesnilnehc/ai-cortex@review-codebase` | 116 | ✗ wrong order → different skills |
| `Code-Review` | `obra/superpowers@requesting-code-review` | 111K | = case-insensitive |
| `testing` | `anthropics/skills@webapp-testing` | 86.7K | broad + popular |
| `react-testing` | `itechmeat/llm-code@react-testing-library` | 913 | narrowed — excludes general testing |
| `pdf` | `github/awesome-copilot@pdftk-server` | 9.3K | distinctive single word, clean |
| `pdf-form` | `claude-office-skills/skills@pdf form filler` | 2.5K | over-narrow (only 2 results) |
| `code` | `mattpocock/skills@improve-codebase-architecture` | 203K | ✗ off-topic (substring "code") |
| `git` | `xixu-me/skills@github-actions-docs` | 189K | ✗ "git" ⊂ "github" → noise |
| `e2e` | `wshobson/agents@e2e-testing-patterns` | 17.1K | distinctive, clean |

**Loop:** hyphenated concept first → if thin, broaden to the single most distinctive
keyword → if noisy, add a hyphenated qualifier. Always pick high-install **and** on-topic.

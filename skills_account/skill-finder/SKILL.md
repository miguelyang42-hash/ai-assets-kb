---
name: skill-finder
description: >-
  Find, search, recommend, and install agent skills. Layered discovery — internal catalog (first-party, vetted) → skills.sh → web search → ClawHub / SkillsMP. Use when the user wants to find/search/discover/choose/install a skill, or asks "how do I do X", "is there a skill for X", "find me something for X", "该用什么skill", "有没有XX的skill", "帮我找skill", "推荐一个skill".
metadata:
  short-description: Find and install agent skills across catalog, skills.sh, web search, and registries
---

# Skill Finder

Discover and install agent skills. Discovery is **layered and early-stopping**:
walk the layers in order and **STOP at the first good match** — do NOT fan out to
every source by default.

```
┌ 1. Internal Catalog (instant, vetted) ┐  ⚡ fire BOTH in one turn (parallel):
└ 2. skills.sh        (fast, no auth)   ┘  prefer a catalog hit, else skills.sh ──► STOP
        │ both miss
3. Web Search         (broad GitHub recall, dry-run gated) ──► verify candidates in ∥ ──► STOP
        │ failing (see "When web search is failing")
4. ClawHub → SkillsMP (noisy tail) ──► escalate on miss; parallel only in a full sweep
   (read reference/registries.md only when you reach Layer 4)
```

**Order rationale.** Catalog first (vetted, official). Then **skills.sh** — clean,
free, returns *ready-to-install* results, so it's the cheapest high-precision external
source. Then **web search** for recall (it covers all of GitHub, not just what a
registry indexed), made safe by the mandatory `--dry-run` SKILL.md check. **ClawHub /
SkillsMP** are noisier (community / mis-indexed entries), so they're the deep tail.
Note: *trust* is gated separately from *search order* — every external install passes
the confirmation gate below, so searching broad-but-noisy sources is safe.

> ⚡ **Run independent work in parallel** — this agent supports parallel tool calls
> (multiple Bash in one turn). It cuts latency *without* giving up early-stop, because
> you only parallelize work you'd do anyway:
> - **Catalog ‖ skills.sh** as a combined first pass — the catalog (~60 skills) misses
>   often, so don't wait for it serially. Fire both in one turn; on a catalog hit prefer
>   it (vetted) and drop the skills.sh result, else use skills.sh.
> - **Layer 3 candidates** — run the 1–3 `--dry-run` verifications together.
> - **Keyword variants** — fire several `npx skills find` variants at once when the slug
>   is uncertain (skills.sh has no auth / rate limit).
> - **Comprehensive sweep** — when the user wants "best/compare", query skills.sh +
>   ClawHub + SkillsMP in parallel and aggregate.
> - **Multiple installs** — install independent skills concurrently.
>
> **Do NOT** speculatively parallelize the expensive/auth tail (web → ClawHub →
> SkillsMP) on *every* query — those still escalate **only on a miss**. Parallelize work
> already committed to; don't pay for the costly tiers just to skip early-stop.

> 📓 For a concrete walk-through of each layer (catalog hit, skills.sh hit,
> web-search + verify + confirm, registry tail, no-match), see **`reference/examples.md`**.

---

## Paths — anchor on THIS skill's own directory

This skill's **installer script** and the **catalog cache** must resolve to the
**currently running agent's own copy**. Anchor everything on this skill's **load-time
base directory**, then derive the rest. Resolve once at the start, reuse the variables.

```bash
# $SF = the absolute "Base directory for this skill" the host gave you when this skill
# loaded (it ends in …/agent-core/skills/skill-finder). Paste THAT exact path — it is
# the current agent's own copy.
SF="<this skill's load-time base directory>"
INSTALL="$SF/scripts/install-skill-from-github.py"
# Catalog cache is account-level — derive it from $SF (same account as this agent):
CACHE="${SF%/agents/*}/skills/remote_skills_cache.json"

# Fail fast — if either is missing, $SF is wrong; re-read your load-time base dir:
test -f "$INSTALL" && test -f "$CACHE" || echo "Paths wrong: re-check this skill's base dir ($SF)"
```

> ### ⚠️ Never `ls …/accounts/*/agents/*/…/skill-finder*` to find the script
> That glob is the #1 failure mode. This account can have **hundreds** of agents, so
> `head -1` picks some *other* agent's copy — frequently an **older one without
> `scripts/`** (→ `python3: can't open file … No such file or directory`), or a working
> copy that then installs into the **wrong agent** (the installer derives
> `--agent-skills` from its own `__file__` path, not from the current session). Deployed
> copies are even named inconsistently (`skill-finder` vs `skill-finder-new`), so
> `skill-finder*` matches several. **The load-time base dir is the only reliable anchor.**
>
> Only if you genuinely weren't given the base dir, fall back to matching the **script
> file itself** (skips script-less dirs) — and accept it may target another agent:
> ```bash
> INSTALL=$(ls ~/.accio/accounts/*/agents/*/agent-core/skills/skill-finder*/scripts/install-skill-from-github.py 2>/dev/null | head -1)
> SF="${INSTALL%/scripts/*}"; CACHE="${SF%/agents/*}/skills/remote_skills_cache.json"
> ```

---

## Install routing: exact name vs. fuzzy need

| User input | Branch |
|---|---|
| Exact skill id — `"装 pdf"`, `"install image-prompt-guide"`, `"把 yuque 装上"` (single noun / kebab-case) | **name** |
| Descriptive need — `"能处理 PDF 的"`, `"找个发邮件的 skill"`, `"best skill for testing"` | **fuzzy** |

- **name + `skill` tool available** → call `skill({ action: "install", skill_id: "<name>" })`
  directly. No need to read further. On `SKILL_NOT_FOUND`, the skill is external →
  drop into the layers below. On other errors, report — do **not** bypass with bash.
- **fuzzy, or `skill` tool unavailable** → run the layered discovery below.

When unsure which branch, do the **Layer 1 catalog lookup first** — it's cheap and
resolves a fuzzy query into a concrete `skill_id`.

---

## Layer 1 — Internal Catalog (vetted; fire in parallel with Layer 2)

First-party skills, already vetted — the most trustworthy source, but the catalog is
small (~60 skills) and **often misses**. So don't wait for it serially: **fire this
search in the same turn as the Layer 2 `npx skills find` (parallel tool calls)**. On a
catalog hit, prefer it (vetted) and drop the skills.sh result; on a miss, Layer 2's
result is already in hand.

```bash
# Keyword-search the catalog cache ($CACHE, resolved in "Paths" above). Ranks by
# number of query words matched (AND-leaning), not "any word" — avoids the false
# positives you get when one stray word matches dozens of skills.
cat "$CACHE" | python3 -c '
import json, sys
q = "USER_QUERY_KEYWORDS".lower().split()
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

**On a match:**
- Already in `<available_skills>` → tell the user it's installed/enabled, offer to use it.
- Not installed → install it. **Preferred:** `skill({ action: "install", skill_id: "<name>" })`.
  If the `skill` tool is unavailable, use the internal-catalog ZIP fallback in
  `reference/registries.md` ("Internal Catalog — ZIP fallback").

**Good catalog match → install and STOP** (discard the parallel skills.sh result). On a
miss, use the Layer 2 result you fired alongside it.

---

## Layer 2 — skills.sh (clean, fast, no auth — fire with Layer 1)

**Fire this in the same turn as the Layer 1 catalog search (parallel)** — the catalog
often misses, so running them together saves a round-trip. skills.sh is the open
agent-skills index: **ready-to-install** results (real repo + name), no API key, fast.
Prefer a Layer 1 catalog hit if one comes back; otherwise this is your result — and it's
still cheaper/higher-precision than web search, so it stays ahead of Layer 3.

> 🔑 **Query the way skills are *named* (kebab-case), not in prose.** `npx skills find`
> substring-matches your query against kebab-case *slugs* (case-insensitive); spaces
> fall back to fuzzy/description matching — noisier, and can silently drop part of the
> query. Three rules, in order:
> 1. **Hyphenate a multi-word concept, in natural order** — `code-review` (→ 111K-install
>    skills) beats `code review` (→ 449). Not `codereview` (no hyphen → misses the
>    `code-review` slugs) nor `review-code` (wrong order → different skills).
> 2. **Don't over-qualify** — a tacked-on qualifier narrows to slugs containing that exact
>    substring and hides popular general skills: `testing` (86.7K) vs `react-testing`
>    (913); `pdf` (9.3K) vs `pdf-form` (only 2 hits). Thin results → retry the single
>    most distinctive keyword.
> 3. **Avoid ultra-short/common words that substring-collide** — `code` matches
>    `codex-pet`, `git` matches `github-*` → off-topic. Pick a distinctive token (`pdf`, `e2e`).
>
> Results are install-ranked — take what's high-install **and** on-topic; skip substring
> flukes. Full empirical cheatsheet: `reference/examples.md` "Appendix".

```bash
npx skills find "<query>"   # kebab-case, e.g. "code-review"
```

Example output:
```
Install with npx skills add <owner/repo@skill>

vercel-labs/agent-skills@react-testing-library
└ https://skills.sh/vercel-labs/agent-skills/react-testing-library
```

Map the result straight to the installer — `owner/repo` → `--repo`, skill name →
`--path` — then confirm + install (see "Installing" below):

```bash
python3 "$INSTALL" \
  --repo vercel-labs/agent-skills --path react-testing-library --agent-skills
```

> ⚠️ Do **not** install with `npx skills add` — it dumps the skill into a nested
> `.agents/skills/` dir the loader can't read, forcing a manual move. Use
> `npx skills find` only to *discover*; always install with `$INSTALL`.
>
> 🖥️ macOS: don't wrap `npx skills find` in the GNU `timeout` util — it's absent by
> default (`command not found: timeout`). Run it directly.

**Good skills.sh match (no catalog hit) → confirm, install, STOP.** Only when **both**
Layer 1 and Layer 2 miss → Layer 3.

---

## Layer 3 — Web Search (broad GitHub recall)

Reach here when skills.sh has no clean match. Web search covers **all of GitHub**, not
just what a registry indexed — higher recall, at the cost of more triage. The
`--dry-run` gate in step 2 is what makes that safe.

### 1. Search
Use your web search tool. Bias the query toward installable skill repos:

```
<need> agent skill SKILL.md github
# e.g. "daily arxiv paper tracking agent skill SKILL.md github"
```

Prefer results that are **GitHub repositories containing a `SKILL.md`** (at repo root
or in a subdirectory). Skip blog posts, docs, and listicles. Collect 1–3 candidate
`owner/repo` (+ subdir path if it's a monorepo).

> **Build `--repo`/`--path` from the actual GitHub URL in the result — never from the
> user's wording or a remembered name.** Repos get renamed: GitHub redirects the old
> name on download, but the downloaded tree's top-level dir is the *current* name, so a
> stale `--repo` makes `--path` resolve against the wrong tree and fails with
> `SKILL.md not found`. When the result URL differs from what the user typed, trust the
> URL. Likewise copy the subdir path verbatim from the URL, don't guess it.

### 2. Verify before trusting (this is the key step)
**Never install on the strength of a search snippet.** For each candidate, run a
`--dry-run` — it resolves the source and **validates that a real `SKILL.md` exists at
that path**. This check is deterministic; it catches "the model picked a repo that
isn't actually a skill" without relying on judgment. **Have 2–3 candidates? Fire their
`--dry-run`s in parallel (one turn)** and keep the one that validates with the best fit.

```bash
python3 "$INSTALL" \
  --repo <owner>/<repo> --path <subdir-or-.> --agent-skills --dry-run
```

- `--dry-run` prints "Would install …" → the skill is real. Show the user the source
  URL + the skill's `name`/`description`, get confirmation, then install (drop `--dry-run`).
- `--dry-run` fails with `SKILL.md not found` → wrong path or not a skill. Try the
  correct subdir, or discard the candidate.

> 🎯 **Locate `--path` with this exact ladder — don't improvise other methods.** The
> variance that makes installs slow is ad-hoc `gh api` / `git ls-remote` / `curl` probing
> across many turns. `--dry-run` is cheap now (checks
> `raw.githubusercontent.com/<repo>/<ref>/<path>/SKILL.md`, ~0.3s, **no download** — a
> wrong path fails in <1s). Go in order, **stop at the first hit**:
> 1. **Deep tree URL** (`…/tree/<ref>/skills/foo`)? The subdir **is** the path — pass the
>    URL to `--url`; the script extracts it. No probing, no cloning.
> 2. **Repo only, conventional layout?** Probe the 3 common spots in **one bash** (each
>    dry-run is ~0.3s); use whichever prints "Would install":
>    ```bash
>    for p in . "<skill-name>" "skills/<skill-name>"; do
>      echo "--- $p ---"; python3 "$INSTALL" --repo <o>/<r> --path "$p" --agent-skills --dry-run
>    done
>    ```
> 3. **Probe missed** (unconventional path, e.g. `.claude/skills/foo`)? Enumerate once,
>    **without downloading file contents** (light even for monorepos):
>    ```bash
>    git clone --filter=blob:none --no-checkout --depth 1 https://github.com/<o>/<r> /tmp/r \
>      && git -C /tmp/r ls-tree -r HEAD --name-only | grep -i skill.md; rm -rf /tmp/r
>    ```
>    Use the printed dir (minus `/SKILL.md`) as `--path`.
>
> **Do NOT use `gh api` / `git ls-remote` / hand-rolled `curl` for this.** raw-probe (2)
> and the blobless clone (3) are cheaper, need no auth, and dodge the GitHub API
> 60-req/hr limit that throttles `gh api` / `curl api.github.com` and triggers the thrash.

### When web search is failing → go to Layer 4
Treat web search as underperforming (and fall back to the noisy registries) when **any** of:
- 0 relevant results, or only articles/docs — no installable repo.
- Every candidate fails `--dry-run` (no valid `SKILL.md`).
- After **2** retries with different keywords (synonym / broader / narrower) still nothing.

Don't loop on web search indefinitely — two honest retries, then fall back.

---

## Layer 4 — ClawHub → SkillsMP (noisy registry tail — read `reference/registries.md`)

Last resort, only when skills.sh **and** web search both miss. These are noisier
(community-submitted / mis-indexed entries), so they sit at the bottom. **Read
`reference/registries.md`** for exact CLI flags, the API endpoint, and parsing. Walk
in order, STOP at the first hit (but for an explicit **"best/compare"** request, skip
early-stop and run both **in parallel**, then aggregate by installs/stars/fit):

1. **ClawHub** — `clawhub search <query>` → `clawhub install <slug> --force`. Needs the
   `clawhub` CLI (`npm i -g clawhub`); uses its own registry, not GitHub.
2. **SkillsMP** — keyword REST search, **no auth needed**; returns a `githubUrl`
   (usually a full `/tree/<ref>/<subdir>` URL) → feed straight to `$INSTALL` (`--url`
   alone suffices). Largest DB but noisiest — rank hits by stars yourself.

GitHub-backed results (SkillsMP, or a skills.sh retry) install through the **same
`$INSTALL` script**. Only ClawHub uses its own `clawhub install`.

---

## Installing (unified) + confirmation gate

One script installs every GitHub source — whole-repo skills (`--path .`) and monorepo
subdirs (`--path <dir>`) alike. It sparse-checks out only the target, validates
`SKILL.md`, and installs to the right level. It auto-resolves the Accio dirs from its
own location, so you don't hand-build long paths.

```bash
# Agent-level (default): only this agent
python3 "$INSTALL" \
  --repo <owner>/<repo> --path <subdir-or-.> --agent-skills
# Account-level (shared by all agents): swap the flag
python3 "$INSTALL" \
  --repo <owner>/<repo> --path <subdir-or-.> --account-skills
```

| Flag | Notes |
|---|---|
| `--repo owner/repo` / `--url <github-tree-url>` | Source (one of). |
| `--path <dir> [<dir> …]` | Dir that **directly contains `SKILL.md`**; `.` = whole-repo skill. Multiple = install several. |
| `--agent-skills` / `--account-skills` | Auto-resolved dest. Pick exactly one. `--agent-skills` is the default choice. |
| `--ref <branch/tag/sha>` | Default `main`; set for `master` etc. |
| `--name <name>` | Override folder name (defaults to last path segment / repo name for `.`). |
| `--force` | Overwrite if destination exists (default: error). |
| `--dry-run` | Resolve + validate `SKILL.md`, copy nothing. |

> **⚠️ Confirmation gate (required for external skills).** Anything from Layers 2–4 is
> third-party code. Before the real install (not `--dry-run`), show the user: **source
> URL**, the skill's **`name` + `description`**, and the **install target**. Wait for a
> clear yes. Layer 1 (vetted catalog) does not need this gate.
>
> Private repos: export `GITHUB_TOKEN` (or `GH_TOKEN`) first.

### Verify after install
```bash
ls "${SF%/*}/<name>/SKILL.md"   # ${SF%/*} = THIS agent's agent-core/skills dir
```
The runtime auto-registers any skill dir dropped in the right place — **never hand-edit
`skills.jsonc` / `skills_config.json`** (manual edits get overwritten).

---

## No match anywhere
After Layers 1–4 and 2 keyword retries with nothing usable:
1. Tell the user no existing skill was found.
2. Offer to do the task directly with general capabilities.
3. Offer to build a custom skill with the **`skill-creator`** skill — it scaffolds,
   edits, and evals skills properly. If it isn't available, find/install it first
   (it's a first-party skill — search Layer 1). Fall back to `npx skills init <name>`
   only when `skill-creator` can't be obtained.

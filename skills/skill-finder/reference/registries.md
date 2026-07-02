# Registry Tail Reference (Layer 4)

Loaded **only** when you reach **Layer 4** — i.e. the internal catalog, skills.sh, and
web search have all missed (see SKILL.md "When web search is failing"). Covers the two
noisy registries; walk in order, STOP at the first good match.

> skills.sh is **Layer 2**, not part of this tail — its quick-use (`npx skills find` →
> `$INSTALL`) is inline in SKILL.md. Don't come here for it.

SkillsMP results are GitHub-backed and install through the same
`scripts/install-skill-from-github.py` (`$INSTALL`) used in Layers 2–3. Only ClawHub
installs via its own CLI. The **confirmation gate** in SKILL.md applies to every install here.

> 🖥️ macOS note: do **not** wrap these commands in the GNU `timeout` utility — it is
> absent on macOS by default (`command not found: timeout`). Run the commands directly,
> or use `perl -e 'alarm shift; exec @ARGV' <seconds> <cmd>` if you need a hard limit.

---

## 1. ClawHub (`clawhub`) — community registry, own installer

Uses its own registry (not GitHub), so it keeps its own installer.

> 🔑 ClawHub is also registry/slug-based, so the same **kebab-case** query habit from
> skills.sh (`code-review`, not `code review`) tends to help here too.

```bash
# Ensure the CLI exists (only if you reach this tier):
clawhub -h >/dev/null 2>&1 || npm i -g clawhub

clawhub search <query>
# Install non-interactively (--force bypasses "suspicious skill" prompts in agents):
clawhub install <slug> --dir "${SF%/*}" --force    # ${SF%/*} = THIS agent's skills dir ($SF from SKILL.md Paths)
```

| Command | Description |
|---|---|
| `clawhub search <query>` | Search skills |
| `clawhub install <slug> --force` | Install (use `--force` in agents) |
| `clawhub install <slug> --version 1.2.3 --force` | Install a specific version |
| `clawhub update <skill> --force` / `clawhub update --all --no-input --force` | Update |
| `clawhub list` | List installed |

- Default registry https://clawhub.com (override `CLAWHUB_REGISTRY` / `--registry`).
- Default install dir `./skills` (override `--dir` / `CLAWHUB_WORKDIR`).

---

## 2. SkillsMP (REST API) — largest DB, keyword search, no auth

Biggest catalog but the **noisiest** — many results are low-star or are docs pages
mis-indexed as skills. It's last in the order for **quality** (rank by stars /
inspect the repo before trusting), not because it's slow or gated. **No API key is
needed for search.**

> ⚠️ The old semantic endpoint `…/skills/ai-search` is **gone** — it returns
> `ENDPOINT_NOT_FOUND` (verified 2026-06; live endpoints: `/skills/search`,
> `/api/v1`, `/api/health`, `/api/llms.txt`, `/api/timeline`). Use the keyword
> endpoint `…/skills/search` below; it's open (no `Authorization` header) and
> returns a `githubUrl` directly.

### Keyword search (open — no auth header)
```bash
curl -s "https://skillsmp.com/api/v1/skills/search?q=<url-encoded-query>&limit=5" \
  -H "Accept: application/json" \
  | jq -r '.data.skills[] | "\(.name) by \(.author) ⭐\(.stars)\n  \(.description[0:100])\n  \(.githubUrl)\n"'
```

| Param | Required | Description |
|---|---|---|
| `q` | yes | Query string (URL-encoded). Plain keywords, e.g. `code-review`. |
| `limit` | no | Default 20, max 100 |

Response shape is `.data.skills[]` — each object carries `name`, `author`,
`description`, `githubUrl`, `skillUrl`, `stars`, `updatedAt` **directly** (note:
this differs from the dead ai-search shape `.data.data[].skill`). The API returns
**no relevance score**, so rank the hits yourself by `stars` + how well
`description` matches the need.

**Install:** the `githubUrl` is usually a full `/tree/<ref>/<subdir>` URL, and the
installer extracts the repo, ref, **and** subdir from it — so `--url` alone is
enough (no `--path`/`--ref` needed):
```bash
# $INSTALL is already resolved in SKILL.md "Paths" (anchored on this skill's base dir —
# do NOT re-glob across agents/*, it picks the wrong agent).
python3 "$INSTALL" --url "<githubUrl>" --agent-skills
# Only if the githubUrl is a bare repo root (no /tree/...): add  --path .
```

- **Errors:** `MISSING_QUERY` 400 → add `q`. The endpoint is open, so the old
  `INVALID_API_KEY` / `DAILY_QUOTA_EXCEEDED` auth errors no longer apply to search.

---

## Internal Catalog — ZIP fallback (Layer 1, when the `skill` tool is unavailable)

Use **only** when the `skill` tool is NOT in `<available_tools>`. When it is available,
always prefer `skill({ action: "install", skill_id: "<name>" })` — atomic and official.

```bash
# $SF and $CACHE come from SKILL.md "Paths" (anchored on this skill's base dir).
# Derive THIS agent's skills dir from $SF — never glob across agents/*:
SKILLS="${SF%/*}"                 # …/agent-core/skills  (current agent)
DIR="$SKILLS/{skillName}"
URL=$(cat "$CACHE" | \
  python3 -c "import json,sys; d=json.load(sys.stdin); [print(s['oss']) for s in d['skills'] if s['name']=='{skillName}']")
mkdir -p "$DIR" && curl -sL "$URL" -o /tmp/skill.zip && \
  unzip -q -o /tmp/skill.zip -d "$DIR" && \
  mv "$DIR"/{skillName}/* "$DIR"/ 2>/dev/null; rmdir "$DIR"/{skillName} 2>/dev/null; \
  rm /tmp/skill.zip
```

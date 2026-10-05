# noslop

An [Agent Skill](https://agentskills.io/specification) for writing and editing prose that reads like a person wrote it. It has three modes:

- **Write:** drafts new content from a brief, and asks the user for the specifics it needs.
- **Edit:** makes the minimum effective edit to a draft and keeps the writer's voice.
- **Audit:** names each AI-writing pattern in a text with the quoted line and a fix, without rewriting.

## Layout

```
noslop/
├── SKILL.md                     core instructions (loaded when the skill activates)
├── references/
│   ├── patterns.md              41 patterns, tiered, each with before/after
│   ├── words.md                 word and phrase lists with plain replacements
│   ├── examples.md              12 full rewrites, including over-correction and light-touch cases
│   ├── social.md                LinkedIn, X, Threads
│   ├── longform.md              blog posts, newsletters, essays
│   └── marketing-email.md       landing pages, product copy, email
└── scripts/
    └── scan.py                  regex backstop for mechanical tells (stdlib only)
```

## Design choices

- **Tiered patterns.** Tier 1 tells (not-X-but-Y, staged openers, chatbot residue, dashes) get fixed on sight. Tier 2 gets fixed when it repeats. Tier 3 only matters alongside other tells. Absolute rules like "no adverbs" or "no passive voice" over-correct into a different kind of robotic prose.
- **Positive guidance first.** SKILL.md leads with what human prose does. Word lists load during the check pass, because reading a banned list right before drafting tends to prime those words.
- **No fabricated humanity.** Specifics make writing read as human, so the skill asks the user for them and never makes them up.
- **Over-correction is a named failure.** Terse fragments, synonym swaps, fake typos and replacement kickers are all slop too.
- **Venue changes the rules.** On X and LinkedIn, hooks, line breaks, punchy closers and questions to readers are allowed as platform conventions. The skill keeps those mechanics and requires real substance and fresh wording inside them. Websites, email and long-form get the strict rules.
- **Zero em dashes by default.** The rule gives way when the user's voice sample uses dashes.

## Scanner

```
python3 scripts/scan.py draft.md          # Tier 1 and 2 hits plus rhythm stats
python3 scripts/scan.py --all draft.md    # include Tier 3
python3 scripts/scan.py --social post.txt # relax hook/question rules for social
pbpaste | python3 scripts/scan.py         # stdin
```

Exits 1 if any Tier 1 pattern is found. It flags candidates for the agent to judge.

## Credits

Built on ideas and patterns from:

- [stop-slop](https://github.com/hardikpandya/stop-slop) by Hardik Pandya (MIT)
- [no-ai-slop](https://github.com/petergyang/no-ai-slop) by Peter Yang (MIT)
- [humanizer](https://github.com/blader/humanizer) by blader (MIT)
- [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing), WikiProject AI Cleanup
- Kobak et al., [Delving into ChatGPT usage in academic writing through excess vocabulary](https://arxiv.org/abs/2406.07016)
- Paech et al., [Antislop](https://arxiv.org/abs/2510.15061)
- Orwell, "Politics and the English Language"; Zinsser, *On Writing Well*; Paul Graham, ["Write Simply"](https://www.paulgraham.com/simply.html); Gary Provost, *100 Ways to Improve Your Writing*

# noslop

An [Agent Skill](https://agentskills.io/specification) for writing and editing prose that reads like a person wrote it. It has three modes:

- **Write:** drafts new content from a brief, and asks the user for the specifics it needs.
- **Edit:** makes the minimum effective edit to a draft and keeps the writer's voice.
- **Audit:** names each AI-writing pattern in a text with the quoted line and a fix, without rewriting.

## Install

```
npx skills add shanvaliyev/noslop
```

## Layout

```
noslop/
├── SKILL.md                     core instructions (loaded when the skill activates)
└── references/
    ├── patterns.md              20 patterns, each with before/after
    ├── words.md                 stock words and phrases with plain replacements
    ├── formats.md               social posts, long-form, marketing copy, email
    └── examples.md              5 full rewrites, including over-correction and light-touch cases
```

## Design choices

- **Judgment over checklists.** Most patterns matter only when they cluster, because one instance is ordinary human writing. Only chatbot residue, leftovers and dashes are removed every time. Absolute rules like "no adverbs" or "no passive voice" over-correct into a different kind of robotic prose, and a long rulebook makes the model worse at writing in general.
- **Positive guidance first.** SKILL.md leads with what human prose does. Word lists load during the check pass, because reading a banned list right before drafting tends to prime those words.
- **No fabricated humanity.** Specifics make writing read as human, so the skill asks the user for them and never makes them up.
- **Over-correction is a named failure.** Terse fragments, synonym swaps, fake typos and replacement kickers are all slop too.
- **Venue changes the rules.** On X and LinkedIn, hooks, line breaks, punchy closers and questions to readers are allowed as platform conventions. The skill keeps those mechanics and requires real substance and fresh wording inside them. Websites, email and long-form get the default rules.
- **Zero em dashes by default.** The rule gives way when the user's voice sample uses dashes.

## Used by

- [AgentKYZ](https://agentkyz.com) runs KYC and AML compliance as a managed service for funds, brokerages, fund administrators, asset managers and banks. AI agents work each case, compliance specialists review the files, and pricing is fixed per case.

Using noslop in your product or team? Open a PR to add yourself.

## Credits

Built on ideas and patterns from:

- [stop-slop](https://github.com/hardikpandya/stop-slop) by Hardik Pandya (MIT)
- [no-ai-slop](https://github.com/petergyang/no-ai-slop) by Peter Yang (MIT)
- [humanizer](https://github.com/blader/humanizer) by blader (MIT)
- [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing), WikiProject AI Cleanup
- Kobak et al., [Delving into ChatGPT usage in academic writing through excess vocabulary](https://arxiv.org/abs/2406.07016)
- Paech et al., [Antislop](https://arxiv.org/abs/2510.15061)
- Orwell, "Politics and the English Language"; Zinsser, *On Writing Well*; Paul Graham, ["Write Simply"](https://www.paulgraham.com/simply.html); Gary Provost, *100 Ways to Improve Your Writing*

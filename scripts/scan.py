#!/usr/bin/env python3
"""Flag mechanical AI-writing tells in prose. A backstop, not a judge.

Usage:
    python3 scripts/scan.py draft.md [more files...]
    cat draft.txt | python3 scripts/scan.py

Skips fenced code blocks, inline code, and URLs. Prints one line per hit:
    path:line  T1  pattern  "matched text"
Then a short summary with rhythm stats.

Options:
    --all      also report Tier 3 (weak-alone) hits
    --social   social-post mode: self-answered questions and reader
               questions ("Thoughts?") drop to Tier 3, since hooks and
               engagement questions are platform craft on X and LinkedIn

Exit code: 1 if any Tier 1 hit was found, else 0. No dependencies.
"""

import re
import statistics
import sys

# (tier, name, regex). Case-insensitive. Keep patterns high-precision:
# a false positive here costs the agent a rewrite it didn't need.
PATTERNS = [
    # Tier 1: fix on sight
    (1, "em/en dash", r"\s?[—]\s?|\s[–]\s|\s--\s"),
    (1, "not X but Y", r"\b(?:it's|it is|this is|that's|that is|isn't|is not|wasn't|was not)\s+(?:not\s+)?(?:just|only|merely|simply|about)\b[^.?!\n—–]{0,80}(?:[,;.]|\s?[—–])\s*(?:it's|it is|but|it was)\b"),
    (1, "not X but Y", r"\bnot (?:just|only|merely) [^.?!\n]{1,60}\bbut(?: also)?\b"),
    (1, "not X but Y", r"\b(?:isn't|is not|aren't|wasn't) the (?:problem|point|question|answer|goal|issue)\b"),
    (1, "more than just", r"\bmore than just\b"),
    (1, "staged opener", r"(?:^|[.!?]\s+)(?:here's the thing|here's (?:what|why|how)\b|let's dive in|let's dive into|let's break (?:it|this) down|let me be clear|the truth is|the reality is|the uncomfortable truth|real talk|honestly\?|buckle up|without further ado)"),
    (1, "faux insight", r"\b(?:what nobody tells you|what no one tells you|nobody talks about|what most people (?:get wrong|miss|don't realize)|the part (?:everyone|most people) (?:misses|miss|skip)|here's where it gets interesting|the secret is)\b"),
    (1, "kicker", r"\b(?:let that sink in|read that again|that's the real win|that's the whole game|that changes everything|full stop\.|mic drop|food for thought)"),
    (1, "self-answered question", r"(?:^|[.!]\s+)(?:the (?:result|answer|catch|kicker|twist|best part|problem|secret)|why|how)\?\s+\S"),
    (1, "chatbot residue", r"\b(?:great question|i hope this helps|i'd be happy to|certainly!|absolutely!|feel free to (?:reach out|ask|let me know)|let me know if you(?:'d| would) like|would you like me to|don't hesitate to|i hope this (?:email|message) finds you|as an ai\b|as of my (?:last|knowledge))"),
    (1, "leaked markup", r"oaicite|contentReference|turn\d+search\d+|utm_source=chatgpt|\[cite:\s*\d+\]|【|】|\[your name\]|\[company(?: name)?\]|lorem ipsum"),
    (1, "recap ending", r"(?:^|\n)\s*(?:in conclusion|in summary|to sum up|to summarize)\b"),
    (1, "inflated significance", r"\b(?:marks? a (?:pivotal|significant|major) (?:moment|milestone|shift)|stands? as a testament|a testament to|plays? a (?:vital|crucial|key|pivotal) role|underscores? the importance|sets? the stage for|paves? the way for|indelible mark|lasting legacy|the future looks bright|exciting times ahead|continues to thrive)\b"),
    (1, "-ing rider", r",\s+(?:highlighting|underscoring|showcasing|reflecting|emphasizing|symbolizing|cementing|solidifying)\b"),
    (1, "stock AI word", r"\b(?:delve[sd]?|delving|tapestry|testament|multifaceted|meticulous(?:ly)?|realm|paramount|intricacies|interplay|bolster(?:ed|s|ing)?|garner(?:ed|s|ing)?|showcas(?:e|es|ed|ing)|underscor(?:e|es|ed|ing)|leverag(?:e|es|ed|ing)|utiliz(?:e|es|ed|ing)|facilitat(?:e|es|ed|ing)|foster(?:s|ed|ing)?|embark(?:s|ed|ing)?|unveil(?:s|ed|ing)?|groundbreaking|transformative|ever-evolving|game-?changer|cutting-edge|seamless(?:ly)?|supercharge[sd]?|nestled|breathtaking|load-bearing)\b"),
    # Tier 2: fix when it repeats or clusters
    (2, "sales word", r"\b(?:unlock(?:s|ed|ing)?|elevat(?:e|es|ed|ing)|empower(?:s|ed|ing)?|revolutioniz(?:e|es|ed|ing)|robust|vibrant|pivotal|crucial|landscape|ecosystem|journey|curated|bespoke|world-class|best-in-class|next-level|reimagined)\b"),
    (2, "filler transition", r"(?:^|\n|[.!?]\s+)(?:moreover|furthermore|additionally|notably|importantly|interestingly|ultimately|consequently),"),
    (2, "signposting", r"\b(?:it's worth noting|it is worth noting|it's important to (?:note|remember)|in this (?:post|article|guide|essay),? (?:we|i)(?:'ll| will)|as we'll see|needless to say|it goes without saying|when it comes to|at the end of the day|in today's (?:fast-paced|digital|ever-changing|modern)|in an era (?:of|where)|the key takeaway)\b"),
    (2, "reader sweep", r"\bwhether you're an? [^,.\n]{1,40} or an? \b|\bfrom (?:startups|beginners|small businesses|freelancers) to\b"),
    (2, "fake-strong verb", r"\b(?:serves as|stands as|functions as|acts as|boasts)\b"),
    (2, "weasel authority", r"\b(?:experts (?:say|agree|believe)|studies (?:show|suggest)|research (?:shows|suggests)|many (?:believe|argue)|it is widely (?:known|believed|accepted))\b"),
    (2, "stacked hedge", r"\b(?:could potentially|might possibly|may potentially|could possibly|may arguably|arguably could)\b"),
    (2, "arguing with no one", r"(?:^|[.!?]\s+)(?:don't get me wrong|i'm not saying|to be clear|this isn't to say|you might be thinking)\b"),
    (2, "false balance", r"\b(?:the truth (?:lies|is) somewhere in (?:the middle|between)|depends on your (?:unique |specific )?needs)\b"),
    (2, "engagement bait", r"(?:^|\n)\s*(?:agree\?|thoughts\?|what do you think\?|repost if|follow (?:me )?for more)"),
    (2, "announcement template", r"\bi'm (?:thrilled|excited|humbled|honored|delighted) to (?:announce|share)\b"),
    (2, "emoji bullet", r"(?:^|\n)\s*[✅\U0001F680\U0001F4A1\U0001F3AF\U0001F449✨\U0001F525\U0001F4C8➡→]\s*"),
    (2, "bold label bullet", r"(?:^|\n)\s*[-*]\s+(?:\S+\s+)?\*\*[^*\n]{1,40}(?::\*\*|\*\*:)"),
    (2, "fancy unicode", r"[\U0001D400-\U0001D7FF]"),
    # Tier 3: weak alone, reported only in --all mode
    (3, "empty adverb", r"\b(?:genuinely|truly|deeply|incredibly|literally|fundamentally|inherently|quietly)\b"),
    (3, "curly quote", r"[“”‘]"),
]

COMPILED = [(t, n, re.compile(p, re.IGNORECASE)) for t, n, p in PATTERNS]
SOCIAL_SOFT = {"self-answered question", "engagement bait", "announcement template"}
SENT_SPLIT = re.compile(r"(?<=[.!?])\s+(?=[A-Z\"'(])")


def strip_code(text):
    """Blank out fenced code, inline code, and URLs, keeping line numbers."""
    out, in_fence = [], False
    for line in text.split("\n"):
        if line.lstrip().startswith(("```", "~~~")):
            in_fence = not in_fence
            out.append("")
            continue
        if in_fence:
            out.append("")
            continue
        line = re.sub(r"`[^`]*`", " ", line)
        line = re.sub(r"https?://\S+", " ", line)
        out.append(line)
    return out


def rhythm(lines):
    prose = " ".join(l.strip().lstrip(">#-* ") for l in lines if l.strip())
    sents = [s for s in SENT_SPLIT.split(prose) if len(s.split()) >= 2]
    if len(sents) < 8:
        return None
    lengths = [len(s.split()) for s in sents]
    return len(sents), statistics.mean(lengths), statistics.pstdev(lengths)


def scan(label, text, show_all, social=False):
    lines = strip_code(text)
    hits = []
    for i, line in enumerate(lines, 1):
        for tier, name, rx in COMPILED:
            if social and name in SOCIAL_SOFT:
                tier = 3
            if tier == 3 and not show_all:
                continue
            for m in rx.finditer(line):
                snippet = m.group(0).strip().lstrip(".!? ").strip() or m.group(0)
                hits.append((tier, i, name, snippet))
    for tier, i, name, snippet in sorted(hits, key=lambda h: (h[1], h[0])):
        print(f"{label}:{i}  T{tier}  {name}  \"{snippet}\"")

    counts = {1: 0, 2: 0, 3: 0}
    for h in hits:
        counts[h[0]] += 1
    words = sum(len(l.split()) for l in lines)
    summary = f"{label}: {words} words, T1={counts[1]} T2={counts[2]}"
    if show_all:
        summary += f" T3={counts[3]}"
    r = rhythm(lines)
    if r:
        n, mean, sd = r
        summary += f", {n} sentences, mean length {mean:.1f}, spread {sd:.1f}"
        if sd < 4.5:
            summary += " (low spread: sentences may sound metronomic)"
    print(summary)
    return counts[1]


def main(argv):
    show_all = "--all" in argv
    social = "--social" in argv
    paths = [a for a in argv if a not in ("--all", "--social")]
    if any(a in ("-h", "--help") for a in paths):
        print(__doc__.strip())
        return 0
    tier1 = 0
    if not paths:
        tier1 += scan("stdin", sys.stdin.read(), show_all, social)
    for p in paths:
        try:
            with open(p, encoding="utf-8") as f:
                tier1 += scan(p, f.read(), show_all, social)
        except OSError as e:
            print(f"scan.py: cannot read {p}: {e.strerror}", file=sys.stderr)
            return 2
    return 1 if tier1 else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

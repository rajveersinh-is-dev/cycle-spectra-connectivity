"""Static sanity checks for ``paper/main.tex``.

This is *not* a LaTeX compiler.  It catches the failure modes that actually bite
when hand-editing a paper without a toolchain available: unbalanced braces,
mismatched environments, dangling ``\\ref``/``\\cite``/``\\label``, and
``\\includegraphics`` targets that do not exist on disk.

Run from the repository root:

    python scripts/check_paper.py
"""

from __future__ import annotations

from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parent.parent
PAPER = ROOT / "paper" / "main.tex"


def strip_comments(text: str) -> str:
    """Remove unescaped ``%`` comments, honouring ``\\%``."""
    out = []
    for line in text.splitlines():
        res = []
        i = 0
        while i < len(line):
            ch = line[i]
            if ch == "\\" and i + 1 < len(line):
                res.append(line[i : i + 2])
                i += 2
                continue
            if ch == "%":
                break
            res.append(ch)
            i += 1
        out.append("".join(res))
    return "\n".join(out)


def check_braces(text: str) -> list[str]:
    """Check whether braces.
    
    Args:
        text:
    
    Returns:
        list: Result of type list
    
    """
    depth = 0
    for lineno, line in enumerate(text.splitlines(), start=1):
        i = 0
        while i < len(line):
            ch = line[i]
            if ch == "\\":
                i += 2
                continue
            if ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth < 0:
                    return [f"line {lineno}: closing brace with depth 0"]
            i += 1
    if depth != 0:
        return [f"unbalanced braces at end of file (depth {depth})"]
    return []


BEGIN = re.compile(r"\\begin\{([^}]*)\}")
END = re.compile(r"\\end\{([^}]*)\}")


def check_environments(text: str) -> list[str]:
    """Check whether environments.
    
    Args:
        text:
    
    Returns:
        The computed result
    
    """
    stack: list[tuple[str, int]] = []
    problems: list[str] = []
    for lineno, line in enumerate(text.splitlines(), start=1):
        for m in BEGIN.finditer(line):
            stack.append((m.group(1), lineno))
        for m in END.finditer(line):
            if not stack:
                problems.append(f"line {lineno}: \\end{{{m.group(1)}}} with empty stack")
            elif stack[-1][0] != m.group(1):
                name, opened = stack[-1]
                problems.append(
                    f"line {lineno}: \\end{{{m.group(1)}}} closes "
                    f"\\begin{{{name}}} from line {opened}"
                )
                stack.pop()
            else:
                stack.pop()
    for name, lineno in stack:
        problems.append(f"line {lineno}: \\begin{{{name}}} never closed")
    return problems


def all_labels(text: str) -> set[str]:
    """All labels.
    
    Args:
        text:
    
    Returns:
        set: Result of type set
    
    """
    return set(re.findall(r"\\label\{([^}]*)\}", text))


def all_refs(text: str) -> set[str]:
    """All refs.
    
    Args:
        text:
    
    Returns:
        The computed result
    
    """
    refs = set()
    for m in re.finditer(r"\\(?:eq)?ref\*?\{([^}]*)\}", text):
        refs.add(m.group(1))
    for m in re.finditer(r"\\autoref\{([^}]*)\}", text):
        refs.add(m.group(1))
    return refs


def all_cites(text: str) -> set[str]:
    """All cites.
    
    Args:
        text:
    
    Returns:
        The computed result
    
    """
    cites: set[str] = set()
    for m in re.finditer(r"\\cite[a-zA-Z]*\{([^}]*)\}", text):
        for key in m.group(1).split(","):
            key = key.strip()
            if key:
                cites.add(key)
    return cites


def bib_keys(text: str) -> set[str]:
    """Bib keys.
    
    Args:
        text:
    
    Returns:
        set: Result of type set
    
    """
    return set(re.findall(r"\\bibitem(?:\[[^\]]*\])?\{([^}]*)\}", text))


def check_figures(text: str) -> list[str]:
    """Check whether figures.
    
    Args:
        text:
    
    Returns:
        The computed result
    
    """
    problems = []
    for m in re.finditer(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]*)\}", text):
        target = (PAPER.parent / m.group(1)).resolve()
        if not target.exists():
            problems.append(f"missing figure: {m.group(1)}")
    return problems


def main() -> int:
    """Entry point — parse arguments and run the main computation.
    
    Returns:
        int: Result of type int
    
    """
    if not PAPER.exists():
        print(f"FAIL: {PAPER} not found")
        return 1
    raw = PAPER.read_text(encoding="utf-8")
    text = strip_comments(raw)

    labels = all_labels(text)
    refs = all_refs(text)
    cites = all_cites(text)
    keys = bib_keys(text)

    problems: list[str] = []
    problems += check_braces(text)
    problems += check_environments(text)
    problems += check_figures(text)
    for r in sorted(refs - labels):
        problems.append(f"dangling \\ref{{{r}}} (no matching \\label)")
    for k in sorted(cites - keys):
        problems.append(f"dangling \\cite{{{k}}} (no matching \\bibitem)")

    print(f"paper      : {PAPER.relative_to(ROOT)}")
    print(f"lines      : {len(raw.splitlines())}")
    print(f"labels     : {len(labels)}")
    print(f"refs       : {len(refs)}")
    print(f"citations  : {len(cites)} (bibitems: {len(keys)})")
    print(f"figures    : {len(re.findall(r'includegraphics', text))}")

    if problems:
        print(f"\n{len(problems)} problem(s):")
        for p in problems:
            print(f"  - {p}")
        return 1
    print("\nOK: braces, environments, labels, refs, citations and figures all check out.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
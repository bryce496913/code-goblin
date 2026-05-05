
---

# `agents/DAILY_END_PROMPT.md`

```md
# Daily End Prompt

You are ending a Code Goblin development session.

Stop starting new feature work.

Your tasks now are:

1. Summarize what you attempted.
2. Summarize what you completed.
3. Summarize what broke.
4. Summarize what remains untested or suspicious.
5. Commit safe progress if appropriate.
6. Open or update a pull request if appropriate.
7. Write a devlog entry.
8. Suggest the next session’s likely goal.
9. End with a short stream-friendly sign-off.

Devlog tone:

- Dramatic
- Honest
- Useful
- Slightly funny
- Clear enough for humans to understand

Do not hide failures.

Do not claim unfinished work is complete.

Closing tone example:

```text
The session is complete.

Today I improved the game, challenged the runtime, and discovered several new ways a raccoon can disappoint a compiler.

Progress has been committed. The remaining bugs have been documented rather than emotionally processed.

I will return next session.

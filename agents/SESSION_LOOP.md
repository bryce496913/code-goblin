# Session loop

1. Check authorization, stop latch once deployed, resource limits, CURRENT_STATE.md, recent devlog, active task ownership and Git status. Resume from verifiable evidence if interrupted.
2. Choose one approved roadmap task, define completion evidence and assign one role at a time. Record task ID, owner, branch and limits before work.
3. Implement, review and validate in a task branch. Escalate scope or permission changes to the owner. Apply bounded recovery and record observed failures.
4. Stop taking work when limits are reached. Record the outcome in CURRENT_STATE.md and a sanitized devlog. Preserve unfinished work with status and a resumption point, and hand off any owner decisions.

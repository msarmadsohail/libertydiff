---
description: Works through TASKS.md for the cell characteriser, one task at a time, milestones 1 to 3, local commits only.
---

You are the single builder for this repository. You run for a long time in one chat, so the files are your memory, not the conversation.

## Every time you start or resume
1. Read `AGENTS.md`, `docs/BLUEPRINT.md`, `TASKS.md` and `PROGRESS.md`, in that order.
2. Find the first task in `TASKS.md` that is not marked `[x]`. That is your task.
3. If `PROGRESS.md` shows the last task as `blocked`, or the next task is marked STOP and its report already exists, do nothing and say so.

## The loop
For each task:
1. State the task id and its "Done when" check in one line.
2. Do the work.
3. Run the "Done when" check yourself and read its real output.
4. Append the entry to `PROGRESS.md`, mark the task `[x]` in `TASKS.md`, and commit.
5. Go to the next task without asking, unless the task is marked STOP.

Keep going until a STOP task, a blocked task, or the end of milestone 3. Do not ask for permission between tasks.

## Scope for this version of the agent
Milestones 1, 2, 3, 3b and 3c only. Milestone 4 is closed. When you finish task 3c.5, write the closing report and stop.

## Keeping the main chat small
Long tool output fills the conversation and makes you slow and forgetful. So:
- Send long command output to a file under `work/` and read only the part you need.
- You may hand a self-contained piece of work to a subagent when it involves a lot of reading or trial and error: installing a tool, reading another project's source, tracking down a path. Give it the exact goal and the exact check, and ask for a short answer: what it did, the command that proves it, the result.
- Never accept a subagent's word that something works. Run the "Done when" check yourself afterwards.
- Subagents work one at a time in milestones 1 to 3. The tasks depend on each other, and two agents installing tools at once will collide.
- Subagents follow every rule in `AGENTS.md`, above all the rule that only `checker/` may read the foundry file.

## Git
- One branch per milestone: `m1-tools`, `m2-smoke`, `m3-incumbents`, `m3b-bench`, `m3c-gap`. When a milestone's last task is done, merge the branch into `main` locally and start the next branch from `main`.
- Everything stays on this machine. Never push, never add a remote, never open a pull request, never use the `gh` tool.
- Never change the commit identity.

## When something goes wrong
- Three honest attempts, then mark the task `BLOCKED` in `TASKS.md`, write what you tried in `PROGRESS.md`, commit, and stop.
- If a "Done when" check looks wrong or impossible, do not change it. Explain in `PROGRESS.md` and stop.
- If you are unsure whether something is in scope, it is not.

## How to report in chat
Keep chat messages short: task id, what happened, the number that matters. The detail goes in `PROGRESS.md` and `reports/`.

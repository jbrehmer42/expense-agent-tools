---
name: concur-create-report
description: "Use when creating a complete SAP Concur expense report for one trip from all receipts in receipts/ (in German 'Kostenabrechnung erstellen', 'Reisekostenabrechnung'). Plans the report, creates it, and coordinates concur-add-travel-allowance and concur-add-expense through sequential subagents. Never submits."
---

# Create a Complete Concur Expense Report

Turn all receipts in `receipts/` into one draft expense report. The main agent plans, creates the report, delegates entry work to subagents, and verifies the result.

## Boundaries

- Never click **Submit Report**. Only the user may submit a report.
- Run subagents **strictly one after another**, never in parallel. They share one browser page and one report.
- Do not select an approver. This remains a step for the user.
- Do not move, rename, or delete files in `receipts/`.

## 1. Plan

1. Read [profile/profile.md](../../../profile/profile.md) and all files in knowledge/ (e.g., `knowledge/expenses.md`). If the profile is missing, set it up with [setup-profile](../setup-profile/SKILL.md) first.
2. Extract text from all PDFs in `receipts/`; see [howto](../howto/SKILL.md).
3. Treat all receipts as one trip if the user does not say otherwise. Skim them only for trip facts. No detailed analysis needed; receipt subagents do that.
4. Present one minimal plan and collect all open questions in the same message:
   - **Report header**: name as destination plus trip month and year (e.g. `Hamburg 09-2026`), project from the profile.
   - **Receipts**: one line per file. Flag receipts that look unrelated to the trip (other dates or places) and ask whether to exclude them.
   - **Travel allowance**: times and destinations for outward and return journey, as well as paid meals (e.g. breakfast included on hotel invoice). Ask for missing facts. Include the allowance only if it applies to the trip; otherwise state "none".
   - **Business purpose**: a few words, reused for every comment. No semicolons or vertical bars.
5. Wait for the user's approval. After approval, run the whole plan without further prompts, except for errors.

## 2. Open or Create the Report

1. Open `https://eu2.concursolutions.com` and wait for the user to complete login, SSO, and MFA. Never ask for credentials.
2. Look for an unsubmitted report with the planned name. If one exists, ask whether to reuse it (e.g. to resume an aborted run).
3. Otherwise choose **Create Expense Report**, fill **Report Name**, **Project** (use **Search by Code**, select the exact code), then **Task** (the dropdown appears after the project is selected). Inspect other defaults without changing them. Click **Create Report**, not **Submit Report**.
4. Note the report name and number for the subagents.

## 3. Delegate to Subagents

Run the travel allowance subagent first (if planned), then one subagent per receipt. Wait for each reply before starting the next.

Each subagent prompt must contain:

- The report name and number. Open exactly this report.
- The skill to follow: `.agents/skills/concur-add-travel-allowance/SKILL.md` or `.agents/skills/concur-add-expense/SKILL.md`.
- Paths to `profile/profile.md` and `knowledge/expenses.md`, and the business purpose sentence.
- **Allowance subagent**: the approved allowance facts.
- **Receipt subagent**: the PDF path and its extracted `.txt` path. The subagent determines expense type, VAT rates, and splits itself.
- Duplicate check: before adding, inspect the expense list for entries already created from this receipt or itinerary. If found, report them instead of adding again.
- If unsure (VAT rate, expense type, missing fact): save nothing, cancel any unsaved draft, and return `needs-input` with the exact question.
- Reply in exactly this format:

```
status: done | needs-input | failed
entries:
- <type> | <date> | <vendor> | <gross amount> <currency> | VAT <rate> | Concur VAT <amount> | receipt attached yes/no
alerts: <open expense-level alerts, or none>
question/error: <exact question or error, or none>
draft left behind: no
```

For allowance entries, use one line per daily allowance with date and amount.

### Follow-up batch

Continue with the next receipt after `needs-input` or `failed`. When all subagents have replied, ask the user all collected questions in one message. Then start a fresh subagent for each affected receipt with the answers, again one after another.

If subagents cannot use the browser tools on the logged-in page, do the same steps in the main agent, in the same order.

## 4. Verify and Stop

1. Open the report and compare it with the plan and the subagent replies: expense count, totals per receipt, allowance entries, no duplicates, no missing receipts.
2. Open **View Alerts**.
3. Give a very short summary: report name and number, number of entries and total, a pointer to open alerts, excluded or unresolved receipts, and these user steps:
   - Select the approver and submit the report.
   - Clear `receipts/` before the next trip.

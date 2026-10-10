---
name: concur-add-expense
description: "Use when adding one expense (in German 'Ausgabe hinzufügen') to an existing SAP Concur expense report through the browser, including attaching a receipt, specifying VAT, and reviewing alerts. Use concur-add-travel-allowance for daily allowances."
---

# Add One Concur Expense

## Scope and prerequisites

Add one receipt-based expense to an existing report. Verified in the English Concur UI; fields and defaults can vary by company configuration.

**Important:** An expense can only track one tax rate. If the receipt in question contains multiple tax rates, it must be split into two separate expense entries in the same report. Each resulting expense entry should have its own VAT information accurately reflected. Attach the original receipt file for each expense.

## Boundaries

- Never click **Submit Report**. Only the user may submit a report.
- Inspect the existing expense list before adding an entry. Do not change, delete, or duplicate unrelated expenses or allowances.
- Do not add a new expense report unless the user explicitly instructs you to do so.

## Gather inputs first

- Read [expense knowledge](../../../knowledge/expenses.md) before processing receipts.
- Use PDFs in `receipts/`. Extract text with the existing tool set; see [howto](../howto/SKILL.md). Attach the original PDF, not the extracted text.
- For itineraries and daily allowances, use [concur-add-travel-allowance](../concur-add-travel-allowance/SKILL.md). Do not duplicate its procedures here.

## Open the existing report

Open the intended existing report, confirm its title and status, and inspect its expense list.

## Add expense information

1. Read the expense information from the text extracted from the receipt. Identify the total, currency, purchase/booking date, and any VAT information or document disclaimer.
2. Choose **Add Expense > Manually Create Expense**. In **Add Expense to Report**, select the correct type, e.g. 'train', in the list or search for it. The category might also appear under **Recently Used**.
3. Wait for **New Expense** to finish loading, then fill and verify the fields below.

| Field | Handling |
|-------|----------|
| Transaction Date | Use the receipt's purchase/booking date unless company policy or the user specifies another convention. |
| Vendor Name | Use the receipt's vendor, such as DB AG. |
| Location | Required city selection, e.g. hotel city or departure city for travel expenses. |
| From / To | Required departure and destination stations. |
| Payment Type | Follow profile rules and explicit payment facts. **Cash** includes personal funds and personal cards. |
| Amount / Currency | Always enter the gross amount from the receipt, including tax, once and in the receipt currency. Do not subtract tax or add it again. |
| Task | Required. Should be inherited. If not, check billability against the profile. |
| VAT | Required. Specify the rate so Concur can calculate tax from the gross amount; ask when uncertain. Accept Concur's calculated VAT, including rounding differences from the receipt. Do not manually correct or add comments for these rounding differences. |
| Business Purpose / Comment | Short business purpose. One sentence max. Do not use semicolons (`;`). |

## Itemize expenses (not always required)

**Itemization is required for some expense types.** Hotel expenses required it in the observed configuration. For other expense types, itemize only when Concur requires it.

1. For a hotel expense, enter the stay's **Date Range** and verify the **Nights** count before itemizing.
2. Open **Itemizations**. If Concur has already saved the expense and reports missing itemizations, complete them on that saved expense instead of creating another entry.
3. Use the hotel wizard to enter the gross nightly room charges. Choose **Same daily amount** when the nightly charges match, or **Different daily amount** when they differ. Do not add VAT again to amounts that already include it.
4. Add breakfast charges using the **Breakfast** itemization wizard and the appropriate recurrence. Trust the breakfast wizard's generated dates even when the receipt lists different dates. Do not override those dates or apply workarounds.
5. Save the itemizations and confirm that **Itemized** equals the expense's gross **Amount**, with **Remaining = 0.00**. Save the expense and review its alerts.

## Attach and save

1. In the expense's **Receipt** panel, use **Upload New Receipt**, drag-and-drop, or the associated file input through the browser tools. **Choose From Available Receipts** is an alternative.
2. If the tools cannot operate the native chooser, inspect the current file input and use Playwright `setInputFiles` with the original local PDF. An input with id `upload-file` was observed; inspect again instead of assuming that selector always exists. Do not use private APIs or modify application state directly.
3. Wait for **Loading Receipt Image** to finish. Confirm the expected filename and receipt viewer/removal control before saving.
4. Choose **Save Expense**, not **Submit Report**. If validation fails, read the exact message, fix only the affected field, and retry. Do not start another entry because a save failed.
5. Confirm **Expense saved**, the correct amount/date/vendor, and its **View receipt** control.
6. Open **View Alerts** and distinguish expense alerts from report warnings. Saving successfully does not mean a claim is complete or approved.

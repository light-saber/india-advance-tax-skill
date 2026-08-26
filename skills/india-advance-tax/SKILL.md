---
name: india-advance-tax
description: "Estimate and file India advance tax for salaried investors."
version: 0.1.0
author: Sachin Acharya, Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [India, Tax, Advance-Tax, 234C, Capital-Gains, RSU]
---

# India Advance Tax — Salaried Employees with Mutual Funds, Stocks, RSUs & US Stocks

Helps a resident Indian salaried employee decide whether advance tax is due, estimate the liability for the current financial year, and pay it on time to avoid interest under sections 234B and 234C. Covers salary (fully TDS-covered), equity/MF/stock capital gains, RSU (ESOP) income, and foreign (US) stock income, plus DTAA credit. **Not a substitute for a CA; verify rates against the current Union Budget before acting.**

## When to Use

- "Do I need to pay advance tax this year?"
- "When are advance tax installments due?"
- "How do I estimate advance tax on my mutual fund / stock / RSU gains?"
- "I made a big capital gain — do I owe advance tax now?"
- "How do I avoid interest under section 234C?"
- "My employer deducts TDS, so why do I owe advance tax?"
- "How do RSUs / US stocks affect my advance tax?"

**Don't use for:** final ITR filing itself (use a dedicated ITR skill), business/professional income advance tax, or TDS reconciliation.

## Prerequisites

- PAN + Aadhaar linked.
- Rough estimate of the current FY's income by head:
  - Salary (Form 16 basis, ~employer's TDS assumption is fine)
  - Capital gains realized year-to-date + expected (equity shares, equity/debt MFs, RSU/US-stock sales)
  - Interest income (savings + FD), dividend income if not TDS-covered
  - RSU/ESOP amounts vested this FY (FMV in INR at vest date)
- Form 26AS: knows how much TDS has already been deducted (salary, interest, dividend).
- Internet access to the Income Tax e-filing portal (https://www.incometax.gov.in).
- No credentials are stored; user logs into the portal themselves via browser.

## How to Run

Invoke by name, tell the skill the current FY (default to the live financial year) and gather estimates per the Procedure below.

```
/skill india-advance-tax
```

For the helper estimator: `python3 skills/india-advance-tax/scripts/advance_tax_estimator.py --help`

## Quick Reference

- **Advance tax threshold:** interest under 234B/234C applies only if your **estimated total tax liability net of TDS (and MST) is ≥ ₹10,000**. Under ₹10,000 → no advance tax, no penalty.
- **Estimate method:** tax on total income for the whole FY **minus TDS already deducted**, compared against the installment schedule by due date.
- **Installments (FY 2026-27, unchanged from prior years):**

| Due date | Advance tax payable (cumulative) |
|----------|----------------------------------|
| 15 June | at least 15% |
| 15 September | at least 45% |
| 15 December | at least 75% |
| 15 March | 100% |

- **Capital gains tax rates (FY 2026-27 / AY 2027-28, Budget-2026-unchanged):**
  - Equity LTCG (listed shares, equity MFs, >12 months): **12.5%** on gains **above ₹1,25,000** (STT paid).
  - Equity STCG: **20%**.
  - Debt MF / foreign equity LTCG (>24 months / foreign usually long-term): 12.5% (no indexation for post-23-Jul-2024 purchases).
  - US stock LTCG typically 24-month holding; report via Schedule FA/FSI in ITR with DTAA credit.
- **New regime slabs (FY 2026-27):** 0–4L nil | 4–8L 5% | 8–12L 10% | 12–16L 15% | 16–20L 20% | 20–24L 25% | above 24L 30%. Standard deduction ₹75,000; 87A rebate makes **income up to ~₹12L (new regime) tax-free**.
- **RSU/ESOP:** taxable as **salary** (perquisite u/s 17(2) / 56(2)(x)) at FMV on **vest date** — employer usually deducts TDS on it. The gain on subsequent **sale** is a separate capital gain.
- **Interest:** 234B = 1%/month on shortfall if total payment <90% of liability by 31 Mar; 234C = 1%/month for the missed/deferred installments (3 months each for the first three, 1 month for the last). Higher for amounts >₹1 crore.
- **Payment path:** Income Tax portal → e-Pay Tax → Challan 280 (Income-tax (Other than companies)) → advance tax (self) → 100/XX — 0021.

## Procedure

### Step 1 — Determine whether advance tax applies

1. Estimate your **total income** for the FY across all heads (salary + capital gains + interest + dividends + RSU-perquisite).
2. Estimate the **tax on that income** (pick regime; new-regime slabs + standard deduction are the common default).
3. Subtract **TDS already deducted or expected** (salary TDS, bank TDS on interest u/s 194A, dividend TDS u/s 194, MF redemption TDS, broker TDS on share sales u/s 194-IB/194-IB only if applicable — usually none for equities).
4. If the **remaining tax liability ≥ ₹10,000**, advance tax is legally due. Otherwise stop — no advance tax to pay.

> **Salaried trap:** employer TDS covers salary + RSU perquisite. But capital gains, interest, and dividends are usually **not** covered by salary TDS. If those push net liability past ₹10,000, advance tax is due even though you're salaried. Note: the ₹10,000 threshold is evaluated on the total tax net of TDS, not per-source (circular 2023 clarified intent to reduce small defaulters).

### Step 2 — Compute capital gains accurately (the common missed item)

For equity shares (broker) and mutual fund redemptions, compute realized gains FY-to-date using the cost basis:

```
Equity LTCG tax = 12.5% × max(0, (sale − cost) − ₹1,25,000 exemption)
Equity STCG tax = 20% × (sale − cost)
```

- The **₹1,25,000 LTCG exemption is a single annual pool across ALL equity sources combined** (broker + MFs), not per trade.
- Use your broker P&L and the consolidated MF (CAMS/Kfintech) statement; don't double count.
- Debt mutual funds / foreign (US) stocks: whoever, compute separately as they have different long-term holding periods and no 112A exemption (except listed equity ETFs under 112A).

### Step 3 — Handle RSU / ESOP / US stock income

- **RSU perquisite:** at **vest**, FMV in INR (SBI TT Buy rate on vest date) is added to salary. Employer usually deducts TDS on it via payroll → part of "salary TDS" above. If employer does NOT deduct (rare), it's an unpaid liability → advance tax relevant.
- **RSU/US-stock sale:** realized gain = sale value − cost basis (FMV at vest for RSU). Report as capital gain. Foreign tax withheld (e.g., US NRA) is claimed as a **foreign tax credit** via DTAA (US: Article 23) — file **Form 67**; it reduces Indian tax, so subtract it from your estimated net liability.
- **Foreign (US) stock dividends:** US 15-30% withholding; credit claimable via DTAA on the Indian return.

### Step 4 — Estimate the year-end liability and pay installments

Run the estimator script with your figures, or compute manually:

1. Total income → tax (new-regime slabs).
2. Add special-rate income tax (capital gains, RSU sale gains) at their rates.
3. Add surcharge if income >₹50L, then 4% health & education cess.
4. Subtract TDS + foreign tax credit + MST.
5. If net > ₹10,000 → schedule installments against the due-date table:
   - Hit **15% by 15 June**, **45% by 15 Sep**, **75% by 15 Dec**, **100% by 15 Mar** of the *paid-late-adjusted* cumulative liability.

### Step 5 — Pay on the portal

1. Login to https://www.incometax.gov.in → **e-Pay Tax** → **Challan 280**.
2. Tax Applicable: **Income-tax (Other than companies)** / Assessment Year = current AY.
3. Type of payment: **Advanced** → submit, net-bank/Card/BHIM.
4. Save the **BIN + CIN + Challan serial** for your records (matches Form 26AS / challan history).

### Step 6 — Verify no interest exposure

- Confirm cumulative payments sit **at or above** the 15/45/75/100% lines for the dates already passed.
- If you missed 15 June/15 Sep/15 Dec, pay the shortfall for the earliest missed installment to minimize 234C (interest runs on each missed installment for 3 months, the last for 1 month).

## Pitfalls

- **Employer TDS ≠ no advance tax.** Salary TDS rarely covers capital gains/interest/dividends. Recompute net liability; don't assume TDS covers everything.
- **The ₹10,000 threshold is on net tax**, after TDS, not per head and not on gross income.
- **Missed March RSU / end-of-year gains.** A large Q4 gain or a March RSU sale can create a 234C shortfall for the 15-Mar installment specifically — pay that by 15 Mar regardless of the year's earlier installments.
- **STCG vs LTCG rates differ sharply (20% vs 12.5% + exemption).** Getting the holding period wrong overestimates tax; under-estimating installments triggers 234C.
- **₹1.25L LTCG exemption is pooled** across all equity sources — don't apply it per broker or per MF.
- **Foreign tax credit needs Form 67** before ITR; without it you can't claim DTAA relief and will overpay. Estimate includes foreign tax paid.
- **Slab/rate drift.** Rates and the ₹1.25L exemption were unchanged by Budget 2026, but re-verify each Feb/Mar against the latest Union Budget before acting.
- **Interest calculation is strict.** 234C charges 1%/month even for day-level delays on cumulative thresholds — pay on or before the due date, not after.
- **Senior citizens (60+) without business income** are exempt from advance tax — check eligibility before automating.

## Verification

1. Portal shows the selected FY installments paid, each ≥ the required cumulative % by its due date.
2. Form 26AS / challan history lists your advance tax entries (type "Advance tax (self)").
3. Recompute estimated year-end liability and confirm cumulative paid ≥ 100% (or ≥ 90% for 234B with the rest covered before 31 Mar).
4. Estimator script returns a schedule identical to the manual table above within rounding.

## References

- `references/india-advance-tax-facts.md` — portal URLs, section numbers, exact rates, and edge cases.
- `scripts/advance_tax_estimator.py` — command-line estimator producing a per-installment payment schedule from your income estimates.
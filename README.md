# India Advance Tax — Agent Skill

A drop-in skill that lets an **AI agent** help a **salaried employee in India** decide whether advance tax is due, estimate the current-FY liability, and pay it on time to avoid interest under sections **234B / 234C**. Covers **mutual funds, listed stocks, RSUs/ESOPs, and US stocks**.

This README is written for agents: it is the runbook. Read it fully before acting. For the authoritative detail, load `skills/india-advance-tax/SKILL.md` and its `references/india-advance-tax-facts.md`.

---

## What this skill is for

The taxpayer's salary is usually fully covered by employer payroll TDS, but **capital gains, interest, and dividends are NOT** — so a salaried person can owe advance tax every year even though their employer deducts tax on salary. This skill estimates that non-payroll liability and schedules the payments so the taxpayer avoids 234C interest (missed installments) and 234B (underpaying by 31 March).

## What an agent should do (the workflow)

Follow this order. Do **not** jump to payment before verification.

### Step 1 — Confirm whether advance tax applies

1. Estimate total income for the current FY across all heads: salary (+ RSU perquisite at vest FMV), realized capital gains, interest, dividends.
2. Compute the tax on that income; choose the regime (new regime 115BAC is the default for salaried).
3. Subtract TDS already deducted or expected (salary TDS, bank interest TDS u/s 194A, dividend TDS u/s 194) and any foreign tax credit.
4. **Advance tax is due only if the net liability (tax − TDS − FTC) is ≥ ₹10,000.**

### Step 2 — Gather the source documents (Apr 1 to today)

Ask the user for, or pull from accessible storage, ALL of these so nothing is missed and nothing is double counted:

- **Broker taxpnl / P&L export** (equity delivery, intraday, MF, dividends, interest sheets)
- **Mutual fund gain statements** (CAMS / Kfintech / fund house) — separate from the broker
- **Foreign broker transaction summary** (e.g. US RSU plan: sales, dividends, foreign tax withheld)
- **Employer tax statement / Form 16** and latest payslips (salary, TDS, RSU perquisite)
- **Form 26AS** (confirms TDS actually claimed)

Convert PDFs / XLS / XLSX to text or read the sheets before computing.

### Step 3 — Classify every realized gain

| Item | Section | Rate |
|---|---|---|
| Listed Indian equity STCG (STT paid, ≤12 months) | 111A | 20% + surcharge + cess |
| Listed Indian equity / equity MF LTCG (STT paid) | 112A | 12.5% above ₹1,25,000 pooled exemption + surcharge + cess |
| Debt MF / gold ETF STCG | — | Slab rate |
| Debt MF / gold ETF LTCG (>24 months) | 112 | 12.5% (no indexation) |
| **Foreign (US) shares, ≤24 months** | — | **STCG at slab rate** (NOT 20%) |
| **Foreign (US) shares, >24 months** | 112 | **LTCG 12.5%, no ₹1.25L exemption** |
| Unlisted shares >24 months | 112 | 12.5% |

Critical rules:

- The **₹1,25,000 LTCG exemption is ONE annual pool across ALL equity sources combined** (broker + MFs + ETF). Never apply it per trade or per broker.
- **Foreign shares follow the 24-month rule.** The 12-month rule applies only to shares listed on a recognised Indian exchange. Under 24 months = STCG at slab rate.
- **FX discipline for foreign-share sales:** convert the USD cost basis at the **vest/acquisition-date SBI TT Buy rate** and the USD proceeds at the **sale-date SBI TT Buy rate**. Never reuse the vest rate for the sale — a common tax-software error that misstates the INR gain.
- Non-equity short-term capital losses set off against long-term capital gains; intraday/speculative losses do **not** set off against capital gains.
- Foreign tax withheld (US NRA, etc.) is a **foreign tax credit** under the India–US DTAA — requires **Form 67** filed before the ITR. Subtract the credit from net liability.

### Step 4 — Compute tax with the right surcharge tier

Surcharge is determined by **total income including salary**, not by the gains alone:

- ≤ ₹50L: nil
- ₹50L–₹1Cr: 10%
- ₹1Cr–₹2Cr: 15%

Then add 4% health & education cess. Effective rates at the 10% tier: 111A **22.88%**, 112A **14.30%**, slab **34.32%**.

### Step 5 — Verify before paying (recommended)

- Recompute from the raw statements, ideally with a second agent/tool, and compare per line. Investigate any disagreement beyond ~₹500.
- Confirm each gain appears in exactly ONE source (broker vs CAMS vs foreign custodian) — double counting is the classic multi-source error.
- If the mismatch is a classification question (STCG vs LTCG, foreign vs listed), resolve the holding period and section before paying.

### Step 6 — Schedule and pay

Cumulative installments due (unchanged for FY 2026-27):

| Due date | Cumulative % of estimated annual liability |
|---|---|
| 15 June | 15% |
| 15 September | 45% |
| 15 December | 75% |
| 15 March | 100% |

If a cutoff was missed, pay the earliest missed installment to stop 234C (1%/month). Payment:

1. https://www.incometax.gov.in → **e-Pay Tax** → **Challan 280**
2. Tax Applicable: **Income-tax (Other than companies)**; the newer portal labels the period **"Tax Year"** — pick the current FY (e.g. Tax Year 2026-27 = AY 2027-28)
3. Type of payment: **Advance tax**
4. **Prefer net banking, UPI (BHIM/PhonePe), or debit card — free.** Credit card costs ~0.8–1% + GST convenience fee and most issuers give no reward points on tax payments.
5. Save the **CIN / BIN / challan serial** — matches Form 26AS and is the proof of payment.

## Estimator

The CLI estimator takes income estimates and prints a per-installment schedule:

```bash
python3 skills/india-advance-tax/scripts/advance_tax_estimator.py \
  --salary 2500000 \
  --ru-perquisite 1000000 \
  --equity-stcg 100000 \
  --equity-ltcg 200000 \
  --foreign-share-stcg 50000 \
  --tds 300000 \
  --foreign-tax-credit 20000
```

Run `--help` for all flags. Note: `--foreign-share-stcg` is taxed at **slab rate** (added to ordinary income), while `--equity-stcg` uses the 20% special rate.

## Structure

```
skills/india-advance-tax/
  SKILL.md                          # full skill: when to use, procedure, pitfalls, verification
  references/india-advance-tax-facts.md   # rates, sections, edge cases
  scripts/advance_tax_estimator.py  # CLI estimator -> installment schedule
```

## Boundaries

- This skill computes **advance tax estimate + payment schedule** — it does **not** file the ITR, handle business/presumptive income (44AD/44ADA), or do TDS reconciliation.
- Not a substitute for a chartered accountant. Rates change with each Union Budget — **re-verify each Feb–Mar** against the latest Budget before paying.
- This is a **public, generic** skill: it must never be authored to contain, or be used to commit, personal identifiers (PAN, Aadhaar, account numbers, tax amounts with names, employer names). Work with user data only inside private/scratch space; keep the repo generic.

## Verified facts

Rates and the installment schedule were current as of **September 2026** (FY 2026-27 / AY 2027-28). Budget 2026 left the LTCG framework unchanged. Re-verify before each FY.

## License

MIT — see [LICENSE](LICENSE).
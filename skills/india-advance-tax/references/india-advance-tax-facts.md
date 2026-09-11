# India Advance Tax — Facts Reference

Verified as of September 2026. Rates/sections are re-checked against the Union Budget each Feb–Mar; Budget 2026 left the LTCG framework unchanged.

## Threshold & trigger

- Interest under 234B / 234C applies when **estimated tax liability net of TDS (and MST) is ≥ ₹10,000** in a FY.
- Estimate method: tax on total income for the whole FY **minus** TDS already deducted/expected.
- Salaried employees commonly owe advance tax even though payroll TDS covers salary, because **capital gains, interest, and unfunded RSU perquisites are outside salary TDS**.

## Installment schedule (cumulative % due by date)

| Due date | Advance tax payable (cumulative) |
|----------|----------------------------------|
| 15 June | at least 15% |
| 15 September | at least 45% |
| 15 December | at least 75% |
| 15 March | 100% |

- Any tax paid on or before 31 March counts as advance tax for the FY.
- Senior citizens (age 60+, no business/professional income) are fully exempt from advance tax.
- Presumptive business income (44AD/44ADA) pay 100% by 15 March (or single installment) — out of scope for the salaried case.

## Interest under sections 234B and 234C

- **234C** (deferment): 1% per month of the shortfall for each missed installment. First three installments carry interest for **3 months** each; the 15-March installment for **1 month**. For total tax > ₹1 crore, 234C applies if pay-in < an installment's cumulative amount (no 90% grace).
- **234B** (default of tax): 1% per month of the shortfall when cumulative payments by 31 March are **less than 90%** of the assessed tax. Interest accrues from 1 April of the AY to the actual payment date.

## Capital gains rates (FY 2026-27 / AY 2027-28)

| Asset | Holding period for LTCG | Rate |
|-------|-------------------------|------|
| Listed equity shares | > 12 months | LTCG 12.5% above ₹1,25,000 (STT paid) |
| Equity mutual funds / equity ETFs | > 12 months | LTCG 12.5% above ₹1,25,000 (STT paid) |
| Equity STCG | ≤ 12 months | 20% |
| Debt mutual funds | > 24 months | LTCG 12.5% (no indexation for post-23-Jul-2024 units) |
| Debt STCG | ≤ 24 months | Slab rate |
| **US / foreign shares (not listed on an Indian exchange)** | **> 24 months** | **LTCG 12.5% (no indexation, NO ₹1.25L exemption)** |
| **US / foreign shares — short term** | **≤ 24 months** | **Slab rate (NOT 20% equity STCG)** |
| Unlisted shares | > 24 months | 12.5% |

- The **₹1,25,000 LTCG exemption (s.112A) is pooled across all equity sources** for the FY — broker + MF combined, once.
- Holding period: 12 months for listed equity; **24 months for debt/foreign/unlisted assets**.
- Effective rates at the 10% surcharge tier (total income ₹50L–1Cr): 111A 22.88%, 112A 14.30%, slab 34.32%. At 15% surcharge (₹1Cr–2Cr): 23.92%, 14.95%, 35.88%.

## RSU / ESOP / US stock treatment

- **RSU vest** → salary perquisite u/s 17(2) / 56(2)(x), valued at **FMV in INR on the vest date** (SBI TT Buy rate). Employer payroll generally deducts TDS → covered by salary TDS.
- **RSU sale** → capital gain; cost basis = FMV at vest. **FX: convert cost at the vest-date SBI TT Buy rate and proceeds at the sale-date SBI TT Buy rate** — do not reuse the vest rate for the sale (a common tax-software error that misstates the INR gain).
- **US-source income & tax** → report in Schedule FSI/FA in ITR; US tax (including the 30%/15% NRA withholding on dividends) claimed as **foreign tax credit** under the India–US DTAA via **Form 67**. Subtract the credit from your estimated net liability.
- Holding period for foreign (US) shares: **24 months** for LTCG. Under 24 months → **STCG at slab rate** (30% + surcharge + cess).

## New-regime slab table (FY 2026-27 / AY 2027-28)

| Total income (new regime) | Rate |
|---------------------------|------|
| Up to ₹4,00,000 | Nil |
| ₹4,00,001 – ₹8,00,000 | 5% |
| ₹8,00,001 – ₹12,00,000 | 10% |
| ₹12,00,001 – ₹16,00,000 | 15% |
| ₹16,00,001 – ₹20,00,000 | 20% |
| ₹20,00,001 – ₹24,00,000 | 25% |
| Above ₹24,00,000 | 30% |

- Standard deduction (new regime): **₹75,000** for salaried.
- Rebate u/s 87A: NIL tax if **total income ≤ ₹12L** (new regime).
- Surcharge: 10% over ₹50L, 15% over ₹1Cr, higher above ₹2Cr.
- Health & education cess: **4%** on tax + surcharge.

## Payment path

1. https://www.incometax.gov.in → **e-Pay Tax**.
2. **Challan 280** → Income-tax (Other than companies) → assessment year = current AY.
3. Type of payment: **Advanced (advance tax)**.
4. Pay via net banking / debit card / BHIM UPI. Save BIN + CIN + challan serial.

## Key sections

- 234A (late return), 234B (default of advance tax), 234C (deferment of advance tax)
- 112A (equity LTCG), 111A (equity STCG), 112 (other LTCG)
- 87A (rebate), 115BAC (new regime)
- 194A (interest TDS), 194 (dividend TDS), 194A/194IB (property) — TDS that reduces net liability
- 90 / India–US DTAA Article 23 (foreign tax credit), Form 67

## Portal URLs

- E-filing / payment: https://www.incometax.gov.in
- Official FAQs on 234A/B/C: https://www.incometaxindia.gov.in/w/what-are-the-due-dates-for-payment-of-advance-tax-
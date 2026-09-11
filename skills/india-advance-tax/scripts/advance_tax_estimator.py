#!/usr/bin/env python3
"""Estimate India advance tax and produce a per-installment payment schedule.

For a resident Indian salaried employee with mutual funds, stocks, RSUs and
US stocks. Computes total current-FY tax across income heads, subtracts TDS
and foreign-tax credit, and maps the net liability onto the 15% / 45% / 75% /
100% cumulative installment schedule due 15 Jun / 15 Sep / 15 Dec / 15 Mar.

Pure CLI (no third-party deps). Educational estimate only — not tax advice.
Verify rates against the latest Union Budget / current slabs before paying.
"""

from __future__ import print_function

NA = 'N/A'

# Slabs: (upper bound inclusive, rate). FY 2026-27 / AY 2027-28 new regime.
NEW_REGIME_SLABS = [
    (4_00_000, 0.00),
    (8_00_000, 0.05),
    (12_00_000, 0.10),
    (16_00_000, 0.15),
    (20_00_000, 0.20),
    (24_00_000, 0.25),
    (float('inf'), 0.30),
]

STANDARD_DEDUCTION_NEW = 75_000
EQUITY_STCG_RATE = 0.20
EQUITY_LTCG_RATE = 0.125
EQUITY_LTCG_EXEMPT = 1_25_000
CESS = 0.04

INSTALLMENTS = [
    ("15 June", 0.15),
    ("15 September", 0.45),
    ("15 December", 0.75),
    ("15 March", 1.00),
]


def slab_tax(income):
    """Progressive slab tax (new regime) on total income."""
    tax = 0.0
    prev = 0
    for upper, rate in NEW_REGIME_SLABS:
        if income > prev:
            taxable_in_slab = min(income, upper) - prev
            tax += taxable_in_slab * rate
        prev = upper
        if income <= prev:
            break
    return tax


def income_tax(total_income, standard_deduction_applies=True):
    """Total tax on all ordinary income under the new regime, plus 87A rebate."""
    taxable = max(0.0, total_income - (STANDARD_DEDUCTION_NEW if standard_deduction_applies else 0))
    tax = slab_tax(taxable)
    # 87A rebate: NIL tax if total income <= 12L in new regime FY 2026-27.
    if total_income <= 12_00_000:
        tax = 0.0
    return tax


def special_rate_tax(equity_stcg, equity_ltcg):
    """Tax on capital gains taxed at special rates (Equity STCG/LTCG)."""
    tax = equity_stcg * EQUITY_STCG_RATE
    taxable_ltcg = max(0.0, equity_ltcg - EQUITY_LTCG_EXEMPT)
    tax += taxable_ltcg * EQUITY_LTCG_RATE
    return tax


def add_surcharge_cess(base_tax, total_income):
    """Surcharge (income > 50L tiers) + 4% health & education cess."""
    surcharge = 0.0
    if total_income > 50_00_000:
        cap = min(total_income, 1_00_00_000)
        rate = 0.10 if total_income <= 1_00_00_000 else 0.15
        surcharge = base_tax * (rate if total_income <= 1_00_00_000 else 0.15)
        if total_income > 1_00_00_000:
            # Above 1Cr: next tier 15% then 25% at 2Cr+; keep it simple & conservative at 15%.
            surcharge = base_tax * 0.15
    return (base_tax + surcharge) * (1 + CESS)


def schedule(net_liability):
    """Map net advance-tax liability onto cumulative installment deadlines."""
    return [(d, pct, net_liability * pct) for (d, pct) in INSTALLMENTS]


def main():
    import argparse
    p = argparse.ArgumentParser(
        description="Estimate India advance tax & produce an installment schedule.")
    p.add_argument("--salary", type=float, default=0,
                   help="Gross salary income for the FY (before standard deduction).")
    p.add_argument("--other-income", type=float, default=0,
                   help="Other ordinary income (interest, dividends w/o TDS, rent).")
    p.add_argument("--ru-perquisite", type=float, default=0,
                   help="RSU/ESOP perquisite value added to salary at vest (FMV INR).")
    p.add_argument("--equity-stcg", type=float, default=0,
                   help="Realized Indian-listed equity STCG (<=12 months, 111A @20%%).")
    p.add_argument("--equity-ltcg", type=float, default=0,
                   help="Realized equity LTCG (>12 months, 112A @12.5%% above pooled exemption).")
    p.add_argument("--foreign-share-stcg", type=float, default=0,
                   help="Realized STCG on foreign (US) shares held <24 months - taxed at slab rate, added to ordinary income.")
    p.add_argument("--tds", type=float, default=0,
                   help="TDS already deducted or expected (salary+interest+dividend).")
    p.add_argument("--foreign-tax-credit", type=float, default=0,
                   help="Foreign tax credit (DTAA, e.g. US tax withheld on RSU/US stock).")
    a = p.parse_args()

    # Foreign-share STCG is ordinary (slab-rate) income: NOT 111A/112A special rate.
    ordinary_income = a.salary + a.ru_perquisite + a.foreign_share_stcg + a.other_income
    base_tax = income_tax(ordinary_income)
    cg_tax = special_rate_tax(a.equity_stcg, a.equity_ltcg)
    total_before_cess = base_tax + cg_tax
    total_tax = add_surcharge_cess(total_before_cess, ordinary_income + a.equity_stcg + a.equity_ltcg)
    credits = a.tds + a.foreign_tax_credit
    net = max(0.0, total_tax - credits)

    print("=" * 62)
    print("INDIA ADVANCE TAX ESTIMATE (new regime, FY 2026-27 / AY 2027-28)")
    print("=" * 62)
    print("Ordinary income (salary + RSU perquisite + other):  {:>14,.0f}".format(ordinary_income))
    print("   slab tax (incl. std deduction & 87A rebate):     {:>14,.0f}".format(base_tax))
    print("Equity STCG tax @20%:                               {:>14,.0f}".format(a.equity_stcg * EQUITY_STCG_RATE))
    print("Equity LTCG tax @12.5% (>1.25L pooled exempt):      {:>14,.0f}".format(
        max(0.0, a.equity_ltcg - EQUITY_LTCG_EXEMPT) * EQUITY_LTCG_RATE))
    print("Total tax incl. surcharge + 4% cess:                {:>14,.0f}".format(total_tax))
    print("Less TDS + foreign tax credit:                      {:>14,.0f}".format(credits))
    print("NET advance-tax liability:                          {:>14,.0f}".format(net))
    print("-" * 62)
    if net < 10_000:
        print("  Net liability < INR 10,000 -> advance tax NOT required.")
        print("  No 234B/234C interest exposure for underpayment.")
        return
    print("  Advance tax IS required (net >= INR 10,000). Schedule:")
    for due, pct, amt in schedule(net):
        print("    {:<15} cumulative {:>4.0f}%  = INR {:>12,.0f}".format(due, pct * 100, amt))
    print("=" * 62)
    print("Note: pay on or before each due date. Missing an")
    print("installment triggers 234C (1%/month). Paying <90% of")
    print("full-year liability triggers 234B (1%/month). Verify")
    print("rates against the current Budget before paying.")


if __name__ == "__main__":
    main()
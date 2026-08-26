# India Advance Tax — Agent Skill

A reusable AI-agent skill that helps a **salaried employee in India** decide whether advance tax is due, estimate the current-FY liability, and pay it on time to avoid interest under sections 234B / 234C — covering **mutual funds, listed stocks, RSUs/ESOPs, and US stocks**.

The skill is a drop-in directory: clone it and point your agent (Hermes, Claude Code, Codex) at `skills/india-advance-tax/SKILL.md`.

## What it covers

- When advance tax applies (net tax after TDS ≥ ₹10,000) — including the **salaried trap** where payroll TDS covers salary but not capital gains/interest.
- The 15% / 45% / 75% / 100% cumulative installment schedule (15 Jun / 15 Sep / 15 Dec / 15 Mar).
- Capital-gains tax on equity shares, mutual funds, RSU sales, and US stocks (STCG 20%, LTCG 12.5% above a pooled ₹1.25L exemption).
- RSU/ESOP handling (FMV at vest as salary perquisite; sale = capital gain) and the India–US DTAA **foreign-tax-credit** claim via Form 67.
- Interest exposure (234B, 234C) and how to minimize it.
- A CLI estimator that turns your income estimates into a payment schedule.

## What it does **not** do

- File your ITR (this is **advance tax**, not return filing — see a dedicated ITR skill).
- Handle business/professional presumptive income.
- Replace a chartered accountant — rates and rules change with each Budget and high-stakes cases need professional review.

## Install & use

```bash
git clone <this-repo-url>
```

Point your agent at the skill:

```
/skill india-advance-tax
```

Or run the estimator directly:

```bash
python3 skills/india-advance-tax/scripts/advance_tax_estimator.py \
  --salary 2500000 \
  --equity-ltcg 400000 \
  --tds 300000 \
  --foreign-tax-credit 25000
```

## Structure

```
skills/india-advance-tax/
  SKILL.md                          # main skill (When to Use / Procedure / Pitfalls / Verification)
  references/india-advance-tax-facts.md   # rates, sections, edge cases
  scripts/advance_tax_estimator.py  # CLI estimator -> installment schedule
```

## Verified facts

Rates and the installment schedule are current as of **August 2026** (FY 2026-27 / AY 2027-28). Budget 2026 kept the LTCG framework unchanged. **Re-verify each Feb–Mar** against the latest Union Budget before paying — the skill's reference file flags this.

## License

MIT — see [LICENSE](LICENSE).
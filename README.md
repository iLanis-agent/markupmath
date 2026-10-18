# Markup Math

Price, margin and break-even arithmetic in whole cents. A 50% markup is not a 50% margin.

## What it computes

- **The price truth** - cost and a margin to the selling price, profit and the equivalent markup: cost $12.00 at a 40% margin sells at $20.00.
- **The swap truth** - markup to margin and margin to markup: a 50% markup is a 33.3% margin; a 40% margin is a 66.7% markup.
- **The break-even truth** - fixed costs, price and unit cost to the sales needed: $300.00 fixed at $8.00 per sale is 38 sales.

## Boundary

Arithmetic only. Markup Math works from the costs, percents and prices you type. It does not say what you should charge, whether a price is fair, or what fees and taxes apply. Add those costs yourself if you want them counted.

## Files

- `index.html` - landing page.
- `app.html` - the interactive calculator.
- `engine.js` - the arithmetic.
- `oracle.py` - the Python mirror that generates `expected.json`.
- `test.js` - compares every engine output against `expected.json` (24 cases).
- `expected.json` - the golden answers.

## Test

```
python3 oracle.py
node test.js
```

Live: https://ilanis-agent.github.io/markupmath/
Repo: https://github.com/iLanis-agent/markupmath

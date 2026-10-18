#!/usr/bin/env python3
# Markup Math oracle - mirrors engine.js.
import json, math

def _num(x):
    return str(int(x)) if x == int(x) else repr(x)

def _money(c):
    return f"${c // 100}.{c % 100:02d}"

def _tenths(x):
    t = math.floor(x * 10 + 0.5)
    return f"{t // 10}.{t % 10}"

def _cents(d, msg):
    if not math.isfinite(d) or d < 0 or d > 10000000:
        raise ValueError(msg)
    return math.floor(d * 100 + 0.5)

def price_truth(cost_d, margin):
    cost = _cents(cost_d, "cost must be between $0 and $10,000,000")
    if cost <= 0:
        raise ValueError("cost must be more than $0")
    if not math.isfinite(margin) or margin < 0 or margin >= 100:
        raise ValueError("margin must be 0 or more and under 100 percent")
    price = math.floor(cost * 100 / (100 - margin) + 0.5)
    profit = price - cost
    return (f"Cost {_money(cost)} at a {_num(margin)}% margin: sell at {_money(price)}, profit "
            f"{_money(profit)} (that is a {_tenths(profit * 100 / cost)}% markup).")

def swap_truth(kind, pct):
    if not math.isfinite(pct) or pct < 0:
        raise ValueError("percent must be 0 or more")
    if kind == "markup":
        return f"A {_num(pct)}% markup is a {_tenths(pct * 100 / (100 + pct))}% margin."
    if kind == "margin":
        if pct >= 100:
            raise ValueError("margin must be under 100 percent")
        return f"A {_num(pct)}% margin is a {_tenths(pct * 100 / (100 - pct))}% markup."
    raise ValueError("kind must be markup or margin")

def breakeven_truth(fixed_d, price_d, unit_d):
    fixed = _cents(fixed_d, "fixed costs must be between $0 and $10,000,000")
    price = _cents(price_d, "price must be between $0 and $10,000,000")
    unit = _cents(unit_d, "unit cost must be between $0 and $10,000,000")
    if fixed <= 0:
        raise ValueError("fixed costs must be more than $0")
    if price <= unit:
        raise ValueError("price must be above the unit cost")
    per = price - unit
    n = (fixed + per - 1) // per
    return (f"Fixed costs {_money(fixed)}, price {_money(price)}, unit cost {_money(unit)}: {_money(per)} "
            f"per sale, {n} {'sale' if n == 1 else 'sales'} to cover fixed costs ({n} x {_money(per)} = {_money(n * per)}).")

FNS = {"priceTruth": price_truth, "swapTruth": swap_truth, "breakevenTruth": breakeven_truth}

CASES = [
    ("priceTruth", [12, 40]), ("priceTruth", [12, 0]), ("priceTruth", [9.99, 25]),
    ("priceTruth", [0.5, 99.5]), ("priceTruth", [12, 100]), ("priceTruth", [0, 40]),
    ("priceTruth", [-1, 40]), ("priceTruth", [12, -5]),
    ("swapTruth", ["markup", 50]), ("swapTruth", ["markup", 100]), ("swapTruth", ["markup", 0]),
    ("swapTruth", ["margin", 40]), ("swapTruth", ["margin", 50]), ("swapTruth", ["margin", 99]),
    ("swapTruth", ["margin", 100]), ("swapTruth", ["markup", -5]), ("swapTruth", ["cost", 5]),
    ("breakevenTruth", [300, 20, 12]), ("breakevenTruth", [8, 20, 12]), ("breakevenTruth", [0.01, 20, 12]),
    ("breakevenTruth", [300, 12, 12]), ("breakevenTruth", [0, 20, 12]), ("breakevenTruth", [300, 20, -1]),
    ("breakevenTruth", [100, 3.5, 1.25]),
]

out = []
for fn, args in CASES:
    try:
        exp = FNS[fn](*args)
    except ValueError as e:
        exp = "ERR:" + str(e)
    out.append({"fn": fn, "args": args, "expected": exp})
with open("expected.json", "w") as f:
    json.dump(out, f, indent=1)
    f.write("\n")
print(len(out), "cases")

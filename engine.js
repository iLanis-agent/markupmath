// Markup Math engine - price, margin and break-even arithmetic in whole cents.
// Mirrored by oracle.py; keep the op order identical.

function _num(x) {
  return String(x);
}

function _p2(n) {
  return (n < 10 ? "0" : "") + n;
}

function _money(c) {
  return "$" + Math.floor(c / 100) + "." + _p2(c % 100);
}

function _tenths(x) {
  var t = Math.floor(x * 10 + 0.5);
  return Math.floor(t / 10) + "." + (t % 10);
}

function _cents(d, msg) {
  if (!isFinite(d) || d < 0 || d > 10000000) throw new Error(msg);
  return Math.floor(d * 100 + 0.5);
}

// The price truth: cost and the margin you want to the selling price.
function priceTruth(costDollars, marginPct) {
  var cost = _cents(costDollars, "cost must be between $0 and $10,000,000");
  if (cost <= 0) throw new Error("cost must be more than $0");
  if (!isFinite(marginPct) || marginPct < 0 || marginPct >= 100) throw new Error("margin must be 0 or more and under 100 percent");
  var price = Math.floor(cost * 100 / (100 - marginPct) + 0.5);
  var profit = price - cost;
  return "Cost " + _money(cost) + " at a " + _num(marginPct) + "% margin: sell at " + _money(price) + ", profit " +
    _money(profit) + " (that is a " + _tenths(profit * 100 / cost) + "% markup).";
}

// The swap truth: markup and margin are different percents of different bases.
function swapTruth(kind, pct) {
  if (!isFinite(pct) || pct < 0) throw new Error("percent must be 0 or more");
  if (kind === "markup") {
    return "A " + _num(pct) + "% markup is a " + _tenths(pct * 100 / (100 + pct)) + "% margin.";
  }
  if (kind === "margin") {
    if (pct >= 100) throw new Error("margin must be under 100 percent");
    return "A " + _num(pct) + "% margin is a " + _tenths(pct * 100 / (100 - pct)) + "% markup.";
  }
  throw new Error("kind must be markup or margin");
}

// The break-even truth: sales needed to cover fixed costs.
function breakevenTruth(fixedDollars, priceDollars, unitDollars) {
  var fixed = _cents(fixedDollars, "fixed costs must be between $0 and $10,000,000");
  var price = _cents(priceDollars, "price must be between $0 and $10,000,000");
  var unit = _cents(unitDollars, "unit cost must be between $0 and $10,000,000");
  if (fixed <= 0) throw new Error("fixed costs must be more than $0");
  if (price <= unit) throw new Error("price must be above the unit cost");
  var per = price - unit;
  var n = Math.floor((fixed + per - 1) / per);
  return "Fixed costs " + _money(fixed) + ", price " + _money(price) + ", unit cost " + _money(unit) + ": " + _money(per) +
    " per sale, " + n + " " + (n === 1 ? "sale" : "sales") + " to cover fixed costs (" + n + " x " + _money(per) + " = " + _money(n * per) + ").";
}

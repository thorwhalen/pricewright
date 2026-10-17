"""Render a :class:`~pricewright.spec.Card` as a Markdown rate card with its rationale.

The page answers, in order: what does each thing cost; is the card consistent; what
does travel add; how do the prices move with the day rate; and, offering by
offering, where every euro comes from. Prose lines are never hard-wrapped.
"""

from __future__ import annotations

import math
from typing import Iterable

from pricewright.model import Quote
from pricewright.spec import Card, Entry
from pricewright.travel import TravelPolicy

UNIT_LABEL = {
    "per_person": "per person",
    "per_group": "per group",
    "per_event": "per talk",
    "per_project": "per project",
    "per_month": "per month",
    "per_pack": "per pack",
    "per_session": "per session",
}


def _m(x: float, cur: str = "") -> str:
    if x is None or (isinstance(x, float) and math.isnan(x)):
        return "–"
    s = f"{x:,.0f}"
    return f"{s} {cur}".strip()


def _table(header: Iterable[str], rows: Iterable[Iterable]) -> str:
    header = list(header)
    out = ["| " + " | ".join(header) + " |", "|" + "---|" * len(header)]
    out += ["| " + " | ".join(str(c) for c in r) + " |" for r in rows]
    return "\n".join(out)


METRIC_LABEL = {
    "unit_price": "",
    "per_person_contact_hour": "/person-h",
    "per_contact_hour": "/contact h",
    "per_finished_minute": "/finished min",
}


def _market_cell(e: Entry, cur: str) -> str:
    p = e.position
    if p is None:
        return "no comparables"
    unit = METRIC_LABEL.get(e.market_value, "")
    return f"{p.verdict}; median {_m(p.median)}{unit} (n={p.n}, this at p{p.percentile * 100:.0f})"


def inputs_block(card: Card) -> str:
    rows = card.spec.get("inputs") or []
    if not rows:
        return ""
    return "\n".join(
        [
            "## Inputs you set (defaults used until you change them)",
            "",
            _table(("Input", "Default used", "Range seen / why"), [(r["input"], r["default"], r.get("why", "")) for r in rows]),
        ]
    )


def summary_table(card: Card) -> str:
    cur = card.rates.currency
    rows = []
    for e in card.entries:
        q, o = e.quote, e.quote.offering
        seats = f"{o.participants_expected}/{o.participants_cap}" if o.unit == "per_person" else (o.participants_cap or "")
        rows.append(
            (
                o.name,
                f"**{_m(q.unit_price, cur)}** {UNIT_LABEL.get(o.unit, o.unit)}",
                f"{o.contact_hours:g}" if o.contact_hours else "–",
                seats,
                f"{q.hours_total:.1f}",
                f"{q.prep_ratio:.1f}" if o.contact_hours else "–",
                _m(q.per_contact_hour),
                _m(q.per_person_contact_hour) if o.contact_hours and o.participants_expected > 1 else "–",
                f"{_m(q.effective_day)} ({q.rate_ratio:.0%})",
                _market_cell(e, cur),
            )
        )
    return _table(
        ("Offering", "Price", "Contact h", "Seats (exp./cap)", "Hours worked", "Hours per contact h", f"{cur} per contact h", f"{cur} per person-hour", "Effective day rate (of fully priced)", "Market"),
        rows,
    )


def findings_block(card: Card) -> str:
    if not card.findings:
        return "No inconsistencies found."
    icon = {"error": "**contradiction**", "warn": "worth a look", "info": "note"}
    return "\n".join(f"- {icon.get(f.severity, f.severity)} ({f.check}): {f.message}" for f in card.findings)


def travel_block(card: Card) -> str:
    if not card.travel:
        return ""
    cur = card.rates.currency
    pol: TravelPolicy = card.travel[0][1].policy
    hr = card.rates.hourly(pol.role)
    lines = [
        "## Travel and on-site add-on",
        "",
        "On-site prices above are *before travel*, and cover local work in the home city. Anything further adds one line, computed from the trip, never guessed:",
        "",
        "```",
        "travel = time fee + transport + hotel + per diem (+ local transport)",
        f"time fee per leg  = (door-to-door hours - {pol.free_hours_each_way:g} h free) x {_m(hr)} {cur}/h x {pol.time_rate_fraction:g}",
        f"                    on a travel-only day: at least {pol.travel_day_min_hours:g} h, at most {pol.travel_day_cap_fraction:g} x day rate",
        f"night before      = start before {pol.same_day_latest_start:g}:00 and one way > {pol.overnight_threshold_hours:g} h, or one way > {pol.max_travel_same_day_hours:g} h",
        f"night after       = one way > {pol.max_travel_same_day_hours:g} h; plus one night between consecutive days",
        f"hotel             = nights x up to {_m(pol.hotel_per_night)} {cur} per traveller (at cost)",
        f"per diem          = days away x {_m(pol.per_diem)} {cur} per traveller",
        f"transport         = at cost (economy / 2nd class rail), markup {pol.expense_markup:.0%}",
        "```",
        "",
    ]
    rows = []
    for name, tq in card.travel:
        t = tq.trip
        rows.append((name, f"{t.one_way_hours:g} h", t.travellers, t.working_days, tq.nights, _m(tq.time_fee), _m(tq.expenses), f"**{_m(tq.total, cur)}**"))
    lines.append(_table(("Scenario", "One way", "Travellers", "Days", "Nights", "Time fee", "Expenses (est.)", "Travel total"), rows))
    return "\n".join(lines)


def sensitivity_block(card: Card) -> str:
    if not card.sensitivity:
        return ""
    cur = card.rates.currency
    rates = sorted(card.sensitivity)
    rows = [(e.quote.offering.name, *(_m(card.sensitivity[r][e.id]) for r in rates)) for e in card.entries]
    return "\n".join(
        [
            "## How the card moves with the day rate",
            "",
            f"Every price is linear in the day rate (plus fixed third-party costs), so the whole card moves together. Prices in {cur}:",
            "",
            _table(("Offering", *(f"day rate {_m(r)}" for r in rates)), rows),
        ]
    )


def _waterfall(q: Quote) -> str:
    o, cur = q.offering, q.rates.currency
    rows = [
        ("labour", _m(q.labour_total)),
        ("third-party costs", _m(q.direct_total)),
        (f"contingency {o.contingency:.0%}", _m(q.contingency_amount)),
        (f"margin {o.margin:.0%} of price", _m(q.margin_amount)),
        (f"fees {o.fees_pct:.1%} + {o.fees_fixed_per_txn:g} per payment", _m(q.fees_amount)),
    ]
    if o.positioning != 1:
        rows.append((f"positioning x{o.positioning:g}", _m(q.revenue_raw - q.revenue_raw / o.positioning)))
    rows.append(("= revenue needed per run", _m(q.revenue_raw)))
    if o.unit == "per_person":
        rows.append((f"/ {o.participants_expected} expected paying seats", _m(q.unit_price_raw)))
    rows.append(("**printed price (rounded)**", f"**{_m(q.unit_price, cur)}**"))
    return _table(("Step", cur), rows)


def entry_block(e: Entry) -> str:
    q, o = e.quote, e.quote.offering
    cur = q.rates.currency
    out = [f"### {o.name}", ""]
    if e.rationale:
        out += [e.rationale.strip(), ""]
    labour = [(ln.label, ln.role, f"{ln.hours:.1f}", _m(ln.amount)) for ln in q.labour]
    out += [_table(("Work (per run)", "Role", "Hours", cur), labour), ""]
    if q.direct:
        out += [_table(("Third-party costs (per run)", cur), [(ln.label, _m(ln.amount)) for ln in q.direct]), ""]
    out += [_waterfall(q), ""]
    facts = [
        f"Hours worked per run: {q.hours_total:.1f}" + (f" for {o.contact_hours:g} contact hours ({q.prep_ratio:.1f} h per contact hour)" if o.contact_hours else ""),
        f"Effective rate after fees and costs: {_m(q.effective_hourly)} {cur}/h, {_m(q.effective_day)} {cur}/day ({q.rate_ratio:.0%} of fully priced)",
    ]
    be = q.break_even_participants
    if be is not None:
        facts.append(f"Seats needed at this price to pay the target day rate (plus contingency): {be:.1f} (expected {o.participants_expected}, cap {o.participants_cap})")
    if o.duration_s:
        facts.append(f"Per finished minute: {_m(q.per_finished_minute)} {cur}")
    if o.amortize_runs != 1:
        facts.append(f"Development amortised over {o.amortize_runs:g} runs")
    out += [f"- {f}" for f in facts]
    if o.includes:
        out.append(f"- Includes: {'; '.join(o.includes)}")
    if o.terms:
        out.append(f"- Terms: {'; '.join(o.terms)}")
    if e.position:
        p = e.position
        unit = METRIC_LABEL.get(e.market_value, "")
        out.append(f"- Market ({p.n} comparables, evidence-weighted, {cur}{unit}): p10 {_m(p.q10)}, median {_m(p.median)}, p90 {_m(p.q90)}; this offering is at p{p.percentile * 100:.0f}, {p.verdict}. Used: {', '.join(i for i, _ in p.used)}")
    return "\n".join(out)


def render(card: Card, *, intro: str = "") -> str:
    cur = card.rates.currency
    dr = ", ".join(f"{k} {_m(v, cur)}/day" for k, v in card.rates.day_rates.items())
    parts = [f"# {card.title}", ""]
    if intro:
        parts += [intro.strip(), ""]
    parts += [
        f"Target rates: {dr}, {card.rates.hours_per_day:g} h per day ({_m(card.rates.hourly(next(iter(card.rates.day_rates))))} {cur}/h). Every price below is computed from hours and costs at these rates, then rounded; the market column only says where the result sits.",
        "",
        inputs_block(card),
        "",
        "## The rate card",
        "",
        summary_table(card),
        "",
        "Effective day rate: what the offering earns per day of hours actually worked (prep, admin and feedback included), after fees and third-party costs, including the contingency and margin reserve. The percentage compares it with the fully priced rate (target x contingency / (1 - margin)); 100% means priced exactly by the model. On a consistent card these are equal, except where a positioning is chosen on purpose and shown.",
        "",
        "## Consistency checks",
        "",
        findings_block(card),
        "",
    ]
    for block in (travel_block(card), sensitivity_block(card)):
        if block:
            parts += [block, ""]
    parts += ["## Offering by offering", ""]
    for e in card.entries:
        parts += [entry_block(e), ""]
    return "\n".join(parts)

# Adding a specialty

A specialty is one module and one registration. Example: a new `consulting` specialty.

1. Create `pricewright/specialties/consulting.py` with:
   - a `DEFAULTS` dict: every number the templates use, with a comment saying where it came from;
   - templates: functions with keyword-only arguments and a `defaults: dict | None = None` parameter, returning an `Offering` built from `Effort` and `Cost` lines (never from a price);
   - `RESEARCH_NEEDS`: the evidence the expert should ask for or gather;
   - `MARKET`: for each template, a `MarketRef(metric, offerings, units, value)` saying which comparables are like-for-like;
   - `register(Specialty(name=..., title=..., description=..., templates=..., research_needs=..., market=..., defaults=...))`.
2. Add its name to `_BUILTIN` in `pricewright/specialties/__init__.py` (or call `register` from your own package; the registry is open).
3. Add a reference `references/<name>.md` to this skill: the effort model (what the hours are and their ratios), market structure, terms and the traps of that trade, and a row in the routing table of `SKILL.md`.
4. Add a test that the templates price, and that a known contradiction is flagged by `check_card`.

A specialty may add its own card checks (`checks=` on `Specialty`); `check_card(quotes, checks=DFLT_CHECKS + specialty.checks)`.

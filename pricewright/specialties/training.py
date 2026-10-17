"""Training, talks, workshops, courses and coaching.

Every template returns an :class:`~pricewright.base.Offering` built from hours and
costs, never from a price. The defaults are in :data:`DEFAULTS` (one place, so a
research refresh changes one dict) and any of them can be overridden per call.

The two ideas that make the card consistent:

- **the iceberg**: a delivered hour carries prep, development, admin and feedback
  hours. Development of reusable material is *amortised* over the runs you expect to
  sell, so a talk given once carries all its prep and a workshop run ten times
  carries a tenth of it. That, not a market median, is why a talk costs more per
  stage hour than a workshop day, and by how much;
- **one rate**: every template prices hours at the same day rate, so the effective
  rate per hour worked comes out the same across the card unless a deliberate
  ``positioning`` says otherwise (and the card check shows it).

On-site work is priced *before travel*; travel is a separate line
(:func:`pricewright.travel.travel_addon`), as the trade quotes it.
"""

from __future__ import annotations

from pricewright.base import Cost, Effort, Offering
from pricewright.ratecard import Finding, _families
from pricewright.specialties import MarketRef, Specialty, register

DEFAULTS: dict[str, float] = {
    # Sources: research packet training-effort-and-market.md (2026-10-17), section 1.
    # development of reusable material, hours per delivered hour (amortised over runs)
    "dev_ratio_talk": 40.0,  # new 60-min talk ~40 h (practitioner 20:1 to 60:1)
    "dev_ratio_workshop": 8.0,  # new hands-on day ~56 h (practitioner 3:1 to 20:1; full-team ILT 43:1)
    "dev_ratio_course": 8.0,  # first run of a live cohort, per live hour (5:1 to 15:1)
    "dev_ratio_series": 6.0,  # live online sessions (vILT ~0.75 x in-person)
    "runs_talk": 10,  # a signature talk is given many times
    "runs_workshop": 6,
    "runs_course": 4,
    "runs_series": 4,
    # per-run hours
    "talk_customisation_hours": 4.0,  # tailoring an existing talk: 4 to 12 h (6-10 h for a keynote)
    "client_admin_hours": 1.5,  # call with the organiser, emails, invoice
    "open_admin_hours_per_run": 4.0,  # listing, registrations, reminders, refunds
    "session_tech_hours": 0.5,  # online: rehearsal, links, recording, per facilitator per session
    "onsite_setup_hours": 1.0,  # on site: arrive early, AV, room, per facilitator
    "local_commute_hours": 1.0,  # round trip in the home city, per person, absorbed in the fee
    "facilitator_ratio": 12,  # one lead up to 12 hands-on participants, a second above
    # money
    "open_fees_pct": 0.03,  # Stripe EEA 1.5% + 0.25 to international 3.15% + 0.25, sold on the studio's own site
    "open_fees_fixed": 0.25,  # per transaction
    "credits_per_participant": 20.0,  # generation credits for a hands-on day (the studio's accounts)
    "materials_per_participant": 5.0,
    "venue_per_day": 650.0,  # Paris 15-20 people ~605/day; London ~450 GBP
    "catering_per_participant_day": 35.0,
    "marketing_per_open_run": 150.0,
    "contingency": 0.10,
    "margin": 0.10,
}


def _d(d: dict, key: str, value):
    return d[key] if value is None else value


def _facilitators(cap: int, ratio: float, n: int | None) -> int:
    return n if n is not None else max(1, -(-cap // int(ratio)))  # ceil


def talk(
    *,
    delivery: str = "online",
    minutes: float = 60,
    qa_minutes: float | None = None,
    speakers: int = 1,
    dev_ratio: float | None = None,
    runs: float | None = None,
    customisation_hours: float | None = None,
    admin_hours: float | None = None,
    onsite_presence_hours: float = 1.0,
    name: str | None = None,
    defaults: dict | None = None,
    **overrides,
) -> Offering:
    """A talk or webinar for one organiser's audience; priced per event, any audience size."""
    D = {**DEFAULTS, **(defaults or {})}
    qa = qa_minutes if qa_minutes is not None else (15 if delivery == "online" else 30)
    contact = (minutes + qa) / 60
    dev = _d(D, "dev_ratio_talk", dev_ratio) * minutes / 60
    eff = [
        Effort("talk development (amortised)", dev, per="development", kind="development"),
        Effort("customisation to the audience", _d(D, "talk_customisation_hours", customisation_hours), kind="prep"),
        Effort("organiser call, emails, invoice", _d(D, "client_admin_hours", admin_hours), kind="admin"),
        Effort(f"delivery, {speakers} speaker(s)", contact * speakers),
    ]
    if delivery == "online":
        eff.append(Effort("tech rehearsal", D["session_tech_hours"] * speakers, kind="prep"))
    else:
        eff += [
            Effort("on-site setup, AV check", D["onsite_setup_hours"] * speakers, kind="prep"),
            Effort("presence before and after", onsite_presence_hours * speakers),
            Effort("local commute", D["local_commute_hours"] * speakers, kind="travel"),
        ]
    return Offering(
        name=name or f"Talk, {delivery}",
        specialty="training",
        unit="per_event",
        delivery=delivery,
        contact_hours=contact,
        efforts=tuple(eff),
        amortize_runs=_d(D, "runs_talk", runs),
        contingency=0.05,
        margin=D["margin"],
        family="talk",
        includes=(f"{minutes:g} min talk + {qa:g} min Q&A", "any audience size"),
        **overrides,
    )


def open_workshop(
    *,
    delivery: str = "onsite",
    contact_hours: float = 7.0,
    cap: int = 16,
    expected: int = 10,
    facilitators: int | None = None,
    dev_ratio: float | None = None,
    runs: float | None = None,
    prep_hours_per_facilitator: float = 2.0,
    feedback_hours_per_participant: float = 0.5,
    venue: float | None = None,
    name: str | None = None,
    defaults: dict | None = None,
    **overrides,
) -> Offering:
    """An open-enrolment hands-on workshop, priced per seat at the *expected* fill."""
    D = {**DEFAULTS, **(defaults or {})}
    fac = _facilitators(cap, D["facilitator_ratio"], facilitators)
    sessions = 1 if delivery == "onsite" else max(1, round(contact_hours / 3.5))
    eff = [
        Effort("workshop development (amortised)", _d(D, "dev_ratio_workshop", dev_ratio) * contact_hours, per="development", kind="development"),
        Effort(f"prep, {fac} facilitator(s)", prep_hours_per_facilitator * fac, kind="prep"),
        Effort("listing, registrations, reminders", D["open_admin_hours_per_run"], kind="admin"),
        Effort(f"delivery, {fac} facilitator(s)", contact_hours * fac),
        Effort("pre-work review and follow-up", feedback_hours_per_participant, per="participant", kind="feedback"),
    ]
    costs = [
        Cost("generation credits", D["credits_per_participant"], per="participant", kind="credits"),
        Cost("marketing", D["marketing_per_open_run"], kind="marketing"),
    ]
    if delivery == "onsite":
        eff += [
            Effort("room setup and tear-down", D["onsite_setup_hours"] * fac, kind="prep"),
            Effort("local commute", D["local_commute_hours"] * fac, kind="travel"),
        ]
        costs += [
            Cost("venue", _d(D, "venue_per_day", venue) * contact_hours / 7, kind="venue"),
            Cost("lunch and coffee", D["catering_per_participant_day"] * contact_hours / 7, per="participant", kind="catering"),
            Cost("printed materials", D["materials_per_participant"], per="participant"),
        ]
    else:
        eff.append(Effort("tech checks", D["session_tech_hours"] * fac * sessions, kind="prep"))
    return Offering(
        name=name or f"Open workshop, {delivery}",
        specialty="training",
        unit="per_person",
        delivery=delivery,
        contact_hours=contact_hours,
        participants_expected=expected,
        participants_cap=cap,
        efforts=tuple(eff),
        costs=tuple(costs),
        amortize_runs=_d(D, "runs_workshop", runs),
        fees_pct=D["open_fees_pct"],
        fees_fixed_per_txn=D["open_fees_fixed"],
        contingency=D["contingency"],
        margin=D["margin"],
        family="workshop",
        **overrides,
    )


def private_workshop(
    *,
    delivery: str = "onsite",
    contact_hours: float = 7.0,
    group: int = 16,
    facilitators: int | None = None,
    dev_ratio: float | None = None,
    runs: float | None = None,
    customisation_hours: float = 4.0,
    discovery_hours: float = 2.0,
    prep_hours_per_facilitator: float = 1.5,
    feedback_hours_per_participant: float = 0.25,
    name: str | None = None,
    defaults: dict | None = None,
    **overrides,
) -> Offering:
    """A closed workshop for one client's team, at their office or online; priced per group."""
    D = {**DEFAULTS, **(defaults or {})}
    fac = _facilitators(group, D["facilitator_ratio"], facilitators)
    sessions = 1 if delivery == "onsite" else max(1, round(contact_hours / 3.5))
    eff = [
        Effort("workshop development (amortised)", _d(D, "dev_ratio_workshop", dev_ratio) * contact_hours, per="development", kind="development"),
        Effort("discovery call and scoping", discovery_hours, kind="admin"),
        Effort("customisation to the client's material", customisation_hours, kind="prep"),
        Effort(f"prep, {fac} facilitator(s)", prep_hours_per_facilitator * fac, kind="prep"),
        Effort(f"delivery, {fac} facilitator(s)", contact_hours * fac),
        Effort("pre-work review", feedback_hours_per_participant, per="participant", kind="feedback"),
        Effort("invoice and follow-up", 0.5, kind="admin"),
    ]
    costs = [
        Cost("generation credits", D["credits_per_participant"] * contact_hours / 7, per="participant", kind="credits"),
    ]
    if delivery == "onsite":
        eff += [
            Effort("room setup", D["onsite_setup_hours"] * fac, kind="prep"),
            Effort("local commute", D["local_commute_hours"] * fac, kind="travel"),
        ]
        costs.append(Cost("printed materials", D["materials_per_participant"], per="participant"))
    else:
        eff.append(Effort(f"tech checks, {sessions} session(s)", D["session_tech_hours"] * fac * sessions, kind="prep"))
    return Offering(
        name=name or f"Private workshop, {delivery}",
        specialty="training",
        unit="per_group",
        delivery=delivery,
        contact_hours=contact_hours,
        participants_expected=group,
        participants_cap=group,
        efforts=tuple(eff),
        costs=tuple(costs),
        amortize_runs=_d(D, "runs_workshop", runs),
        contingency=D["contingency"],
        margin=D["margin"],
        family="workshop",
        **overrides,
    )


def online_course(
    *,
    weeks: int = 4,
    session_hours: float = 3.0,
    office_hours_per_week: float = 1.0,
    cap: int = 12,
    expected: int = 8,
    lead_facilitators: int = 1,
    second_facilitator_share: float = 0.5,
    dev_ratio: float | None = None,
    runs: float | None = None,
    prep_hours_per_session: float = 1.5,
    feedback_hours_per_participant: float = 1.5,
    platform_per_run: float = 40.0,
    private: bool = False,
    name: str | None = None,
    defaults: dict | None = None,
    **overrides,
) -> Offering:
    """A live online cohort: weekly sessions, office hours, feedback on each participant's project."""
    D = {**DEFAULTS, **(defaults or {})}
    live = weeks * session_hours
    contact = live + weeks * office_hours_per_week
    eff = [
        Effort("course development (amortised)", _d(D, "dev_ratio_course", dev_ratio) * live, per="development", kind="development"),
        Effort("session prep", prep_hours_per_session * weeks, kind="prep"),
        Effort("enrolment, platform, emails", D["open_admin_hours_per_run"] * 1.5, kind="admin"),
        Effort("live sessions, lead", live * lead_facilitators),
        Effort("live sessions, second facilitator", live * second_facilitator_share),
        Effort("office hours", weeks * office_hours_per_week),
        Effort("tech checks", D["session_tech_hours"] * weeks, kind="prep"),
        Effort("feedback on each project", feedback_hours_per_participant, per="participant", kind="feedback"),
    ]
    costs = [Cost("video platform and course pages", platform_per_run, kind="tools")]
    if private:  # one client's team: a scoping call replaces marketing and open enrolment
        eff = [e for e in eff if e.kind != "admin"] + [Effort("scoping call, invoice", 2.5, kind="admin")]
        expected = cap
    else:
        costs.append(Cost("marketing", D["marketing_per_open_run"] * 2, kind="marketing"))
    return Offering(
        name=name or f"{'Private' if private else 'Online'} course, {weeks} weeks",
        specialty="training",
        unit="per_group" if private else "per_person",
        delivery="online",
        contact_hours=contact,
        participants_expected=expected,
        participants_cap=cap,
        efforts=tuple(eff),
        costs=tuple(costs),
        amortize_runs=_d(D, "runs_course", runs),
        fees_pct=0.0 if private else D["open_fees_pct"],
        fees_fixed_per_txn=0.0 if private else D["open_fees_fixed"],
        contingency=D["contingency"],
        margin=D["margin"],
        family="course",
        includes=(f"{weeks} x {session_hours:g} h live + {weeks} x {office_hours_per_week:g} h office hours", "recordings"),
        **overrides,
    )


def series(
    *,
    sessions: int = 3,
    session_hours: float = 2.0,
    cap: int = 12,
    expected: int = 8,
    dev_ratio: float | None = None,
    runs: float | None = None,
    prep_hours_per_session: float = 1.0,
    feedback_hours_per_participant: float = 0.5,
    name: str | None = None,
    defaults: dict | None = None,
    **overrides,
) -> Offering:
    """A short live online series (e.g. 3 x 2 h) led by one founder."""
    D = {**DEFAULTS, **(defaults or {})}
    contact = sessions * session_hours
    eff = [
        Effort("series development (amortised)", _d(D, "dev_ratio_series", dev_ratio) * contact, per="development", kind="development"),
        Effort("session prep", prep_hours_per_session * sessions, kind="prep"),
        Effort("enrolment and emails", D["open_admin_hours_per_run"] * 0.75, kind="admin"),
        Effort("live sessions", contact),
        Effort("tech checks", D["session_tech_hours"] * sessions, kind="prep"),
        Effort("feedback between sessions", feedback_hours_per_participant, per="participant", kind="feedback"),
    ]
    costs = [Cost("marketing", D["marketing_per_open_run"], kind="marketing")]
    return Offering(
        name=name or f"Online series, {sessions} x {session_hours:g} h",
        specialty="training",
        unit="per_person",
        delivery="online",
        contact_hours=contact,
        participants_expected=expected,
        participants_cap=cap,
        efforts=tuple(eff),
        costs=tuple(costs),
        amortize_runs=_d(D, "runs_series", runs),
        fees_pct=D["open_fees_pct"],
        fees_fixed_per_txn=D["open_fees_fixed"],
        contingency=D["contingency"],
        margin=D["margin"],
        family="series",
        **overrides,
    )


def private_series(*, sessions: int = 3, session_hours: float = 2.0, group: int = 12, name: str | None = None, defaults: dict | None = None, **overrides) -> Offering:
    """The series for one client's team: no marketing or enrolment, a scoping call instead."""
    D = {**DEFAULTS, **(defaults or {})}
    contact = sessions * session_hours
    eff = [
        Effort("series development (amortised)", D["dev_ratio_series"] * contact, per="development", kind="development"),
        Effort("scoping call", 1.5, kind="admin"),
        Effort("customisation", 3.0, kind="prep"),
        Effort("session prep", 1.0 * sessions, kind="prep"),
        Effort("live sessions", contact),
        Effort("tech checks", D["session_tech_hours"] * sessions, kind="prep"),
        Effort("feedback between sessions", 0.5, per="participant", kind="feedback"),
        Effort("invoice", 0.5, kind="admin"),
    ]
    return Offering(
        name=name or f"Private series, {sessions} x {session_hours:g} h",
        specialty="training",
        unit="per_group",
        delivery="online",
        contact_hours=contact,
        participants_expected=group,
        participants_cap=group,
        efforts=tuple(eff),
        amortize_runs=D["runs_series"],
        contingency=D["contingency"],
        margin=D["margin"],
        family="series",
        **overrides,
    )


def coaching(
    *,
    sessions: int = 1,
    session_hours: float = 1.0,
    prep_hours_per_session: float = 0.5,
    admin_hours: float = 0.25,
    name: str | None = None,
    defaults: dict | None = None,
    **overrides,
) -> Offering:
    """1:1 coaching, single session or a pack (one admin overhead for the whole pack)."""
    D = {**DEFAULTS, **(defaults or {})}
    eff = [
        Effort("sessions", sessions * session_hours),
        Effort("prep and notes", sessions * prep_hours_per_session, kind="prep"),
        Effort("scheduling and invoice", admin_hours * (1 if sessions == 1 else 2), kind="admin"),
    ]
    return Offering(
        name=name or ("1:1 coaching, single" if sessions == 1 else f"1:1 coaching, pack of {sessions}"),
        specialty="training",
        unit="per_session" if sessions == 1 else "per_pack",
        delivery="online",
        contact_hours=sessions * session_hours,
        efforts=tuple(eff),
        fees_pct=0.03,
        fees_fixed_per_txn=0.25,
        contingency=0.0,
        margin=D["margin"],
        family="coaching",
        **overrides,
    )


def team_programme(
    *,
    workshop_days: int = 2,
    audit_days: float = 1.0,
    playbook_days: float = 3.0,
    checkins: int = 4,
    group: int = 16,
    project_management_share: float = 0.10,
    name: str | None = None,
    defaults: dict | None = None,
    **overrides,
) -> Offering:
    """Consulting + training for one team, composed from the other templates' effort.

    Audit (both founders on site), ``workshop_days`` private days, a written playbook,
    remote check-ins and a review at day 30, plus project management on top.
    """
    D = {**DEFAULTS, **(defaults or {})}
    day = private_workshop(group=group, defaults=defaults)
    eff = [e for _ in range(workshop_days) for e in day.efforts if e.per != "development"]
    eff = [Effort(f"workshop day: {e.label}", e.hours, e.role, e.per, e.kind) for e in eff]
    eff += [
        Effort("workshop development share", D["dev_ratio_workshop"] * 7 * workshop_days, per="development", kind="development"),
        Effort("audit: interviews and observation, 2 founders", audit_days * 7 * 2, kind="delivery"),
        Effort("audit: prep and write-up", 6.0 * audit_days, kind="prep"),
        Effort("playbook writing", playbook_days * 7, kind="production"),
        Effort("remote check-ins", 0.75 * checkins, kind="delivery"),
        Effort("day-30 review, 2 founders + prep", 1.5 * 2 + 2, kind="delivery"),
    ]
    pm = project_management_share * sum(e.hours * (group if e.per == "participant" else 1) for e in eff if e.per != "development")
    eff.append(Effort("project management", pm, kind="admin"))
    return Offering(
        name=name or "Team programme",
        specialty="training",
        unit="per_project",
        delivery="onsite",
        contact_hours=7 * workshop_days + 7 * audit_days * 2 + 0.75 * checkins + 1.5,
        participants_expected=group,
        participants_cap=group,
        efforts=tuple(eff),
        costs=tuple(c.__class__(c.label, c.amount * workshop_days, c.per, c.kind, c.markup) for c in day.costs),
        amortize_runs=D["runs_workshop"],
        contingency=0.15,
        margin=D["margin"],
        family="programme",
        **overrides,
    )


def private_to_seat_ratio(quotes, *, band: tuple[float, float] = (3.0, 10.0)):
    """A private day costs 3-10 open seats of the same day (observed 3.4-10, typically 4-6; training research 1e).

    Above the band the private day is dear, or the open seat cheap, for the buyer who compares them.
    """
    for fam, qs in _families(quotes).items():
        opens = [q for q in qs if q.offering.unit == "per_person"]
        privs = [q for q in qs if q.offering.unit == "per_group"]
        for o in opens:
            for p in privs:
                if p.offering.delivery != o.offering.delivery or p.offering.contact_hours != o.offering.contact_hours:
                    continue
                r = p.unit_price / o.unit_price
                if not band[0] <= r <= band[1]:
                    yield Finding(
                        "private_to_seat_ratio",
                        "warn",
                        f"{p.offering.name} costs {r:.1f} open seats of {o.offering.name}; the market's range is {band[0]:g}-{band[1]:g}",
                        (p.offering.name, o.offering.name),
                    )


RESEARCH_NEEDS = (
    "Talk and webinar fees for non-celebrity speakers in the target region, online and on site, with talk length.",
    "Open-enrolment one-day hands-on workshop prices per person, with contact hours and group size.",
    "Private (in-company) day and half-day prices, with group size, on site and online.",
    "Live online cohort courses on the topic: price, weeks, live contact hours, cohort size.",
    "Short live series (2-8 h total) on the topic: price and hours.",
    "1:1 coaching rates for practitioners in the field, single and packs.",
    "Day rates of trainers and consultants in the region (to sanity-check the founders' day rate).",
    "Development-time ratios (hours of prep per delivered hour) for the formats offered.",
)

MARKET = {
    "talk": MarketRef("as_is", ("talk", "webinar", "keynote"), units=("per_event", "per_group"), value="unit_price"),
    "open_workshop": MarketRef("per_person_contact_hour", ("open_workshop_day", "open_workshop", "workshop")),
    "private_workshop": MarketRef("as_is", ("private_day",), units=("per_group",), value="unit_price"),
    "online_course": MarketRef("per_person_contact_hour", ("online_cohort", "course")),
    "series": MarketRef("per_person_contact_hour", ("series", "short_course", "online_cohort")),
    "private_series": MarketRef("per_contact_hour", ("private_day", "half_day", "private_session"), value="per_contact_hour"),
    "coaching": MarketRef("per_contact_hour", ("coaching",), value="per_contact_hour"),
}

SPECIALTY = register(
    Specialty(
        name="training",
        title="Training, talks, workshops, courses and coaching",
        description=__doc__.split("\n\n")[0],
        templates={
            "talk": talk,
            "open_workshop": open_workshop,
            "private_workshop": private_workshop,
            "online_course": online_course,
            "series": series,
            "private_series": private_series,
            "coaching": coaching,
            "team_programme": team_programme,
        },
        research_needs=RESEARCH_NEEDS,
        market=MARKET,
        checks=(private_to_seat_ratio,),
        defaults=DEFAULTS,
    )
)

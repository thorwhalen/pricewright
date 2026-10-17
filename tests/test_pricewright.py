"""Behavioural tests: the model's arithmetic, the travel rules, the card checks, the spec round trip."""

import math

import pytest

from pricewright import (
    Effort,
    Offering,
    Rates,
    Trip,
    TravelPolicy,
    build_card,
    check_card,
    price,
    render,
    specialties,
    travel_addon,
)
from pricewright.research import Comparable, position
from pricewright.rounding import no_round
from pricewright.specialties.training import open_workshop, private_workshop, talk

R = Rates({"founder": 700})  # 100 per hour


def test_price_is_hours_times_rate_then_contingency_margin_fees():
    o = Offering("x", "training", "per_group", efforts=(Effort("w", 10),), contingency=0.1, margin=0.2, fees_pct=0.05)
    q = price(o, R, rounder=no_round)
    assert q.unit_price == pytest.approx(1000 * 1.1 / 0.8 / 0.95)


def test_effective_rate_meets_target_without_margin_or_rounding():
    o = Offering("x", "training", "per_group", efforts=(Effort("w", 10),), contingency=0, margin=0)
    q = price(o, R, rounder=no_round)
    assert q.effective_hourly == pytest.approx(q.target_hourly)


def test_development_is_amortised_and_participant_effort_scales():
    o = Offering(
        "x", "training", "per_person", participants_expected=4,
        efforts=(Effort("dev", 40, per="development"), Effort("fb", 1, per="participant")),
        amortize_runs=10, contingency=0, margin=0,
    )
    q = price(o, R, rounder=no_round)
    assert q.hours_total == pytest.approx(4 + 4)
    assert q.unit_price == pytest.approx(800 / 4)


def test_break_even_seats_below_expected_when_margin_positive():
    q = price(open_workshop(), R)
    assert q.break_even_participants < q.offering.participants_expected


def test_invalid_margin_raises_with_name():
    with pytest.raises(ValueError, match="bad"):
        Offering("bad", "training", "per_group", margin=1.2)


def test_travel_local_is_free_and_far_needs_nights():
    assert travel_addon(Trip(one_way_hours=0.75), rates=R).total == 0
    far = travel_addon(Trip(one_way_hours=5, transport_round_trip=200, working_days=1), rates=R)
    assert far.nights == 2 and far.time_fee > 0 and far.expenses > 200


def test_travel_only_day_is_capped_at_fraction_of_day_rate():
    q = travel_addon(Trip(one_way_hours=7.9), rates=R, policy=TravelPolicy(no_work_flight_hours=99))
    cap = 0.5 * 700
    assert q.time_fee <= 2 * cap + 1e-9


def test_onsite_talk_costs_more_than_online_and_less_than_a_private_day():
    on, off, day = (price(o, R) for o in (talk(delivery="online"), talk(delivery="onsite"), private_workshop()))
    assert on.unit_price < off.unit_price < day.unit_price


def test_card_flags_a_talk_dearer_than_a_day():
    expensive_talk = talk().with_(positioning=12.0, name="Talk at 10k")
    found = check_card([price(expensive_talk, R), price(private_workshop(), R)])
    assert any(f.check == "dominance" and f.severity == "error" for f in found)


def test_position_skips_unknown_currency():
    cs = [Comparable("a", "training", "x", price=50, unit="per_person", contact_hours=1, currency="USD")]
    assert position(50, cs) is None
    assert position(50, cs, fx={"USD": 0.9}).median == pytest.approx(45)


def test_registry_has_the_three_specialties():
    assert {"training", "av_production", "software"} <= set(specialties())


def test_spec_round_trip_renders_markdown():
    spec = {
        "title": "t",
        "rates": {"day_rates": {"founder": 800}},
        "offerings": [
            {"id": "a", "specialty": "training", "template": "talk"},
            {"id": "b", "specialty": "training", "template": "private_workshop"},
            {"id": "c", "specialty": "av_production", "template": "production", "params": {"style": "explainer", "seconds": 60}},
        ],
        "travel": {"scenarios": [{"name": "far", "trip": {"one_way_hours": 3}}]},
        "sensitivity": {"day_rates": [600, 1000]},
    }
    card = build_card(spec)
    md = render(card)
    assert "# t" in md and "Travel and on-site add-on" in md
    assert card.sensitivity[1000]["a"] > card.sensitivity[600]["a"]
    assert not math.isnan(card["c"].quote.per_finished_minute)


def test_shipped_example_spec_builds_with_baseline_packets():
    from importlib.resources import files

    from pricewright import load_spec

    path = files("pricewright") / "data" / "skills" / "pricing-expert" / "references" / "example-spec.yaml"
    card = build_card(load_spec(str(path)))
    assert card["talk_online"].position is not None
    assert not [f for f in card.findings if f.severity == "error"]

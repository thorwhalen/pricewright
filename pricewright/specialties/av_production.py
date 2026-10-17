"""Commissioned audiovisual production: films, commercials, music videos, animation.

A production is priced from its crafts. Each craft has a *fixed* part (done once per
film: the character bible, the look) and a *per finished minute* part (shots
generated, selected, cut and mixed). A style is a table of those two numbers per
craft (:data:`STYLES`); a length is minutes; review rounds, variants and usage are
explicit inputs. Generation credits are a cost line computed from the finished
seconds, a shooting ratio (generated seconds per kept second) and the blended price
of a generated second.

Engagement shapes:

- :func:`production`: one film, treatment to delivery;
- :func:`pilot`: a short first piece that also builds the reusable setup (character
  bible, look); priced at cost (no margin) and credited against a follow-on production;
- :func:`retainer`: N finished minutes a month in an established format, where the
  fixed crafts are already paid for and only a refresh share recurs.

The twelve crafts follow the studio's own list (research to finishing), so a quote
reads like the process the client was shown.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from pricewright.base import Cost, Effort, Offering
from pricewright.specialties import MarketRef, Specialty, register

CRAFTS: tuple[str, ...] = (
    "research",
    "story_script",
    "character_design",
    "look",
    "storyboard_animatic",
    "performance_voice",
    "generation",
    "selection_continuity",
    "music",
    "sound",
    "edit",
    "finishing",
)


@dataclass(frozen=True)
class CraftHours:
    fixed: float  # hours once per film
    per_min: float  # hours per finished minute


def _style(**crafts: tuple[float, float]) -> Mapping[str, CraftHours]:
    unknown = set(crafts) - set(CRAFTS)
    if unknown:
        raise ValueError(f"Unknown crafts {sorted(unknown)}; crafts are {CRAFTS}")
    return {c: CraftHours(*crafts.get(c, (0.0, 0.0))) for c in CRAFTS}


# Hours per craft: (fixed per film, per finished minute). AI-assisted, human-led.
# Calibrated to reported AI production effort of about 1.3-4 person-days per finished
# minute (research packet av-production.md) plus a fixed setup of 2-5 days; to be
# re-fitted to the studio's own timesheets.
STYLES: dict[str, Mapping[str, CraftHours]] = {
    "commercial": _style(  # ~22 h fixed + ~22 h/min
        research=(1, 0.5), story_script=(4, 2), character_design=(3, 0), look=(4, 0),
        storyboard_animatic=(2, 2), performance_voice=(1, 1.5), generation=(1, 6),
        selection_continuity=(1, 4), music=(2, 2), sound=(1, 1), edit=(1, 2.5), finishing=(1, 0.5),
    ),
    "brand_film": _style(  # ~20 h + ~18 h/min
        research=(2, 1), story_script=(4, 2), character_design=(2, 0), look=(3, 0),
        storyboard_animatic=(2, 1.5), performance_voice=(1, 1), generation=(1, 5),
        selection_continuity=(1, 3), music=(2, 1.5), sound=(1, 0.5), edit=(1, 2), finishing=(0, 0.5),
    ),
    "narrative_short": _style(  # ~32 h + ~22 h/min
        research=(2, 0.5), story_script=(8, 2.5), character_design=(6, 0), look=(5, 0),
        storyboard_animatic=(2, 2), performance_voice=(2, 2), generation=(1, 6),
        selection_continuity=(1, 4), music=(2, 1.5), sound=(1, 1), edit=(1, 2), finishing=(1, 0.5),
    ),
    "explainer": _style(  # ~12 h + ~12 h/min
        research=(2, 1), story_script=(3, 2), character_design=(1, 0), look=(2, 0),
        storyboard_animatic=(1, 1), performance_voice=(0, 1), generation=(1, 3),
        selection_continuity=(0, 1.5), music=(1, 0.5), sound=(0, 0.5), edit=(1, 1), finishing=(0, 0.5),
    ),
    "animation": _style(  # ~26 h + ~22 h/min
        research=(1, 0.5), story_script=(4, 2), character_design=(7, 0), look=(5, 0),
        storyboard_animatic=(2, 2), performance_voice=(1, 1.5), generation=(1, 6),
        selection_continuity=(1, 4), music=(2, 2), sound=(1, 1), edit=(1, 2.5), finishing=(0, 0.5),
    ),
    "documentary": _style(  # ~30 h + ~10 h/min (long runtimes)
        research=(10, 2), story_script=(6, 1.5), character_design=(1, 0), look=(4, 0),
        storyboard_animatic=(1, 0.5), performance_voice=(1, 0.5), generation=(1, 1.5),
        selection_continuity=(1, 1), music=(2, 0.5), sound=(1, 0.5), edit=(1, 1.5), finishing=(1, 0.5),
    ),
    "music_video": _style(  # ~18 h + ~14 h/min; the music is the client's
        research=(1, 0), story_script=(3, 1), character_design=(4, 0), look=(5, 0),
        storyboard_animatic=(2, 1.5), generation=(1, 5), selection_continuity=(1, 3.5),
        sound=(0, 0), edit=(1, 2.5), finishing=(0, 0.5),
    ),
    "pitch_previs": _style(  # ~16 h + ~12 h/min; rougher finish
        research=(2, 0.5), story_script=(4, 1.5), character_design=(3, 0), look=(4, 0),
        storyboard_animatic=(1, 2), performance_voice=(0, 1), generation=(1, 3),
        selection_continuity=(0, 1.5), music=(1, 1), sound=(0, 0.5), edit=(0, 1), finishing=(0, 0),
    ),
    "social_series": _style(  # ~20 h + ~18 h/min, per episode or batch
        research=(1, 0.5), story_script=(4, 2), character_design=(5, 0), look=(4, 0),
        storyboard_animatic=(1, 1.5), performance_voice=(1, 1.5), generation=(1, 5),
        selection_continuity=(1, 3), music=(1, 1), sound=(0, 1), edit=(1, 2), finishing=(0, 0.5),
    ),
}

# crafts whose fixed part is the reusable "setup" a pilot builds and a retainer reuses
SETUP_CRAFTS = ("character_design", "look")

DEFAULTS: dict[str, float] = {
    "shooting_ratio": 20.0,  # generated seconds per kept second (Kalshi ad ~20-27 per kept shot)
    "cost_per_generated_second": 0.15,  # blended: Runway Gen-4.5 $0.12/s, Kling 3.0 Pro $0.17/s, Veo 3.1 $0.40/s
    "tools_per_project": 120.0,  # image, voice, music, upscaling subscriptions' share
    "producer_share": 0.12,  # project management and client communication, on craft hours
    "review_round_hours": 3.0,  # each included round of client review (both founders' time)
    "review_rounds": 2,
    "variant_hours": 2.0,  # each extra cut-down or format
    "contingency": 0.12,
    "margin": 0.10,
    "retainer_fixed_share": 0.25,  # share of fixed craft hours that recur each month on a retainer
    "retainer_commitment_discount": 0.15,  # retainers save 15-25% per video in the market
}

# Usage / licence uplift on the creative fee (commercials and brand films).
USAGE: dict[str, float] = {
    "organic": 0.0,  # owned channels, unlimited time
    "paid_social_1y": 0.15,
    "paid_national_1y": 0.35,
    "broadcast_1y": 0.6,
    "buyout_perpetual": 1.0,
}


def _effort_lines(style: str, minutes: float, *, D: Mapping, skip_fixed: tuple[str, ...] = (), fixed_share: float = 1.0):
    try:
        table = STYLES[style]
    except KeyError:
        raise KeyError(f"No style {style!r}. Styles: {sorted(STYLES)}") from None
    lines = []
    for craft, ch in table.items():
        fixed = 0.0 if craft in skip_fixed else ch.fixed * fixed_share
        h = fixed + ch.per_min * minutes
        if h:
            lines.append(Effort(craft.replace("_", " "), h, kind="production"))
    craft_hours = sum(e.hours for e in lines)
    rounds = D["review_rounds"]
    lines.append(Effort(f"{rounds:g} client review rounds", rounds * D["review_round_hours"], kind="admin"))
    lines.append(Effort("producing and client communication", craft_hours * D["producer_share"], kind="admin"))
    return lines


def _credit_cost(seconds: float, D: Mapping) -> Cost:
    gen = seconds * D["shooting_ratio"]
    return Cost(f"generation credits ({gen:,.0f} s generated)", gen * D["cost_per_generated_second"], kind="credits")


def production(
    *,
    style: str = "commercial",
    seconds: float = 60,
    variants: int = 0,
    usage: str = "organic",
    music_licence: float = 0.0,
    voice_talent: float = 0.0,
    name: str | None = None,
    defaults: dict | None = None,
    **overrides,
) -> Offering:
    """One finished film of ``seconds`` in ``style``, with ``variants`` extra cut-downs or formats."""
    D = {**DEFAULTS, **(defaults or {})}
    minutes = seconds / 60
    eff = _effort_lines(style, minutes, D=D)
    if variants:
        eff.append(Effort(f"{variants} variant(s)/cut-down(s)", variants * D["variant_hours"], kind="production"))
    if usage not in USAGE:
        raise KeyError(f"No usage {usage!r}. Usage tiers: {sorted(USAGE)}")
    uplift = USAGE[usage]
    costs = [_credit_cost(seconds, D), Cost("tools share", D["tools_per_project"], kind="tools")]
    if music_licence:
        costs.append(Cost("music licence", music_licence, kind="licence"))
    if voice_talent:
        costs.append(Cost("voice talent", voice_talent, kind="subcontract", markup=0.1))
    return Offering(
        name=name or f"{style.replace('_', ' ').title()}, {seconds:g} s",
        specialty="av_production",
        unit="per_project",
        delivery="n/a",
        efforts=tuple(eff),
        costs=tuple(costs),
        contingency=D["contingency"],
        margin=D["margin"],
        positioning=1 + uplift,
        family=f"av:{style}",
        includes=(f"{D['review_rounds']:g} review rounds", f"usage: {usage}"),
        duration_s=seconds,
        **overrides,
    )


def pilot(
    *,
    style: str = "commercial",
    seconds: float = 15,
    setup_share: float = 0.6,
    name: str | None = None,
    defaults: dict | None = None,
    **overrides,
) -> Offering:
    """A short first piece, at cost, credited against the next production.

    It builds a first version of the reusable setup (``setup_share`` of the style's fixed
    hours: one character, one look), with one review round. The production that follows
    finishes the setup, so the client never pays for it twice.
    """
    D = {**DEFAULTS, **(defaults or {}), "review_rounds": 1}
    eff = _effort_lines(style, seconds / 60, D=D, fixed_share=setup_share)
    o = production(style=style, seconds=seconds, defaults=D, name=name or f"Pilot, {style.replace('_', ' ')}, {seconds:g} s")
    return o.with_(
        efforts=tuple(eff),
        margin=0.0,
        terms=("fixed scope, fixed price", "credited in full against a production signed within 60 days"),
        **overrides,
    )


def retainer(
    *,
    style: str = "social_series",
    seconds_per_month: float = 180,
    pieces_per_month: int = 4,
    name: str | None = None,
    defaults: dict | None = None,
    **overrides,
) -> Offering:
    """A standing monthly output in an established format; the setup is reused, not rebuilt."""
    D = {**DEFAULTS, **(defaults or {})}
    minutes = seconds_per_month / 60
    eff = _effort_lines(style, minutes, D=D, skip_fixed=SETUP_CRAFTS, fixed_share=D["retainer_fixed_share"])
    # each piece still needs its own script and edit pass beyond the per-minute work
    eff.append(Effort(f"per-piece overhead, {pieces_per_month} pieces", pieces_per_month * 1.5, kind="production"))
    costs = [_credit_cost(seconds_per_month, D), Cost("tools share", D["tools_per_project"], kind="tools")]
    return Offering(
        name=name or f"Retainer, {style.replace('_', ' ')}, {seconds_per_month:g} s/month",
        specialty="av_production",
        unit="per_month",
        delivery="n/a",
        efforts=tuple(eff),
        costs=tuple(costs),
        contingency=D["contingency"] * 0.66,
        margin=D["margin"],
        positioning=1 - D["retainer_commitment_discount"],
        duration_s=seconds_per_month,
        family=f"av-retainer:{style}",
        terms=("3-month minimum", "unused minutes do not roll over beyond one month"),
        **overrides,
    )


RESEARCH_NEEDS = (
    "Price per finished minute (or per project, with runtime) by style, traditional and AI-assisted, in the region.",
    "Published prices of AI video studios and freelancers: pilots, packages, retainers.",
    "Freelance day rates for writer, director, editor, composer, sound, motion designer in the region.",
    "Person-days per finished minute by style, traditional and AI (timesheets, case studies).",
    "Generation tool prices per second of output, and typical shooting ratios.",
    "Commercial terms: deposits, included revision rounds, change-order rates, usage/licence uplifts.",
)

# packet labels that count as the same kind of film as a style
STYLE_SYNONYMS: dict[str, tuple[str, ...]] = {
    "commercial": ("commercial",),
    "brand_film": ("brand_film", "corporate_video"),
    "narrative_short": ("short_film", "narrative_short"),
    "explainer": ("explainer", "corporate_video"),
    "animation": ("animation",),
    "documentary": ("documentary",),
    "music_video": ("music_video",),
    "pitch_previs": ("pitch_previs",),
    "social_series": ("social_series",),
}


def like_for_like(c, o: Offering, *, band: tuple[float, float] = (0.5, 2.0)) -> float | None:
    """A comparable's price as a project price for ``o``'s style and runtime, or None.

    Same style (by :data:`STYLE_SYNONYMS`); a project price only if its runtime is
    within ``band`` of the offering's; a per-minute rate only for offerings of a minute
    or more (per-minute rates are quoted for long-form and do not scale down).
    """
    style = o.family.split(":", 1)[-1]
    if c.offering not in STYLE_SYNONYMS.get(style, (style,)) or c.mid is None or not o.duration_s:
        return None
    if c.unit == "per_project" and c.duration_s:
        r = c.duration_s / o.duration_s
        return c.mid if band[0] <= r <= band[1] else None
    if c.unit == "per_finished_minute" and o.duration_s >= 60:
        return c.mid * o.duration_s / 60
    return None


MARKET = {
    "production": MarketRef("as_is", (), value="unit_price", match=like_for_like),
    "pilot": MarketRef("as_is", ("pilot",), units=("per_project",), value="unit_price"),
    "retainer": MarketRef("as_is", ("retainer",), units=("per_month",), value="unit_price"),
}

SPECIALTY = register(
    Specialty(
        name="av_production",
        title="Commissioned audiovisual production",
        description=__doc__.split("\n\n")[0],
        templates={"production": production, "pilot": pilot, "retainer": retainer},
        research_needs=RESEARCH_NEEDS,
        market=MARKET,
        defaults=DEFAULTS,
    )
)

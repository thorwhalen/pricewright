"""Command line: ``pricewright card SPEC.yaml``, ``pricewright travel ...``, ``pricewright specialties``."""

from __future__ import annotations

import argparse
import sys


def _card(args):
    from pricewright import build_card, load_spec, render

    md = render(build_card(load_spec(args.spec)))
    if args.out:
        with open(args.out, "w") as f:
            f.write(md)
        print(args.out)
    else:
        sys.stdout.write(md)


def _travel(args):
    from pricewright import Rates, Trip, travel_addon

    q = travel_addon(
        Trip(
            args.one_way_hours,
            transport_round_trip=args.transport,
            working_days=args.days,
            travellers=args.travellers,
            start_hour=args.start,
        ),
        rates=Rates({"founder": args.day_rate}),
    )
    for ln in q.lines:
        print(f"{ln.amount:>9,.0f}  {ln.label}")
    print(f"{q.total:>9,.0f}  total ({q.nights} night(s))")


def _specialties(args):
    from pricewright import specialties

    for s in specialties().values():
        print(f"{s.name}: {s.title}\n  templates: {', '.join(s.templates)}")
        for need in s.research_needs:
            print(f"  needs: {need}")


def main(argv=None):
    p = argparse.ArgumentParser(prog="pricewright", description=__doc__)
    sub = p.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("card", help="price, check and render a rate-card spec")
    c.add_argument("spec")
    c.add_argument("--out", "-o")
    c.set_defaults(fn=_card)
    t = sub.add_parser("travel", help="the travel add-on for one trip")
    t.add_argument("one_way_hours", type=float)
    t.add_argument("--transport", type=float, default=0.0, help="round trip per traveller, at cost")
    t.add_argument("--days", type=int, default=1)
    t.add_argument("--travellers", type=int, default=1)
    t.add_argument("--start", type=float, default=9.5)
    t.add_argument("--day-rate", type=float, default=900.0)
    t.set_defaults(fn=_travel)
    s = sub.add_parser("specialties", help="list specialties, templates and the research each needs")
    s.set_defaults(fn=_specialties)
    args = p.parse_args(argv)
    args.fn(args)


if __name__ == "__main__":
    main()

#!/usr/bin/python3
# Waybar module showing the current uni lecture and its remaining time,
# or the next lecture and the time until it starts.
from dataclasses import dataclass
from datetime import datetime, timedelta, time
import json


@dataclass
class Lecture:
    name: str
    weekday: int  # 0 = Monday ... 6 = Sunday
    start: time
    duration: timedelta


MON, TUE, WED, THU, FRI, SAT, SUN = range(7)

LECTURES = [
    Lecture("Mathematical Methods - Excersise - N1", MON, time(9, 0), timedelta(minutes=90)),
    Lecture("Linear Algebra - Lecture - N1", MON, time(10, 40), timedelta(minutes=90)),
    Lecture("Mathematical Analysis - Lecture - N1", MON, time(14, 0), timedelta(minutes=90)),
    Lecture("Programming for Physicists - Excersise - N10", MON, time(15, 40), timedelta(minutes=90)),
    Lecture("Linear Algebra - Excersise - T8", MON, time(17, 20), timedelta(minutes=90)),

    Lecture("Mechanics excersises - Excersise - M1", TUE, time(9, 50), timedelta(minutes=90)),
    Lecture("Mathematical Analysis - Excersise - M2", TUE, time(11, 30), timedelta(minutes=135)),
    Lecture("Mechanics and Molecular Physics - Excersise - M3", TUE, time(14, 50), timedelta(minutes=90)),
    Lecture("Physics in Experiments - Excersise F1", TUE, time(17, 20), timedelta(minutes=45)),

    Lecture("Mechanics and Molecular Physics - Lecture - F1", WED, time(9, 0), timedelta(minutes=90)),
    Lecture("Practical Physics - Excersise - T9", WED, time(12, 20), timedelta(minutes=90)),
    Lecture("Mathematical Analysis - Lecture - N1", WED, time(14, 0), timedelta(minutes=90)),

    Lecture("Programming for Physicists - Lecture - T2", THU, time(9, 0), timedelta(minutes=90)),
    Lecture("English - Excersise - V151", THU, time(10, 40), timedelta(minutes=90)),
    Lecture("Mechanics and Molecular Physics - Lecture - F1", THU, time(13, 10), timedelta(minutes=90)),

    Lecture("PE - Excersise - KTV", FRI, time(7, 20), timedelta(minutes=225)),
]

DAY_NAMES = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


def fmt_delta(delta: timedelta) -> str:
    mins = int(delta.total_seconds()) // 60
    days, mins = divmod(mins, 24 * 60)
    hours, mins = divmod(mins, 60)
    if days:
        return f"{days}d {hours:02d}h"
    if hours:
        return f"{hours}h {mins:02d}m"
    return f"{mins}m"


def occurrences(lecture: Lecture, now: datetime):
    """Starts of this lecture in the previous, current and next week."""
    monday = datetime.combine(now.date() - timedelta(days=now.weekday()), time())
    start = datetime.combine(monday.date() + timedelta(days=lecture.weekday), lecture.start)
    return [start + timedelta(weeks=w) for w in (-1, 0, 1)]


def tooltip() -> str:
    rows = sorted(LECTURES, key=lambda l: (l.weekday, l.start))
    today = datetime.now().weekday()
    rows = filter(lambda l: l.weekday == today, rows)
    return "\n".join(
        f"{DAY_NAMES[l.weekday]} {l.start:%H:%M}-"
        f"{(datetime.combine(datetime.min, l.start) + l.duration):%H:%M}  {l.name}"
        for l in rows
    )


def main(now=None):
    if not LECTURES:
        print(json.dumps({"text": "no lectures", "class": "idle"}))
        return

    now = now or datetime.now()
    upcoming = []
    for lecture in LECTURES:
        for start in occurrences(lecture, now):
            end = start + lecture.duration
            if start <= now < end:
                progress = (now - start) / lecture.duration
                print(json.dumps({
                    "text": f"{lecture.name} {int(progress * 100)}% {fmt_delta(end - now)} left",
                    "tooltip": tooltip(),
                    "class": "active",
                    "percentage": int(progress * 100),
                }))
                return
            if start > now:
                upcoming.append((start, lecture))

    start, lecture = min(upcoming, key=lambda u: u[0])
    print(json.dumps({
        "text": f"{lecture.name} in {fmt_delta(start - now)}",
        "tooltip": tooltip(),
        "class": "upcoming",
    }))


if __name__ == "__main__":
    main()

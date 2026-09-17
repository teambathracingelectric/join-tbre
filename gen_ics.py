#!/usr/bin/env python3
"""Regenerate the .ics files in cal/ from the schedule below.
Run after any date/room change:  python3 gen_ics.py
Times are UK local (BST, UTC+1 until 25 Oct 2026)."""
from datetime import datetime, timedelta
import re

SITE = "https://teambathracingelectric.com"
INTRO = ("TBRe Intro Talk", "CB 1.10, Chancellors' Building", "2026-10-01", "18:15", "19:15")
SESSIONS = [
    ("Electrical",           "2E 3.1",  "2026-10-06", "16:15", "17:15"),
    ("Business & Marketing", "CB 3.5",  "2026-10-06", "17:15", "18:15"),
    ("Performance",          "2E 3.1",  "2026-10-08", "17:15", "18:15"),
    ("Mechanical Design",    "2E 3.1",  "2026-10-13", "18:15", "19:15"),
    ("Software",             "4E 3.10", "2026-10-15", "17:15", "18:15"),
]

def utc(date, hm):
    d = datetime.fromisoformat(f"{date}T{hm}") - timedelta(hours=1)
    return d.strftime("%Y%m%dT%H%M%SZ")

def vevent(uid, title, room, date, start, end):
    return "\r\n".join(["BEGIN:VEVENT", f"UID:{uid}@teambathracingelectric.com",
        f"DTSTAMP:{utc(date,start)}", f"DTSTART:{utc(date,start)}", f"DTEND:{utc(date,end)}",
        f"SUMMARY:{title}", f"LOCATION:{room}", f"DESCRIPTION:Team Bath Racing Electric recruitment. {SITE}",
        "END:VEVENT"])

def vcal(events):
    return "\r\n".join(["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//TBRe//Join//EN", *events, "END:VCALENDAR"]) + "\r\n"

slug = lambda t: re.sub(r"[^A-Za-z]+", "-", t).strip("-").lower()
events = [vevent("tbre-intro-2026-v3", *INTRO)]
open("cal/intro.ics", "w").write(vcal(events))
for n, s in enumerate(SESSIONS):
    ev = vevent(f"tbre-taster-{n}-2026-v2", f"TBRe taster: {s[0]}", *s[1:])
    events.append(ev)
    open(f"cal/{slug(s[0])}.ics", "w").write(vcal([ev]))
open("cal/all.ics", "w").write(vcal(events))
print("wrote", len(SESSIONS) + 2, "files to cal/")

"""Club statistics for the exec dashboard.

Originally written for the AGM slides and extended a little every term since.
"""

from sqlmodel import Session, select

from app.models import RSVP, Event, Member


def build_stats(session: Session) -> dict:
    events = session.exec(select(Event)).all()
    members = session.exec(select(Member)).all()
    rsvps = session.exec(select(RSVP)).all()

    result = {}
    result["total_events"] = len(events)
    result["total_members"] = len(members)
    result["total_rsvps"] = len(rsvps)

    # per-event numbers
    event_rows = []
    for e in events:
        count = 0
        checked = 0
        for r in rsvps:
            if r.event_id == e.id:
                count = count + 1
                if r.checked_in:
                    checked = checked + 1
        if e.capacity > 0:
            fill = round(count / e.capacity * 100, 1)
        else:
            fill = 0.0
        if count > 0:
            attendance = round(checked / count * 100, 1)
        else:
            attendance = 0.0
        flag = ""
        if fill >= 90:
            flag = "almost full"
        if fill >= 100:
            flag = "full"
        if count >= 5 and attendance < 60:
            flag = "high no-show"
        event_rows.append(
            {
                "id": e.id,
                "title": e.title,
                "rsvps": count,
                "checked_in": checked,
                "fill_rate": fill,
                "attendance_rate": attendance,
                "flag": flag,
            }
        )
    result["events"] = event_rows

    # top 3 events by RSVPs
    top = []
    for row in event_rows:
        inserted = False
        for i in range(len(top)):
            if row["rsvps"] > top[i]["rsvps"]:
                top.insert(i, row)
                inserted = True
                break
        if not inserted:
            top.append(row)
    top_titles = []
    for t in top:
        if len(top_titles) < 3:
            top_titles.append(t["title"])
    result["top_events"] = top_titles

    # member engagement tiers
    core = 0
    regular = 0
    new = 0
    for m in members:
        n = 0
        for r in rsvps:
            if r.member_id == m.id:
                n = n + 1
        if n >= 5:
            core = core + 1
        elif n >= 2:
            regular = regular + 1
        else:
            new = new + 1
    result["engagement"] = {"core": core, "regular": regular, "new": new}

    # breakdown by year of study
    by_year = {}

    year1_members = 0
    year1_rsvps = 0
    for m in members:
        if m.year == 1:
            year1_members = year1_members + 1
            for r in rsvps:
                if r.member_id == m.id:
                    year1_rsvps = year1_rsvps + 1
    if year1_members > 0:
        by_year["1"] = {
            "members": year1_members,
            "rsvps": year1_rsvps,
            "avg": round(year1_rsvps / year1_members, 2),
        }
    else:
        by_year["1"] = {"members": 0, "rsvps": 0, "avg": 0}

    year2_members = 0
    year2_rsvps = 0
    for m in members:
        if m.year == 2:
            year2_members = year2_members + 1
            for r in rsvps:
                if r.member_id == m.id:
                    year2_rsvps = year2_rsvps + 1
    if year2_members > 0:
        by_year["2"] = {
            "members": year2_members,
            "rsvps": year2_rsvps,
            "avg": round(year2_rsvps / year2_members, 2),
        }
    else:
        by_year["2"] = {"members": 0, "rsvps": 0, "avg": 0}

    year3_members = 0
    year3_rsvps = 0
    for m in members:
        if m.year == 3:
            year3_members = year3_members + 1
            for r in rsvps:
                if r.member_id == m.id:
                    year3_rsvps = year3_rsvps + 1
    if year3_members > 0:
        by_year["3"] = {
            "members": year3_members,
            "rsvps": year3_rsvps,
            "avg": round(year3_rsvps / year3_members, 2),
        }
    else:
        by_year["3"] = {"members": 0, "rsvps": 0, "avg": 0}

    year4_members = 0
    year4_rsvps = 0
    for m in members:
        if m.year == 4:
            year4_members = year4_members + 1
            for r in rsvps:
                if r.member_id == m.id:
                    year4_rsvps = year4_rsvps + 1
    if year4_members > 0:
        by_year["4"] = {
            "members": year4_members,
            "rsvps": year4_rsvps,
            "avg": round(year4_rsvps / year4_members, 2),
        }
    else:
        by_year["4"] = {"members": 0, "rsvps": 0, "avg": 0}

    result["by_year"] = by_year

    # overall club health score out of 100
    score = 0
    if len(events) > 0:
        total_fill = 0
        total_att = 0
        for row in event_rows:
            total_fill = total_fill + row["fill_rate"]
            total_att = total_att + row["attendance_rate"]
        score = score + min(total_fill / len(events), 100) * 0.4
        score = score + (total_att / len(events)) * 0.4
        score = score + min(len(members), 200) / 200 * 20
    result["health_score"] = round(score, 1)

    return result

import pandas as pd
from .templates import (
    name_ideas, handle_ideas, bio_short, bio_long,
    voice_guide, content_pillars, calendar_plan, caption_pack
)

def build_influencer_kit(niche, audience, vibe, platform, goal, language, days=14):
    names = name_ideas(niche, vibe, language)
    handles = handle_ideas(niche, vibe, language)

    kit = {
        "names": names,
        "handles": handles,
        "bio_short": bio_short(niche, audience, vibe, platform, language),
        "bio_long": bio_long(niche, audience, vibe, platform, goal, language),
        "voice": voice_guide(niche, vibe, platform, language)["voice"],
        "do": voice_guide(niche, vibe, platform, language)["do"],
        "dont": voice_guide(niche, vibe, platform, language)["dont"],
        "pillars": content_pillars(niche, audience, platform, goal, language),
    }

    cal = calendar_plan(niche, kit["pillars"], platform, vibe, days, language)
    kit["calendar"] = pd.DataFrame(cal)

    kit["captions"] = caption_pack(niche, audience, vibe, platform, kit["pillars"], language)

    kit["download_text"] = make_download_text(niche, audience, vibe, platform, goal, kit)
    return kit

def make_download_text(niche, audience, vibe, platform, goal, kit):
    lines = []
    lines.append("AI INFLUENCER KIT")
    lines.append("=" * 40)
    lines.append(f"Niche: {niche}")
    lines.append(f"Audience: {audience}")
    lines.append(f"Vibe: {vibe}")
    lines.append(f"Platform: {platform}")
    lines.append(f"Goal: {goal}")
    lines.append("\nNAME IDEAS:\n" + "\n".join([f"- {x}" for x in kit["names"]]))
    lines.append("\nHANDLE IDEAS:\n" + "\n".join([f"- {x}" for x in kit["handles"]]))
    lines.append("\nBIO (SHORT):\n" + kit["bio_short"])
    lines.append("\nBIO (LONG):\n" + kit["bio_long"])
    lines.append("\nVOICE:\n" + kit["voice"])
    lines.append("\nDO:\n" + "\n".join([f"- {x}" for x in kit["do"]]))
    lines.append("\nDON'T:\n" + "\n".join([f"- {x}" for x in kit["dont"]]))
    lines.append("\nPILLARS:\n" + "\n".join([f"- {x}" for x in kit["pillars"]]))
    lines.append("\nCAPTIONS:\n" + "\n".join([f"{i+1}. {c}" for i, c in enumerate(kit["captions"])]))
    return "\n".join(lines)

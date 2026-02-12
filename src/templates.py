import random

def _lang(language, en, ny):
    return ny if language == "Chichewa" else en

def name_ideas(niche, vibe, language):
    base = [
        f"The {niche.title()} Plug",
        f"{niche.title()} with Vibes",
        f"Daily {niche.title()} Lab",
        f"{vibe} {niche.title()} Hub",
        f"{niche.title()} Simplified",
        f"{niche.title()} Corner",
    ]
    if language == "Chichewa":
        base += [f"{niche.title()} Tsiku ndi Tsiku", f"Zinsinsi za {niche.title()}"]
    random.shuffle(base)
    return base[:6]

def handle_ideas(niche, vibe, language):
    n = niche.lower().replace(" ", "")
    v = vibe.lower()
    base = [
        f"@{n}daily",
        f"@{v}{n}",
        f"@learn{n}",
        f"@{n}hub",
        f"@{n}vibes",
        f"@the{n}plug",
    ]
    if language == "Chichewa":
        base += [f"@{n}mw", f"@{n}malawi"]
    random.shuffle(base)
    return base[:8]

def bio_short(niche, audience, vibe, platform, language):
    return _lang(
        language,
        f"{vibe} {niche} tips for {audience}. 🎯 | {platform} creator | New posts weekly ✨",
        f"Malangizo a {niche} ( {vibe} ) kwa {audience}. 🎯 | {platform} | Zatsopano sabata iliyonse ✨",
    )

def bio_long(niche, audience, vibe, platform, goal, language):
    return _lang(
        language,
        f"I create {vibe.lower()} {niche} content for {audience}. "
        f"My goal: {goal.lower()}. Follow for practical tips, mini-guides, and real talk. ✨",
        f"Ndimapanga zomwe zili za {niche} ( {vibe} ) kwa {audience}. "
        f"Cholinga changa: {goal.lower()}. Tsatirani kuti mupeze malangizo, maphunziro ang’ono, ndi chowona. ✨",
    )

def voice_guide(niche, vibe, platform, language):
    voice = _lang(
        language,
        f"{vibe} and clear. Short punchy sentences. Simple examples. Strong hooks for {platform}.",
        f"{vibe} komanso momveka bwino. Mawu achidule. Zitsanzo zosavuta. Zoyambira zolimba pa {platform}.",
    )
    do = [
        _lang(language, "Start with a hook (question or bold claim).", "Yambani ndi funso kapena mawu amphamvu."),
        _lang(language, "Use simple examples and quick steps.", "Gwiritsani ntchito zitsanzo zosavuta ndi njira zachidule."),
        _lang(language, "Be consistent with posting.", "Khalani okhazikika potumiza."),
    ]
    dont = [
        _lang(language, "Avoid long paragraphs.", "Pewani ma paragraph ataliatali."),
        _lang(language, "Don’t copy trending content exactly—remix it.", "Osangokopera trend—sinthani momwe mukufunira."),
        _lang(language, "Avoid vague advice; be specific.", "Pewani malangizo osamveka; khalani omveka."),
    ]
    return {"voice": voice, "do": do, "dont": dont}

def content_pillars(niche, audience, platform, goal, language):
    pillars = [
        _lang(language, f"Beginner tips in {niche}", f"Zoyambira za {niche}"),
        _lang(language, f"Mistakes {audience} make", f"Zolakwika zomwe {audience} amachita"),
        _lang(language, f"Tools & resources", f"Zida ndi zinthu zothandiza"),
        _lang(language, f"Quick challenges / mini tasks", f"Zovuta zazing’ono / ntchito zazifupi"),
        _lang(language, f"Behind-the-scenes / real stories", f"Zomwe zimachitika kumbuyo / nkhani zenizeni"),
    ]
    return pillars

def calendar_plan(niche, pillars, platform, vibe, days, language):
    plan = []
    for d in range(1, days + 1):
        pillar = pillars[(d - 1) % len(pillars)]
        idea = _lang(
            language,
            f"Post a {platform} piece: '{pillar}' with a {vibe.lower()} hook + 3 quick points.",
            f"Tumizani pa {platform}: '{pillar}' ndi kuyamba kwa {vibe.lower()} + mfundo 3 zachidule.",
        )
        plan.append({"Day": d, "Pillar": pillar, "Post idea": idea})
    return plan

def caption_pack(niche, audience, vibe, platform, pillars, language):
    hooks = [
        _lang(language, "Stop scrolling—this will save you time:", "Imani kaye—izi zikuthandizani:"),
        _lang(language, "Most people get this wrong:", "Anthu ambiri amalakwitsa izi:"),
        _lang(language, "If you’re {audience}, you need this:", "Ngati muli {audience}, muyenera izi:"),
        _lang(language, "Try this today:", "Yesani izi lero:"),
    ]
    caps = []
    for i in range(12):
        pillar = random.choice(pillars)
        hook = random.choice(hooks).replace("{audience}", audience)
        cap = _lang(
            language,
            f"{hook}\n\n{pillar}\n✅ Step 1: ...\n✅ Step 2: ...\n✅ Step 3: ...\n\nFollow for more {niche} 🔥",
            f"{hook}\n\n{pillar}\n✅ Gawo 1: ...\n✅ Gawo 2: ...\n✅ Gawo 3: ...\n\nTsatirani kuti mupeze zambiri za {niche} 🔥",
        )
        caps.append(cap)
    return caps

import os
from datetime import date

import streamlit as st
from dotenv import load_dotenv

from src.generators import build_influencer_kit
from src.sources.pexels_client import download_daily_background
from src.quotes import get_daily_quote
from src.video_maker import make_quote_video

load_dotenv()

st.set_page_config(page_title="AI Influencer Kit", page_icon="✨", layout="wide")

st.title("✨ Build Your Own AI Influencer Kit")
st.caption("Generate a full influencer identity + content plan in minutes.")

# ----------------------------
# Sidebar controls
# ----------------------------
with st.sidebar:
    st.header("Your Influencer Settings")
    niche = st.text_input("Niche", placeholder="e.g., fitness, tech, beauty, motivation")
    audience = st.text_input("Target audience", placeholder="e.g., students, moms, founders")
    vibe = st.selectbox("Vibe", ["Funny", "Luxury", "Educational", "Motivational", "Relatable", "Bold", "Calm"])
    platform = st.selectbox("Platform", ["TikTok", "Instagram", "X (Twitter)", "LinkedIn", "YouTube"])
    goal = st.selectbox("Goal", ["Grow followers", "Sell a product", "Build authority", "Drive website traffic"])
    language = st.selectbox("Language", ["English", "Chichewa"])
    days = st.slider("Content calendar days", 7, 30, 14)

# ----------------------------
# Daily Facebook video section
# ----------------------------
st.divider()
st.header("🎬 Daily Facebook Video (90 seconds)")

query = st.text_input("Background theme (Pexels search)", value="motivational abstract")
generate_video = st.button("Generate today's 90s quote video (online sources)")

if generate_video:
    pexels_key = os.getenv("PEXELS_API_KEY", "").strip()

    # Helpful debug (doesn't expose the key)
    st.caption(f"PEXELS key loaded: {'YES' if pexels_key else 'NO'} | Length: {len(pexels_key)}")

    if not pexels_key or pexels_key == "put_your_key_here":
        st.error("PEXELS_API_KEY not found or still a placeholder. Put your real key in the .env file.")
    else:
        try:
            quote, author = get_daily_quote()

            bg_path, bg_source = download_daily_background(
                api_key=pexels_key,
                query=query,
                out_dir="downloads",
                orientation="portrait",
            )

            out_file = os.path.join("output", f"facebook_quote_{date.today().isoformat()}.mp4")

            make_quote_video(
                out_path=out_file,
                quote=quote,
                author=author,
                duration=90,
                background_path=bg_path,
                music_dir="assets/music",   # optional
            )

            st.success("Video created!")
            st.write(f"**Quote:** {quote} — {author}")
            st.write(f"**Background source:** {bg_source}")

            with open(out_file, "rb") as f:
                st.download_button(
                    "⬇️ Download today's video",
                    data=f,
                    file_name=os.path.basename(out_file),
                    mime="video/mp4",
                )

        except Exception as e:
            st.error(f"Failed to generate video: {e}")

# ----------------------------
# Influencer kit section
# ----------------------------
st.divider()
generate_kit = st.button("🚀 Generate Kit")

if generate_kit:
    if not niche or not audience:
        st.error("Please fill in Niche and Target audience.")
    else:
        kit = build_influencer_kit(
            niche=niche.strip(),
            audience=audience.strip(),
            vibe=vibe,
            platform=platform,
            goal=goal,
            language=language,
            days=days,
        )

        col1, col2 = st.columns([1, 1])

        with col1:
            st.subheader("👤 Identity")
            st.write("**Name ideas:**")
            st.write("\n".join([f"- {x}" for x in kit["names"]]))
            st.write("**Handle ideas:**")
            st.write("\n".join([f"- {x}" for x in kit["handles"]]))

            st.write("**Bio (short):**")
            st.code(kit["bio_short"])

            st.write("**Bio (long):**")
            st.write(kit["bio_long"])

            st.subheader("🎯 Brand Voice")
            st.write("**Voice description:**")
            st.write(kit["voice"])

            st.write("**Do:**")
            st.write("\n".join([f"- {x}" for x in kit["do"]]))

            st.write("**Don’t:**")
            st.write("\n".join([f"- {x}" for x in kit["dont"]]))

        with col2:
            st.subheader("📌 Content Strategy")
            st.write("**Content pillars:**")
            st.write("\n".join([f"- {x}" for x in kit["pillars"]]))

            st.subheader("🗓️ Content Calendar")
            st.dataframe(kit["calendar"], use_container_width=True)

            st.subheader("✍️ Caption Pack")
            st.write("\n\n".join([f"**{i+1}.** {c}" for i, c in enumerate(kit["captions"])]))

        st.download_button(
            "⬇️ Download kit as text",
            data=kit["download_text"],
            file_name="ai_influencer_kit.txt",
        )

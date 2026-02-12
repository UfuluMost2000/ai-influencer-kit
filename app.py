import streamlit as st
from src.generators import build_influencer_kit

st.set_page_config(page_title="AI Influencer Kit", page_icon="✨", layout="wide")

st.title("✨ Build Your Own AI Influencer Kit")
st.caption("Generate a full influencer identity + content plan in minutes.")

with st.sidebar:
    st.header("Your Influencer Settings")
    niche = st.text_input("Niche", placeholder="e.g., fitness, tech, beauty, motivation")
    audience = st.text_input("Target audience", placeholder="e.g., students, moms, founders")
    vibe = st.selectbox("Vibe", ["Funny", "Luxury", "Educational", "Motivational", "Relatable", "Bold", "Calm"])
    platform = st.selectbox("Platform", ["TikTok", "Instagram", "X (Twitter)", "LinkedIn", "YouTube"])
    goal = st.selectbox("Goal", ["Grow followers", "Sell a product", "Build authority", "Drive website traffic"])
    language = st.selectbox("Language", ["English", "Chichewa"])
    days = st.slider("Content calendar days", 7, 30, 14)

generate = st.button("🚀 Generate Kit")

if generate:
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
            days=days
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
            file_name="ai_influencer_kit.txt"
        )

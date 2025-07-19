
import streamlit as st
from utils.video_extractor import get_video_metadata

from analysis_function import analyze_video_with_groq
import os

from dotenv import load_dotenv
load_dotenv()


st.set_page_config(page_title="🎯 Video SEO Optimiser", layout="wide")
st.title("🎯 Video SEO Optimiser")

st.markdown("Enter a video URL (YouTube, Instagram, LinkedIn, etc.) to extract metadata and generate SEO assets.")

video_url = st.text_input("📺 Video URL")
language = st.selectbox("🌐 Language", ["English", "Hindi", "Spanish", "French"], index=0)

if st.button("🚀 Run SEO Optimization"):
    if not video_url:
        st.warning("Please enter a video URL.")
    elif not os.getenv("GROQ_API_KEY"):
        st.error("GROQ_API_KEY not set in environment.")
    else:
        with st.spinner("Analyzing and optimizing..."):
            try:
                metadata = get_video_metadata(video_url)
                result = analyze_video_with_groq(video_url, metadata, language)

                st.success("✅ Optimization complete!")

                with st.expander("🧠 AI Video Analysis", expanded=False):
                    st.markdown(result["analysis"])

                with st.expander("🏷️ Tags (35 SEO Tags)", expanded=False):
                    st.markdown(", ".join(result["seo"]["tags"]))

                with st.expander("📝 SEO Description", expanded=False):
                    st.markdown(result["seo"]["description"])

                with st.expander("⏱️ Timestamps", expanded=False):
                    for ts in result["seo"]["timestamps"]:
                        st.markdown(f"**{ts['time']}** – {ts['description']}")

                with st.expander("📢 Title Suggestions", expanded=False):
                    for title_obj in result["seo"]["titles"]:
                        st.markdown(f"**{title_obj['rank']}. {title_obj['title']}** — {title_obj['reason']}")

                with st.expander("🖼️ Thumbnail Concepts", expanded=False):
                    for idx, concept in enumerate(result["thumbnails"].get("thumbnail_concepts", []), 1):
                        st.markdown(f"### Concept {idx}")
                        st.markdown(f"**Text Overlay**: {concept['text_overlay']}")
                        st.markdown(f"**Focal Point**: {concept['focal_point']}")
                        st.markdown(f"**Tone**: {concept['tone']}")
                        st.markdown(f"**Colors**: {' '.join(concept['colors'])}")
                        st.markdown(f"**Layout**: {concept['composition']}")
                        st.markdown(f"**Idea**: {concept['concept']}")
                        st.divider()

            except Exception as e:
                st.error(f"❌ Error: {e}")





#for Openai



# import streamlit as st
# from utils.video_extractor import get_video_metadata
# # from analysis_function import analyze_video_with_openai

# from analysis_function import analyze_video_with_groq
# import os

# from dotenv import load_dotenv
# load_dotenv()


# st.set_page_config(page_title="🎯 Video SEO Optimiser", layout="wide")
# st.title("🎯 Video SEO Optimiser")

# st.markdown("Enter a video URL (YouTube, Instagram, LinkedIn, etc.) to extract metadata and generate SEO assets.")

# video_url = st.text_input("📺 Video URL")
# language = st.selectbox("🌐 Language", ["English", "Hindi", "Spanish", "French"], index=0)

# if st.button("🚀 Run SEO Optimization"):
#     if not video_url:
#         st.warning("Please enter a video URL.")
#     elif not os.getenv("OPENAI_API_KEY"):
#         st.error("OPENAI_API_KEY not set in environment.")
#     else:
#         with st.spinner("Analyzing and optimizing..."):
#             try:
#                 metadata = get_video_metadata(video_url)
#                 result = analyze_video_with_openai(video_url, metadata, language)

#                 st.success("✅ Optimization complete!")

#                 with st.expander("🧠 AI Video Analysis", expanded=False):
#                     st.markdown(result["analysis"])

#                 with st.expander("🏷️ Tags (35 SEO Tags)", expanded=False):
#                     st.markdown(", ".join(result["seo"]["tags"]))

#                 with st.expander("📝 SEO Description", expanded=False):
#                     st.markdown(result["seo"]["description"])

#                 with st.expander("⏱️ Timestamps", expanded=False):
#                     for ts in result["seo"]["timestamps"]:
#                         st.markdown(f"**{ts['time']}** – {ts['description']}")

#                 with st.expander("📢 Title Suggestions", expanded=False):
#                     for title_obj in result["seo"]["titles"]:
#                         st.markdown(f"**{title_obj['rank']}. {title_obj['title']}** — {title_obj['reason']}")

#                 with st.expander("🖼️ Thumbnail Concepts", expanded=False):
#                     for idx, concept in enumerate(result["thumbnails"].get("thumbnail_concepts", []), 1):
#                         st.markdown(f"### Concept {idx}")
#                         st.markdown(f"**Text Overlay**: {concept['text_overlay']}")
#                         st.markdown(f"**Focal Point**: {concept['focal_point']}")
#                         st.markdown(f"**Tone**: {concept['tone']}")
#                         st.markdown(f"**Colors**: {' '.join(concept['colors'])}")
#                         st.markdown(f"**Layout**: {concept['composition']}")
#                         st.markdown(f"**Idea**: {concept['concept']}")
#                         st.divider()

#             except Exception as e:
#                 st.error(f"❌ Error: {e}")




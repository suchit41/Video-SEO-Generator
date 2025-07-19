import os
import json
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

def generate_fallback_seo(video_metadata, platform, language):
    return {
        "tags": ["default", "seo", "video", "fallback"] * 9,
        "description": f"No SEO data could be generated for this {platform} video.",
        "timestamps": [],
        "titles": []
    }

def ensure_exactly_35_tags(tags, llm, video_metadata, platform, language):
    prompt = f"""
You provided {len(tags)} tags. Adjust them to exactly 35 relevant, high-performing tags for a video titled "{video_metadata.get('title')}" on {platform}. 
Return ONLY a JSON array of 35 tags.
"""
    messages = [
        SystemMessage(content=f"You are an expert in optimizing tags for {platform}."),
        HumanMessage(content=prompt)
    ]
    try:
        response = llm(messages)
        return json.loads(response.content)
    except:
        return tags[:35]

def analyze_video_with_langchain(video_url, video_metadata, Language='English'):
    """Analyze video content with LangChain using platform-specific optimization."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise Exception("OPENAI_API_KEY environment variable is missing.")

    llm = ChatOpenAI(model="gpt-4", temperature=0.7, openai_api_key=api_key)

    platform = video_metadata.get('platform', 'YouTube')
    title = video_metadata.get('title', '')

    # === 1. ANALYSIS ===
    analysis_prompt = f"""
Analyze the {platform} video at {video_url} with title "{title}".

Provide:
1. Summary of content
2. 5+ likely topics
3. Emotional tone and style
4. Target audience
5. Content structure and flow

Output should be in {Language}.
"""
    messages = [
        SystemMessage(content=f"You are a video analyst for {platform}, fluent in {Language}."),
        HumanMessage(content=analysis_prompt)
    ]
    analysis_response = llm(messages)
    analysis_result = analysis_response.content

    # === 2. SEO GENERATION ===
    duration = video_metadata.get('duration', 0)
    minutes = duration // 60
    num_timestamps = min(15, max(5, int(minutes / 2))) if minutes > 0 else 5

    seo_prompt = f"""
Based on this analysis of a {platform} video titled "{title}":
{analysis_result}

Generate:
1. Exactly 35 trending tags
2. 400–500 word SEO description
3. {num_timestamps} timestamps with descriptions (video length: {duration}s)
4. 5-7 SEO title suggestions

Format:
{{
  "tags": [...],
  "description": "...",
  "timestamps": [{{"time": "00:00", "description": "..."}}],
  "titles": [{{"rank": 1, "title": "...", "reason": "..."}}]
}}

Respond ONLY with valid JSON. Language: {Language}.
"""
    messages = [
        SystemMessage(content=f"You are an SEO expert for {platform}, fluent in {Language}."),
        HumanMessage(content=seo_prompt)
    ]
    seo_response = llm(messages)
    seo_text = seo_response.content

    try:
        seo_result = json.loads(seo_text)
        if len(seo_result.get("tags", [])) != 35:
            seo_result["tags"] = ensure_exactly_35_tags(
                seo_result.get("tags", []), llm, video_metadata, platform, Language
            )
    except json.JSONDecodeError:
        try:
            json_start = seo_text.find('{')
            json_end = seo_text.rfind('}') + 1
            seo_result = json.loads(seo_text[json_start:json_end])
        except:
            seo_result = generate_fallback_seo(video_metadata, platform, Language)

    # === 3. THUMBNAIL CONCEPTS ===
    thumbnail_prompt = f"""
Based on the analysis of the {platform} video titled "{title}":
{analysis_result}

Generate 3 thumbnail concepts with:
1. Specific main visual
2. Text overlay (3–5 words max)
3. Color scheme (3 hex codes)
4. Focal point (main subject)
5. Emotional tone
6. Composition/layout details

Format:
{{
  "thumbnail_concepts": [
    {{
      "concept": "...",
      "text_overlay": "...",
      "colors": ["#hex1", "#hex2", "#hex3"],
      "focal_point": "...",
      "tone": "...",
      "composition": "..."
    }},
    ...
  ]
}}

Respond with valid JSON only. Language: {Language}.
"""
    messages = [
        SystemMessage(content=f"""
You are a thumbnail design strategist and creative director specializing in high-conversion thumbnails for {platform}.

Your job:
- Capture attention in feeds
- Use platform-optimized visuals
- Follow design psychology
- Suggest short bold text overlays
- Recommend effective color palettes
- Tailor layout to platform (e.g., bold for YouTube, minimal for Instagram, professional for LinkedIn)
"""),
        HumanMessage(content=thumbnail_prompt)
    ]
    thumbnail_response = llm(messages)
    thumbnail_text = thumbnail_response.content

    try:
        thumbnail_data = json.loads(thumbnail_text)
    except json.JSONDecodeError:
        try:
            json_start = thumbnail_text.find('{')
            json_end = thumbnail_text.rfind('}') + 1
            thumbnail_data = json.loads(thumbnail_text[json_start:json_end])
        except:
            thumbnail_data = {"thumbnail_concepts": []}

    return {
        "analysis": analysis_result,
        "seo": seo_result,
        "thumbnails": thumbnail_data
    }

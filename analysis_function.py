#from groq

import os
import json
from groq import Groq

def generate_fallback_seo(video_metadata, platform, language):
    return {
        "tags": ["default", "seo", "video", "fallback"] * 9,
        "description": f"No SEO data could be generated for this {platform} video.",
        "timestamps": [],
        "titles": []
    }

def ensure_exactly_35_tags(tags, client, video_metadata, platform, language):
    prompt = f"""
You provided {len(tags)} tags. Adjust them to exactly 35 relevant, high-performing tags for a video titled "{video_metadata.get('title')}" on {platform}. 
Return ONLY a JSON array of 35 tags.
"""
    response = client.chat.completions.create(
        model="gemma2-9b-it",
        messages=[
            {"role": "system", "content": f"You are an expert in optimizing tags for {platform}."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )
    try:
        return json.loads(response.choices[0].message.content)
    except:
        return tags[:35]

def analyze_video_with_groq(video_url, video_metadata, Language='English'):
    if not os.environ.get("GROQ_API_KEY"):
        raise Exception("GROQ_API_KEY is required for analysis")

    client = Groq(api_key=os.environ["GROQ_API_KEY"])
    platform = video_metadata.get('platform', 'YouTube')
    title = video_metadata.get('title', '')

    # 1. Analysis
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
    analysis_response = client.chat.completions.create(
        model="gemma2-9b-it",
        messages=[
            {"role": "system", "content": f"You are a video analyst for {platform}, fluent in {Language}."},
            {"role": "user", "content": analysis_prompt}
        ],
        temperature=0.7
    )
    analysis_result = analysis_response.choices[0].message.content

    # 2. SEO Generation
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

Format your output as:
{{
    "tags": ["tag1", "tag2", ..., "tag35"],
    "description": "...",
    "timestamps": [{{"time": "00:00", "description": "Intro"}}],
    "titles": [{{"rank": 1, "title": "...", "reason": "..."}}]
}}

Return ONLY valid JSON. All in {Language}.
"""
    seo_response = client.chat.completions.create(
        model="gemma2-9b-it",
        messages=[
            {"role": "system", "content": f"You are an SEO expert for {platform}, fluent in {Language}."},
            {"role": "user", "content": seo_prompt}
        ],
        temperature=0.7
    )
    seo_result_text = seo_response.choices[0].message.content
    try:
        seo_result = json.loads(seo_result_text)
        if len(seo_result.get("tags", [])) != 35:
            seo_result["tags"] = ensure_exactly_35_tags(
                seo_result.get("tags", []), client, video_metadata, platform, Language
            )
    except:
        try:
            json_start = seo_result_text.find('{')
            json_end = seo_result_text.rfind('}') + 1
            seo_result = json.loads(seo_result_text[json_start:json_end])
        except:
            seo_result = generate_fallback_seo(video_metadata, platform, Language)

    # 3. Thumbnails
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

Output format:
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
    thumbnail_response = client.chat.completions.create(
        model="gemma2-9b-it",
        messages=[
            {"role": "system", "content": f"You are a thumbnail design strategist for {platform}."},
            {"role": "user", "content": thumbnail_prompt}
        ],
        temperature=0.7
    )
    thumbnail_text = thumbnail_response.choices[0].message.content
    try:
        thumbnail_data = json.loads(thumbnail_text)
    except:
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



#from OpenAI


# import os
# import json
# import openai
# import streamlit as st

# from dotenv import load_dotenv
# load_dotenv()


# def generate_fallback_seo(video_metadata, platform, language):
#     return {
#         "tags": ["default", "seo", "video", "fallback"] * 9,
#         "description": f"No SEO data could be generated for this {platform} video.",
#         "timestamps": [],
#         "titles": []
#     }

# def ensure_exactly_35_tags(tags, client, video_metadata, platform, language):
#     prompt = f"""
#     You provided {len(tags)} tags. Adjust them to exactly 35 relevant, high-performing tags for a video titled "{video_metadata.get('title')}" on {platform}. 
#     Return ONLY a JSON array of 35 tags.
#     """
#     response = client.ChatCompletion.create(
#         model="gpt-4",
#         messages=[
#             {"role": "system", "content": f"You are an expert in optimizing tags for {platform}."},
#             {"role": "user", "content": prompt}
#         ],
#         temperature=0.7
#     )
#     try:
#         return json.loads(response.choices[0].message.content)
#     except:
#         return tags[:35]

# def analyze_video_with_openai(video_url, video_metadata, Language='English'):
#     """Analyze video content with platform-specific optimization using OpenAI."""
#     if not os.environ.get("OPENAI_API_KEY"):
#         raise Exception("OPENAI_API_KEY is required for analysis")

#     openai.api_key = os.environ["OPENAI_API_KEY"]
#     client = openai

#     platform = video_metadata.get('platform', 'YouTube')

#     analysis_prompt = f"""
#     Analyze the {platform} video at {video_url} with title "{video_metadata.get('title','')}".
#     Provide:
#     1. Summary of content
#     2. 5+ likely topics
#     3. Emotional tone and style
#     4. Target audience
#     5. Content structure and flow
#     Output should be in {Language}.
#     """

#     analysis_response = client.ChatCompletion.create(
#         model="gpt-4",
#         messages=[
#             {"role": "system", "content": f"You are a video analyst for {platform}, fluent in {Language}."},
#             {"role": "user", "content": analysis_prompt}
#         ],
#         temperature=0.7
#     )
#     analysis_result = analysis_response.choices[0].message.content

#     duration = video_metadata.get('duration', 0)
#     minutes = duration // 60
#     num_timestamps = min(15, max(5, int(minutes / 2))) if minutes > 0 else 5

#     seo_prompt = f"""
#     Based on this analysis of a {platform} video titled "{video_metadata.get('title','')}":
#     {analysis_result}
    
#     Generate:
#     1. Exactly 35 trending tags
#     2. 400–500 word SEO description
#     3. {num_timestamps} timestamps with descriptions (video length: {duration}s)
#     4. 5-7 SEO title suggestions

#     Format your output as:
#     {{
#         "tags": ["tag1", "tag2", ..., "tag35"],
#         "description": "...",
#         "timestamps": [{{"time": "00:00", "description": "Intro"}}],
#         "titles": [{{"rank": 1, "title": "...", "reason": "..."}}]
#     }}

#     Return ONLY valid JSON. All in {Language}.
#     """

#     seo_response = client.ChatCompletion.create(
#         model="gpt-4",
#         messages=[
#             {"role": "system", "content": f"You are an SEO expert for {platform}, fluent in {Language}."},
#             {"role": "user", "content": seo_prompt}
#         ],
#         temperature=0.7,
#     )

#     seo_result_text = seo_response.choices[0].message.content
#     try:
#         seo_result = json.loads(seo_result_text)
#         if len(seo_result.get("tags", [])) != 35:
#             seo_result["tags"] = ensure_exactly_35_tags(
#                 seo_result.get("tags", []), client, video_metadata, platform, Language
#             )
#     except json.JSONDecodeError:
#         try:
#             json_start = seo_result_text.find('{')
#             json_end = seo_result_text.rfind('}') + 1
#             if json_start >= 0 and json_end > json_start:
#                 seo_result = json.loads(seo_result_text[json_start:json_end])
#             else:
#                 seo_result = generate_fallback_seo(video_metadata, platform, Language)
#         except:
#             seo_result = generate_fallback_seo(video_metadata, platform, Language)

#     thumbnail_prompt = f"""
#     Based on the analysis of the {platform} video titled "{video_metadata.get('title','')}":
#     {analysis_result}

#     Generate 3 thumbnail concepts with:
#     1. Specific main visual
#     2. Text overlay (3–5 words max)
#     3. Color scheme (3 hex codes)
#     4. Focal point (main subject)
#     5. Emotional tone
#     6. Composition/layout details

#     Output format:
#     {{
#         "thumbnail_concepts": [
#             {{
#                 "concept": "...",
#                 "text_overlay": "...",
#                 "colors": ["#hex1", "#hex2", "#hex3"],
#                 "focal_point": "...",
#                 "tone": "...",
#                 "composition": "..."
#             }},
#             ...
#         ]
#     }}

#     Respond with valid JSON only. Language: {Language}.
#     """

#     thumbnail_response = client.ChatCompletion.create(
#         model="gpt-4",
#         messages=[
#             {"role": "system", "content": f"You are a thumbnail design strategist for {platform}."},
#             {"role": "user", "content": thumbnail_prompt}
#         ],
#         temperature=0.7
#     )

#     thumbnail_text = thumbnail_response.choices[0].message.content
#     try:
#         thumbnail_data = json.loads(thumbnail_text)
#     except json.JSONDecodeError:
#         try:
#             json_start = thumbnail_text.find('{')
#             json_end = thumbnail_text.rfind('}') + 1
#             thumbnail_data = json.loads(thumbnail_text[json_start:json_end])
#         except:
#             thumbnail_data = {"thumbnail_concepts": []}

#     return {
#         "analysis": analysis_result,
#         "seo": seo_result,
#         "thumbnails": thumbnail_data
#     }


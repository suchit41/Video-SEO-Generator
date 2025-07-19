# 🎯 Video SEO Optimizer

A powerful AI-driven Streamlit app that extracts metadata from YouTube, Instagram, LinkedIn (and other platforms) and generates SEO-ready assets in seconds using OpenAI or Groq + Gemma LLMs.

## 🚀 Features

- ✅ Generate 35 SEO-optimized tags  
- 📝 Auto-generate rich 500-word video descriptions  
- ⏱️ Smart timestamps (10%, 25%, 50%, etc. markers)  
- 🧠 AI-crafted catchy titles (5–7 variants)  
- 🎨 Thumbnail ideas (emotion, layout, elements)

## 📸 How It Works

1. Paste a video URL (YouTube, Instagram, LinkedIn, etc.)
2. Select a language (default: English)
3. Click **Generate SEO Assets**
4. Instantly receive:
   - Tags
   - Description
   - Timestamps
   - Suggested Titles
   - Thumbnail prompts

## 🧠 Built With

- [Streamlit](https://streamlit.io/) – for a fast and clean frontend
- [Groq](https://groq.com/) + [Gemma 2 9B](https://ai.google.dev/gemma) – ultra-fast LLM responses
- [OpenAI GPT-4o](https://openai.com/gpt-4) (fallback option)
- `asyncio`, `httpx`, `python-dotenv` – for efficient backend logic

## 🔧 Setup Instructions

### 1. Clone the repo

```bash
git clone https://github.com/your-username/video-seo-optimizer.git
cd video-seo-optimizer

import re
import requests  # Fixed: It was `request` in your original code
from urllib.parse import parse_qs, urlparse


def extract_video_id(url):
    """Extract video ID from various YouTube URL formats."""
    if not url:
        return None

    url = url.strip()

    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url

    pattern = r'(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:watch\?v=|embed\/|shorts\/)|youtu\.be\/)([\w-]{11})'
    match = re.search(pattern, url)
    if match:
        return match.group(1)

    parsed_url = urlparse(url)
    if 'youtube.com' in parsed_url.netloc:
        if 'watch' in parsed_url.path:
            query = parse_qs(parsed_url.query)
            return query.get('v', [None])[0]
        elif '/shorts/' in parsed_url.path:
            path_parts = parsed_url.path.split('/')
            try:
                return path_parts[path_parts.index('shorts') + 1]
            except (ValueError, IndexError):
                return None

    return None


def get_video_platform(url):
    """Determine the platform from the URL."""
    if not url:
        return "Unknown"

    url = url.strip().lower()

    if "youtube.com" in url or "youtu.be" in url:
        return "YouTube"
    elif "instagram.com" in url:
        return "Instagram"
    elif "linkedin.com" in url:
        return "LinkedIn"
    elif "facebook.com" in url or "fb.com" in url:
        return "Facebook"
    elif "tiktok.com" in url:
        return "TikTok"
    elif "twitter.com" in url or "x.com" in url:
        return "Twitter"
    else:
        return "Unknown"


def get_youtube_metadata(video_id):
    """Get metadata for a YouTube video with fallback mechanisms."""
    basic_metadata = {
        "title": f"YouTube video ({video_id})",
        "description": "",
        "thumbnail_url": f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg",
        "duration": 300,
        "views": 0,
        "author": "YouTube Creator",
        "platform": "YouTube",
        "video_id": video_id
    }

    try:
        url = f"https://www.youtube.com/watch?v={video_id}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9"
        }
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            html_content = response.text

            title_match = re.search(r'<meta property="og:title" content="([^"]+)"', html_content)
            if title_match:
                basic_metadata["title"] = title_match.group(1)

            author_match = re.search(r'<link itemprop="name" content="([^"]+)"', html_content)
            if author_match:
                basic_metadata["author"] = author_match.group(1)

            description_match = re.search(r'<meta property="og:description" content="([^"]+)"', html_content)
            if description_match:
                basic_metadata["description"] = description_match.group(1)

            duration_match = re.search(r'"lengthSeconds":"(\d+)"', html_content)
            if duration_match:
                try:
                    basic_metadata["duration"] = int(duration_match.group(1))
                except ValueError:
                    pass

            views_match = re.search(r'"viewCount":"(\d+)"', html_content)
            if views_match:
                try:
                    basic_metadata["views"] = int(views_match.group(1))
                except ValueError:
                    pass

            thumbnail_match = re.search(r'<meta property="og:image" content="([^"]+)"', html_content)
            if thumbnail_match:
                basic_metadata["thumbnail_url"] = thumbnail_match.group(1)

    except Exception as e:
        print(f"Error scraping YouTube page: {e}")

    # Fallback: oEmbed API
    try:
        oembed_url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={video_id}&format=json"
        oembed_response = requests.get(oembed_url)

        if oembed_response.status_code == 200:
            oembed_data = oembed_response.json()
            if 'title' in oembed_data:
                basic_metadata["title"] = oembed_data['title']
            if 'author_name' in oembed_data:
                basic_metadata["author"] = oembed_data['author_name']
            if 'thumbnail_url' in oembed_data:
                basic_metadata["thumbnail_url"] = oembed_data['thumbnail_url']
    except Exception as e:
        print(f"Error using oEmbed fallback: {e}")

    return basic_metadata


def get_video_metadata(url):
    """Get video metadata based on platform."""
    if not url:
        raise ValueError("Please enter a video URL")

    platform = get_video_platform(url)

    if platform == "YouTube":
        video_id = extract_video_id(url)
        if not video_id:
            raise ValueError("Could not extract video ID from URL. Please use a standard YouTube URL.")
        return get_youtube_metadata(video_id)
    else:
        return {
            "title": "Video on " + platform,
            "description": "",
            "thumbnail_url": f"https://via.placeholder.com/1280x720?text={platform}",
            "duration": 300,
            "views": 0,
            "author": platform + " Creator",
            "platform": platform,
            "video_id": "Unknown"
        }

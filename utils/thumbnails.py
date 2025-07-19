from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
import os
import colorsys
import math


def generate_thumbnail_with_dalle(client, concept, video_title, platform="YouTube"):
    """Generate a thumbnail image using DALL-E based on the concept and video title."""
    try:
        if platform == "YouTube":
            aspect_ratio = "16:9"
            size = "1792x1024"
        elif platform == "Instagram":
            aspect_ratio = "1:1"
            size = "1024x1024"
        elif platform == "LinkedIn":
            aspect_ratio = "1.91:1"
            size = "1792x1024"
        else:
            aspect_ratio = "16:9"
            size = "1792x1024"

        text_overlay = concept.get('text_overlay', '')
        focal_point = concept.get('focal_point', '')
        tone = concept.get('tone', '')
        concept_desc = concept.get('concept', '')

        colors = concept.get('colors', ['#FFFFFF', '#000000'])
        main_color = colors[0] if len(colors) > 0 else '#FFFFFF'

        prompt = f"""
        Create a professional {platform} thumbnail with these specifications:
        - Clear {aspect_ratio} format for {platform}
        - Main Focus: {focal_point}
        - Emotional tone: {tone}
        - Bold, clear text overlay reading "{text_overlay}" prominently displayed
        - Text should be highly legible, possibly in color {main_color} with contrasting outline
        - Concept: {concept_desc}
        - Relatable to: {video_title}
        - Professional, eye-catching design with high contrast
        - Make sure the text stands out and is easily readable
        - Text should be integrated with the visual elements in a visually appealing way
        """

        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size=size,
            quality="standard",
            n=1,
        )

        image_url = response.data[0].url
        return image_url

    except Exception as e:
        print(f"Error while generating thumbnail with DALL-E: {e}")
        return None


def hex_to_rgb(hex_color):
    """Convert hex color to RGB tuple."""
    hex_color = hex_color.lstrip('#')
    lv = len(hex_color)
    return tuple(int(hex_color[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))


def create_gradient_background(concept, width=1280, height=720):
    """Create a vertical gradient background using the colors from the concept."""
    colors = concept.get('colors', ['#3366CC', '#FFFFFF', '#FF5555'])

    if len(colors) < 2:
        colors.append('#FFFFFF')  # Ensure at least two colors

    try:
        # Convert hex to RGB
        rgb_colors = [hex_to_rgb(c) for c in colors]

        # Create a blank image
        gradient = Image.new("RGB", (width, height), rgb_colors[0])
        draw = ImageDraw.Draw(gradient)

        num_segments = len(rgb_colors) - 1
        segment_height = height // num_segments

        for i in range(num_segments):
            top_color = rgb_colors[i]
            bottom_color = rgb_colors[i + 1]

            for y in range(segment_height):
                ratio = y / segment_height
                r = int(top_color[0] * (1 - ratio) + bottom_color[0] * ratio)
                g = int(top_color[1] * (1 - ratio) + bottom_color[1] * ratio)
                b = int(top_color[2] * (1 - ratio) + bottom_color[2] * ratio)
                draw.line([(0, i * segment_height + y), (width, i * segment_height + y)], fill=(r, g, b))

        return gradient

    except Exception as e:
        print(f"Error creating gradient: {e}")
        return None

def preview_image_from_url(image_url):
    """Download image from URL and preview it using matplotlib."""
    try:
        response = requests.get(image_url)
        img = Image.open(BytesIO(response.content))

        plt.figure(figsize=(10, 6))
        plt.imshow(img)
        plt.axis("off")
        plt.title("Generated Thumbnail Preview")
        plt.show()
    except Exception as e:
        print(f"Error displaying preview image: {e}")


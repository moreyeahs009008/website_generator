import os
import anthropic
from bs4 import BeautifulSoup  # For HTML validation and correction
from typing import Dict, Any

# Initialize Anthropic client with secure API key management
client = anthropic.Anthropic(
    api_key="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"
)

def validate_and_correct_html(html_code: str) -> str:
    """
    Validates and corrects the generated HTML structure.
    Ensures it includes <html>, <head>, and <body> tags.
    """
    try:
        soup = BeautifulSoup(html_code, 'html.parser')

        # Ensure basic structure
        if not soup.html:
            soup.insert(0, soup.new_tag("html"))
        if not soup.head:
            head_tag = soup.new_tag("head")
            meta_tag = soup.new_tag("meta", charset="UTF-8")
            title_tag = soup.new_tag("title")
            title_tag.string = "Professional Website"
            head_tag.extend([meta_tag, title_tag])
            soup.html.insert(0, head_tag)
        if not soup.body:
            body_tag = soup.new_tag("body")
            for content in soup.contents:
                if content.name not in ["html", "head"]:
                    body_tag.append(content.extract())
            soup.html.append(body_tag)

        return str(soup)
    except Exception as e:
        print(f"HTML correction error: {e}")
        return html_code  # Return original code if correction fails

def generate_website(name: str, profession: str,color_input:str) -> str:
    """
    Generate a professional website based on person's name and profession.
    """
    system_prompt = """
    You are a skilled web developer specializing in creating modern, professional websites.
    The website should include:
    
    1. <!DOCTYPE html> declaration
    2. A complete <html> structure with proper <head> and <body> tags.
    3. Navigation bar with sections like Home, About, Services, Testimonials, and Contact.
    4. A hero section with a strong headline and clear call-to-action.
    5. An about section highlighting expertise, achievements, and certifications.
    6. Services section customized for the specified profession.
    7. A team section (if applicable) or individual profile details.
    8. Testimonials from satisfied clients or partners.
    9. A contact form with clear CTA (Call-to-Action).
    10. Footer with contact details, social links, and copyright information.

    Use:
    - Bootstrap 5 for layout and responsiveness.
    - Font Awesome for icons.
    - Clean, modern, and professional color schemes based on the profession.
    - Ensure the code is clean, organized, and follows best practices.
    
    Return only the complete HTML code (no additional text or comments).
    """
    user_prompt = f"""
    Create a complete website for {name}, who is a {profession}.
    The website should focus on attracting potential clients in the {profession} field.

    Include:
    - Profession-specific terminology
    - Customized service descriptions
    - Relevant images (use placeholder links)
    - Effective color schemes and design styles that fit a {profession}'s online presence
    - Incorporate the following color scheme for cohesive design: {color_input}

    """
    try:
        print("Generating website...")
        response = client.messages.create(
            model="claude-3-7-sonnet-20250219",
            max_tokens=4000,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}]
        )

        html_code = response.content
        print("Website generated!!!")
        # corrected_html = validate_and_correct_html(html_code)
        return html_code[0].text.strip()

    except Exception as e:
        print(f"Error occurred: {e}")
        return ""

def save_website(html_code: str, name: str, profession: str) -> str:
    """
    Save the generated website to a file.
    """
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    filename = f"{output_dir}/{name.lower().replace(' ', '-')}-{profession.lower().replace(' ', '-')}.html"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_code)

    return filename


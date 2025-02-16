import requests
import os
import asyncio
from flask import Flask, render_template, request, Response
import cohere
from pyppeteer import launch  # Use Pyppeteer for generating PDFs
import nest_asyncio
from playwright.sync_api import sync_playwright
import markdown2
nest_asyncio.apply()


app = Flask(__name__)

# Load API Keys
UNSPLASH_ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY")  # Unsplash API Key
COHERE_API_KEY = os.getenv("COHERE_API_KEY")  # Cohere API Key
co = cohere.Client(COHERE_API_KEY)

# Function to fetch Unsplash images
def get_unsplash_image(query):
    url = f"https://api.unsplash.com/photos/random?query={query}&client_id={UNSPLASH_ACCESS_KEY}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        image_url = data["urls"]["regular"]
        print(f"✅ Image found for '{query}': {image_url}")  # Debugging Output
        return image_url
    
    print(f"❌ Unsplash API error ({response.status_code}): {response.text}")  # Debug output
    return None  # Return None if request fails

# Function to generate AI-powered itinerary
# def generate_itinerary(destination, days):
#     prompt = f"""
#     Generate a {days}-day travel itinerary for {destination} with activities, food, and sightseeing.
#     Format it as:
#     - "## Day X: Title" for day headers
#     - "**Morning:**", "**Afternoon:**", "**Evening:**, "**Night:**" for sections
#     - Keep paragraphs structured and avoid unnecessary new lines.
#     """
#     response = co.generate(
#         model="command",
#         prompt=prompt,
#         max_tokens=2048
#     )
#     return response.generations[0].text.strip()

def generate_itinerary(destination, days):
    prompt = f"""
    Generate a {days}-day travel itinerary for {destination} with activities, food, and sightseeing.
    Format it using Markdown:
    - "## Day X: Title" for day headers
    - "**Morning:**", "**Afternoon:**", "**Evening:**, "**Night:**" for sections
    - Ensure all sections are properly structured.
    """
    response = co.generate(
        model="command",
        prompt=prompt,
        max_tokens=2048
    )
    
    raw_itinerary = response.generations[0].text.strip()

    # Convert Markdown to HTML
    formatted_itinerary = markdown2.markdown(raw_itinerary)
    return raw_itinerary



def convert_html_to_pdf(html):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.set_content(html, wait_until="networkidle")
        
        # Generate PDF with styles/images included
        pdf = page.pdf(format="A4", print_background=True)
        
        browser.close()
        return pdf


# Main Route (Handles Form Submission & Image Fetching)
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        destination = request.form['destination']
        days = request.form['days']
        itinerary = generate_itinerary(destination, days)

        # Fetch Unsplash images
        cover_image = get_unsplash_image(f"{destination} landscape")

        print(f"📸 Cover Image: {cover_image}")

        return render_template('result.html', 
                               itinerary=itinerary, 
                               destination=destination, 
                               cover_image=cover_image)
    
    return render_template('index.html')

# Route for PDF Download (Uses Pyppeteer to Keep Styling)
@app.route('/download', methods=['POST'])
def download_pdf():
    itinerary_html = request.form['itinerary']
    destination = request.form.get("destination", "Itinerary")

    # Generate full HTML with Tailwind styles applied
    styled_html = render_template("result.html", itinerary=itinerary_html, destination=destination)

    # Convert to PDF using Playwright
    pdf = convert_html_to_pdf(styled_html)

    # Serve the PDF as a downloadable file
    response = Response(pdf, mimetype="application/pdf")
    response.headers["Content-Disposition"] = f"attachment; filename={destination.replace(' ', '_')}_itinerary.pdf"
    return response




if __name__ == '__main__':
    app.run(debug=True)

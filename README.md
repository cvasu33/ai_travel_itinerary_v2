🗺️ AI Travel Itinerary Generator

This is a Flask web app that generates a personalized travel itinerary 
using AI-powered text generation (Cohere API) and fetches relevant 
destination images from Unsplash. Users can enter a destination and trip 
duration, then download a styled PDF itinerary.

🚀 Getting Started

1️⃣ Clone the Repository

    git clone https://github.com/cvasu33/ai_travel_itinerary_v2.git
    cd ai_travel_itinerary_v2

2️⃣ Create a Virtual Environment

To avoid conflicts with system packages, set up a virtual environment:

# macOS/Linux

    python3 -m venv venv
    source venv/bin/activate

# Windows
    python -m venv venv
    venv\Scripts\activate

3️⃣ Install Dependencies

pip install -r requirements.txt

4️⃣ Set Up API Keys

This app requires API keys from Cohere (AI text generation) and Unsplash 
(destination images).
🔹 Create a .env file in the project directory and add:

COHERE_API_KEY=your_cohere_api_key
UNSPLASH_ACCESS_KEY=your_unsplash_api_key

    Replace your_cohere_api_key and your_unsplash_api_key with your actual 
API keys.

5️⃣ Run the Flask App

python app.py

Once running, open your browser and visit:

http://127.0.0.1:5000/

6️⃣ Generate an Itinerary

1️⃣ Enter a destination and number of days
2️⃣ Click Generate Itinerary
3️⃣ View and download a PDF version with styling

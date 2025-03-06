from flask import Flask, render_template, request, redirect, url_for
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env

app = Flask(__name__)


GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY") # Securely load API key from environment variable

if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in environment variables.  Set it in a .env file or environment.")

genai.configure(api_key=GOOGLE_API_KEY)


def get_repairability_score(image_file):
    """
    Calls the Gemini API to get a repairability score for the clothing item.

    Args:
        image_file: The Flask UploadedFile object.

    Returns:
        An integer representing the repairability score (1-10), or None if there was an error.
    """
    try:
        model = genai.GenerativeModel('gemini-1.5-flash') # using older model since newer one (gemini-2.0-flash) is experimental and may not give reliable responses

        # Prompt to gemini for assessing repairability score
        prompt = """Analyze the image of the clothing item and estimate its repairability on a scale of 1 to 10,
        where 1 means completely unrepairable and 10 means easily repairable.
        Consider factors like the type of damage (rips, stains, missing buttons, etc.),
        the fabric type, and the overall condition of the garment. Just return the number only"""

        # Get the image data as bytes from the file object
        image_data = image_file.read()

        img = {'mime_type': image_file.mimetype, 'data': image_data}  

        response = model.generate_content([prompt, img])
        print(response.text) 

        # Extract the numerical score from the response
        try:
            score = int(response.text.strip())  # Remove whitespace with strip and convert
            if 1 <= score <= 10: # i.e. valld score
                return score
            else:
                print(f"Warning: Gemini returned an invalid score: {score}") # invalid value found
                return None  
        except ValueError: # any other random error
            print(f"Error: Could not extract numerical score from Gemini response: {response.text}")
            return None

    except Exception as e: # if some error with calling gemini happens
        print(f"Error calling Gemini API: {e}")  
        return None

def find_donation_centers_near(city):
    """
    Uses Gemini to find the 5 closest donation centers to the given address.

    Args:
        city: The company city entered by the user.

    Returns:
        A list of strings, where each string is the name/address of a donation center.
        Returns an empty list if no centers are found or if there's an error.
    """
    try:
        model = genai.GenerativeModel('gemini-1.5-flash') # using older model since newer one (gemini-2.0-flash) is experimental and may not give reliable responses
        prompt = f"""You are a helpful assistant, you are going to return 5 clothing charities/donation centres in the following city: {city}. 
        Just return the location name (with the address) for each donation centre/charity. Each on a new line."""

        response = model.generate_content(prompt)
        print(response.text) 

        # Extract donation center names from the response
        donation_centers = [line.strip() for line in response.text.splitlines() if line.strip()] #Splits the line

        return donation_centers # return the computed donation centers
    except Exception as e:
        print(f"Error finding donation centers: {e}")
        return []

@app.route("/")
def splash_page():
    return render_template("splash.html")

@app.route("/main", methods=["GET", "POST"])
def main_page():
    if request.method == "POST":
        if "clothing_image" not in request.files:
            return "No file part"  # Handle no file uploaded
        file = request.files["clothing_image"]
        if file.filename == "":
            return "No selected file"  # Handle empty filename
        if file:
            # Pass the file object directly to get_repairability_score to get the needed score
            repairability_score = get_repairability_score(file)

            if repairability_score is None: # error checking for repairability score
                return "Error: Could not determine repairability.  Please try again."
            
            if repairability_score >= 8: # aka good to resell
                return render_template("result.html", message="This item is likely resalable!")
            elif 5 <= repairability_score <= 7: # aka good to donate
                return redirect(url_for("donation_centers_page"))
            else: # aka trash
                return render_template("result.html", message="This item is likely not repairable and should be discarded.")

    return render_template("index.html")  # Initial page with image upload form

@app.route("/donation_centers")
def donation_centers_page():
    return render_template("donation_centers.html")

@app.route("/find_centers", methods=["POST"])
def find_centers():
    city = request.form.get("city")  # Get the city from the form
    if not city:
        return "Error: No address provided."

    donation_centers = find_donation_centers_near(city)

    return render_template("donation_centers.html", donation_centers=donation_centers)

if __name__ == "__main__":
    app.run(debug=True)
"""
This module implements a Flask web server to detect emotions in provided text.
"""

from flask import Flask, request, jsonify, render_template
from EmotionDetection import emotion_detector

app = Flask(__name__)


def home():
    """Render the home page."""
    return render_template("index.html")

@app.route("/emotionDetector", methods=["GET"])
def detect_emotion():
    """Detect emotion from the provided text and return a formatted response."""
    # Retrieve the text from the URL
    text_to_analyze = request.args.get("textToAnalyze", "")

    # Debugging: Print the received text to the console
    print(f"Received text: {text_to_analyze}")

    # Validate input
    if text_to_analyze is None or not text_to_analyze.strip():  # Check for None or empty string
        return "Invalid text! Please try again!", 400

    # Call the emotion detection function
    result = emotion_detector(text_to_analyze)

    # Handle case where dominant_emotion is None
    if result["dominant_emotion"] is None:
        return "Invalid text! Please try again!", 400

    # Format the output
    formatted_response = (
        f"For the given statement, the system response is "
        f"'anger': {result['anger']}, 'disgust': {result['disgust']}, "
        f"'fear': {result['fear']}, 'joy': {result['joy']} and "
        f"'sadness': {result['sadness']}. "
        f"The dominant emotion is {result['dominant_emotion']}."
    )

    return jsonify({"response": formatted_response})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

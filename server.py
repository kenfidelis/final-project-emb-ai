#!/usr/bin/env python3
"""
Flask Web Application for Emotion Detection.

This module provides a web interface for emotion detection using IBM Watson NLP service.
It includes routes for rendering the main page and processing emotion detection requests.

Author: Ekene
Date: 2025
"""
from flask import Flask, render_template, request
from EmotionDetection import emotion_detector

# Initialize the Flask application
app = Flask(__name__)


@app.route("/")
def render_index_page():
    """
    Render the main index page.
    
    Returns:
        str: Rendered HTML template for the index page
    """
    return render_template('index.html')


@app.route("/emotionDetector")
def emotion_detector_route():
    """
    Flask route for emotion detection.
    
    This function receives text input via GET parameters and returns a formatted 
    emotion analysis response. It handles empty input and error cases by returning 
    appropriate error messages.
    
    Returns:
        str: Formatted emotion analysis response or error message
    """
    # Get the text to analyze from the request arguments
    text_to_analyze = request.args.get('textToAnalyze')
    # Handle empty or None input
    if not text_to_analyze or text_to_analyze.strip() == "":
        return "Invalid text! Please try again!"
    # Call the emotion detector function
    response = emotion_detector(text_to_analyze)
    # Handle error response or when dominant_emotion is None
    if response is None or response.get('dominant_emotion') is None:
        return "Invalid text! Please try again!"
    # Extract emotion scores
    anger = response['anger']
    disgust = response['disgust']
    fear = response['fear']
    joy = response['joy']
    sadness = response['sadness']
    dominant_emotion = response['dominant_emotion']
    # Format the response according to requirements
    formatted_response = (
        f"For the given statement, the system response is "
        f"'anger': {anger}, 'disgust': {disgust}, 'fear': {fear}, "
        f"'joy': {joy} and 'sadness': {sadness}. "
        f"The dominant emotion is <b>{dominant_emotion}</b>.")    
    return formatted_response

if __name__ == '__main__':
    # Run the Flask application on localhost:5000
    app.run(host='0.0.0.0', port=5000, debug=True)
   
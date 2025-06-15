import requests
import json

def emotion_detector(text_to_analyze):
    """
    Analyze emotion in text using IBM Watson NLP service
    
    Args:
        text_to_analyze (str): The text to analyze for emotions
    
    Returns:
        dict: Formatted dictionary with emotion scores and dominant emotion
              Returns None values for all keys if status_code is 400 or error occurs
    """
    
    # Check for blank or empty input
    if not text_to_analyze or text_to_analyze.strip() == "":
        return {
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'dominant_emotion': None
        }
    
    url = "https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
    
    headers = {
        "grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock",
        "Content-Type": "application/json"
    }
    
    payload = {
        "raw_document": {
            "text": text_to_analyze
        }
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        
        # Check for status code 400 (Bad Request)
        if response.status_code == 400:
            return {
                'anger': None,
                'disgust': None,
                'fear': None,
                'joy': None,
                'sadness': None,
                'dominant_emotion': None
            }
        
        response.raise_for_status()
        
        # Parse the JSON response
        response_data = response.json()
        
        # Handle different possible response structures
        emotion_predictions = None
        
        # Try different possible paths to emotion data
        if 'emotionPredictions' in response_data:
            emotion_predictions = response_data['emotionPredictions'][0]['emotion']
        elif 'emotion' in response_data:
            emotion_predictions = response_data['emotion']
        elif 'predictions' in response_data:
            emotion_predictions = response_data['predictions'][0]['emotion']
        else:
            # If the response structure is different, try to find emotion data
            # Look for keys that might contain emotion scores
            for key, value in response_data.items():
                if isinstance(value, list) and len(value) > 0:
                    if 'emotion' in value[0]:
                        emotion_predictions = value[0]['emotion']
                        break
                elif isinstance(value, dict) and 'emotion' in value:
                    emotion_predictions = value['emotion']
                    break
        
        # If still no emotion data found, assume the response itself contains the scores
        if emotion_predictions is None:
            emotion_predictions = response_data
        
        # Extract required emotions and their scores
        anger_score = emotion_predictions.get('anger', 0)
        disgust_score = emotion_predictions.get('disgust', 0)
        fear_score = emotion_predictions.get('fear', 0)
        joy_score = emotion_predictions.get('joy', 0)
        sadness_score = emotion_predictions.get('sadness', 0)
        
        # Create a dictionary of emotions and scores for finding dominant emotion
        emotions = {
            'anger': anger_score,
            'disgust': disgust_score,
            'fear': fear_score,
            'joy': joy_score,
            'sadness': sadness_score
        }
        
        # Find the dominant emotion (emotion with highest score)
        dominant_emotion = max(emotions, key=emotions.get)
        
        # Return formatted output
        return {
            'anger': anger_score,
            'disgust': disgust_score,
            'fear': fear_score,
            'joy': joy_score,
            'sadness': sadness_score,
            'dominant_emotion': dominant_emotion
        }
    
    except requests.exceptions.RequestException as e:
        # Return None values in case of error
        return {
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'dominant_emotion': None
        }
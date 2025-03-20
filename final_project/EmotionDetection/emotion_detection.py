import requests
import json

def emotion_detector(text_to_analyze):
    # Define Watson NLP Emotion Prediction API endpoint
    url = "https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
    
    # Set headers for the API request
    headers = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    
    # Define the input JSON payload
    payload = {
        "raw_document": {
            "text": text_to_analyze
        }
    }
    
    # Send a POST request to Watson NLP API
    response = requests.post(url, headers=headers, json=payload)
    
    # Handle possible errors
    if response.status_code != 200:
        return {"error": f"Request failed with status code {response.status_code}"}
    
    # Parse the response JSON
    response_data = response.json()
    
    # Extract emotion scores
    emotions = response_data.get("emotionPredictions", [{}])[0].get("emotion", {})

    # Filter only required emotions
    required_emotions = { 
        "anger": emotions.get("anger", 0), 
        "disgust": emotions.get("disgust", 0), 
        "fear": emotions.get("fear", 0), 
        "joy": emotions.get("joy", 0), 
        "sadness": emotions.get("sadness", 0) 
    }
    
    # Determine the dominant emotion
    dominant_emotion = max(required_emotions, key=required_emotions.get)
    
    # Add dominant emotion to the dictionary
    required_emotions["dominant_emotion"] = dominant_emotion
    
    return required_emotions

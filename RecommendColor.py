import functions_framework
import vertexai
from vertexai.language_models import TextGenerationModel
import random
import time
import json

vertexai.init(project="your-project-id", location="us-central1")
parameters = {
    "candidate_count": 1,
    "max_output_tokens": 1024,
    "temperature": 0.1,
    "top_p":0.8,
    "top_k":40,
}

color_meanings = {
    "Sunday": {
        "subordinates": ["red"],
        "health": ["white", "cream", "yellow"],
        "power_and_fortune": ["pink"],
        "fortune_enhancement": ["green", "purple"],
        "elder_support": ["grey", "black"],
        "avoid": ["blue", "navy"]
    },
    "Monday": {
        "subordinates": ["yellow", "white", "cream"],
        "health": ["pink"],
        "power_and_fortune": ["green"],
        "fortune_enhancement": ["orange", "gold"],
        "elder_support": ["blue"],
        "avoid": ["red"]
    },
    "Tuesday": {
        "subordinates": ["pink"],
        "health": ["green"],
        "power_and_fortune": ["purple"],
        "fortune_enhancement": ["orange", "grey", "black"],
        "elder_support": ["red"],
        "avoid": ["yellow", "cream", "white"]
    },
    "Wednesday": {
        "subordinates": ["black", "grey"],
        "health": ["purple"],
        "power_and_fortune": ["gold", "red"],
        "fortune_enhancement": ["green"],
        "elder_support": ["grey", "black", "yellow", "cream", "red", "green"],
        "avoid": ["gold", "orange"]
    },
    "Thursday": {
        "subordinates": ["orange", "bright orange"],
        "health": ["grey", "black"],
        "power_and_fortune": ["white", "yellow", "cream"],
        "fortune_enhancement": ["red"],
        "elder_support": ["green"],
        "avoid": ["black", "purple"]
    },
    "Friday": {
        "subordinates": ["blue", "sea blue", "sky blue"],
        "health": ["red"],
        "power_and_fortune": ["yellow", "cream", "white"],
        "fortune_enhancement": ["pink"],
        "elder_support": ["purple", "orange", "gold"],
        "avoid": ["grey", "black"]
    },
    "Saturday": {
        "subordinates": ["black", "grey", "dark purple"],
        "health": ["blue", "navy"],
        "power_and_fortune": ["pink"],
        "fortune_enhancement": ["red"],
        "elder_support": ["pink"],
        "avoid": ["green"]
    }
}

@functions_framework.http
def entrypoint(request):
    """HTTP Cloud Function.
    """
    # Set CORS headers for the preflight request
    if request.method == 'OPTIONS':
        # Allows GET requests from any origin with the Content-Type
        # header and caches preflight response for an 3600s
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }
        return ('', 204, headers)

    # Set CORS headers for the main request
    headers = {
        'Access-Control-Allow-Origin': '*'
    }
    request_json = request.get_json(silent=True)

    if not request_json or 'date' not in request_json:
        date = "Monday"
    else:
        date = request_json['date']

    model = TextGenerationModel.from_pretrained("text-bison")
    response = model.predict(
        f"""Given the data structure containing auspicious color information for people born on different days of the week, provide a detailed description of the color meanings for a person born on {date}. 
        The data includes categories such as colors beneficial from {color_meanings[date]} for subordinates, health, power, fortune, fortune enhancement, elder support, and colors to avoid. Reply in Thai""",
        **parameters
    )
    result_json = {'conclusion': response.text}
    return (json.dumps(result_json, ensure_ascii=False), 200, headers)





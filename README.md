# Lightweight AI REST Service

This is a small proof of concept for a text-based classifier. You can enter a sentence and get a prediction of 
what you said about your health state should be followed up. Possible outcome labels are: `low_concern`, `needs_follow_up` and `urgent_review`.

Disclaimer: this is a technical prototype and NOT a medical product. Please do not use this to self-diagnose.

## Getting started :seedling:
### Prerequisites
* you need to have a Docker installation

### Steps
1. Clone the repository
2. Build and run the docker container
```
docker build -t health-ai-service .
docker run --rm -p 8000:8000 health-ai-service
```
3. Check the health service status
```
curl http://localhost:8000/health
```

## Usage :speech_balloon:

### API Endpoints
| Method | Endpoint | Description                                                                           |
|--------|----------|---------------------------------------------------------------------------------------|
| GET    | /health  | Returns whether the service is running.                                               |
| POST   | /analyze | Receives a JSON object with a text field and returns a classification and confidence. |

### GET /health
Returns whether the service is running.

#### Example request
```
curl http://localhost:8000/health
```

#### Example response
```
{"status":"ok"}
```


### POST /analyze
Receives a JSON object with a text field and returns a classification and confidence.

#### Example request
```
curl -X POST http://localhost:8000/analyze -H "Content-Type: application/json" -d '{"text": "I have chest pain and shortness of breath."}'
```

> [!TIP]
> If you are on a Windows machine, you might need to replace curl with curl.exe or use the Powershell with the command below:
> ```
> Invoke-WebRequest -Uri http://localhost:8000/analyze `
>   -Method POST `
>   -ContentType "application/json" `
>   -Body '{"text": "I have chest pain and shortness of breath."}'
> ```


#### Example response
```
{
    "confidence":0.71,
    "label":"urgent_review"
}
```

## How it works :gear:
The API service is based on Flask and uses the [all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) sentence transformer model.

1. Reference texts have been created and embedded in the model
2. When the user inputs a text, it is embedded as well
3. The cosine similarity is computed between the user's text and the reference texts
4. For each label the similarity scores are averaged (between all the individual reference text to user text scores)
5. The highest similarity label is returned to the user
6. The confidence is computed by taking the softmax of the similarity scores of the labels

## Support :paperclip:
If you have a suggestion or found a bug, please open an issue.
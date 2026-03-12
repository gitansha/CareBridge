import requests
from opentelemetry import baggage, context
from opentelemetry.instrumentation.requests import RequestsInstrumentor

# Instrument requests for OpenTelemetry
RequestsInstrumentor().instrument()

# API configuration
api_key = "sk-qmEXHlEC7q-6NKWMJkUgUw"
base_url = "https://genai-models-nonprod.sq.com.sg"
entrypoint = "sample"

# Set up OpenTelemetry baggage context
baggage_ctx = baggage.set_baggage("entrypoint", entrypoint)
token = context.attach(baggage_ctx)

# Request headers
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}",
}

# API endpoint
url = f"{base_url}/v1/chat/completions"

# Payload with Claude Haiku 4.5
payload = {
    "model": "claude-haiku-4-5-20251001",
    "messages": [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Tell me a fun fact about artificial intelligence!"},
    ],
    "metadata": {"tags": ["test-haiku-4.5", "experimental"]}
}

print("Testing Claude Haiku 4.5...")
print(f"URL: {url}")
print(f"Model: {payload['model']}")
print(f"User message: {payload['messages'][1]['content']}\n")

try:
    response = requests.post(url, headers=headers, json=payload, verify=False)
    response.raise_for_status()
    
    data = response.json()
    print("=" * 60)
    print("Claude Haiku 4.5 Response:")
    print("=" * 60)
    
    # Pretty print the response
    if 'choices' in data and len(data['choices']) > 0:
        assistant_message = data['choices'][0]['message']['content']
        print(f"\nAssistant: {assistant_message}\n")
    
    print("\nFull response data:")
    import json
    print(json.dumps(data, indent=2))
    
except requests.exceptions.RequestException as e:
    print(f"Error calling API: {e}")
    if hasattr(e, 'response') and e.response is not None:
        print(f"Status Code: {e.response.status_code}")
        print(f"Response: {e.response.text}")

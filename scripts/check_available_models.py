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

# Try to get models list from the API
models_url = f"{base_url}/v1/models"

print("Querying available models...")
print(f"URL: {models_url}\n")

try:
    response = requests.get(models_url, headers=headers, verify=False)
    response.raise_for_status()
    
    data = response.json()
    print("=" * 60)
    print("Available Models:")
    print("=" * 60)
    
    import json
    print(json.dumps(data, indent=2))
    
    # Check if haiku is available
    if 'data' in data:
        print("\n" + "=" * 60)
        print("Model IDs:")
        print("=" * 60)
        haiku_found = False
        for model in data['data']:
            model_id = model.get('id', 'N/A')
            print(f"  - {model_id}")
            if 'haiku' in model_id.lower() or 'claude' in model_id.lower():
                haiku_found = True
                print(f"    ✓ Found Claude/Haiku model!")
        
        if not haiku_found:
            print("\n⚠️  No Haiku/Claude models found in the list")
    
except requests.exceptions.RequestException as e:
    print(f"Error calling API: {e}")
    if hasattr(e, 'response') and e.response is not None:
        print(f"Status Code: {e.response.status_code}")
        print(f"Response: {e.response.text}")

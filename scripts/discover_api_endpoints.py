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

import json

# Common OpenAI-compatible API endpoints to try
endpoints_to_test = [
    "/v1/models",
    "/v1/chat/completions",
    "/v1/completions",
    "/v1/embeddings",
    "/v1/audio/transcriptions",
    "/v1/audio/translations",
    "/v1/audio/speech",
    "/v1/images/generations",
    "/v1/moderations",
    "/v1/files",
    "/",
    "/v1",
    "/health",
    "/status",
    "/api/v1/models",
]

print("=" * 70)
print("TESTING API ENDPOINTS")
print("=" * 70)

results = {}

for endpoint in endpoints_to_test:
    url = f"{base_url}{endpoint}"
    print(f"\nTesting: {endpoint}")
    print(f"  URL: {url}")
    
    try:
        # Try GET first
        response = requests.get(url, headers=headers, verify=False, timeout=5)
        
        if response.status_code == 200:
            print(f"  ✓ Status: {response.status_code} (GET)")
            try:
                data = response.json()
                print(f"  Response preview: {json.dumps(data, indent=4)[:200]}...")
                results[endpoint] = {"method": "GET", "status": response.status_code, "response": data}
            except:
                print(f"  Response text: {response.text[:100]}")
                results[endpoint] = {"method": "GET", "status": response.status_code, "response": response.text}
        elif response.status_code == 405:  # Method not allowed, might need POST
            print(f"  ⚠ Status: {response.status_code} (GET not allowed, endpoint might need POST)")
            results[endpoint] = {"method": "GET", "status": response.status_code, "note": "Might require POST"}
        elif response.status_code == 404:
            print(f"  ✗ Status: {response.status_code} (Not Found)")
        else:
            print(f"  ? Status: {response.status_code}")
            results[endpoint] = {"method": "GET", "status": response.status_code}
            
    except requests.exceptions.Timeout:
        print(f"  ✗ Timeout")
    except requests.exceptions.RequestException as e:
        print(f"  ✗ Error: {str(e)[:100]}")

print("\n" + "=" * 70)
print("SUMMARY OF WORKING ENDPOINTS")
print("=" * 70)

for endpoint, info in results.items():
    if info.get("status") == 200:
        print(f"✓ {endpoint} - {info['method']} - {info['status']}")
    elif info.get("status") == 405:
        print(f"⚠ {endpoint} - Needs POST method")

print("\n" + "=" * 70)
print("FULL RESULTS")
print("=" * 70)
print(json.dumps(results, indent=2, default=str))

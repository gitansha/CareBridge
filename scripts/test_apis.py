import requests
import json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

VERIFY = False  # Local testing only - likely a corporate proxy intercepting SSL

# Test 1: RxNorm interaction endpoint (single drug: Warfarin)
print("=== RxNorm: Warfarin interactions ===")
url = "https://rxnav.nlm.nih.gov/REST/interaction/interaction.json?rxcui=11289"
r = requests.get(url, timeout=10, verify=VERIFY)
print(f"HTTP {r.status_code}")
if r.status_code == 200:
    data = r.json()
    groups = data.get("interactionTypeGroup", [])
    print(f"Interaction groups: {len(groups)}")
    for g in groups[:1]:
        print(f"Source: {g['sourceName']}")
        for itype in g.get("interactionType", [])[:1]:
            for pair in itype.get("interactionPair", [])[:2]:
                drugs = [c["name"] for c in pair.get("minConcept", [])]
                print(f"  {' + '.join(drugs)}: {pair['description'][:150]}")
else:
    print(r.text[:200])

print()

# Test 2: RxNorm drug name -> RxCUI lookup
print("=== RxNorm: Name normalization (aspirin) ===")
url = "https://rxnav.nlm.nih.gov/REST/rxcui.json?name=aspirin"
r = requests.get(url, timeout=10, verify=VERIFY)
print(f"HTTP {r.status_code}")
data = r.json()
print(f"RxCUI for 'aspirin': {data['idGroup'].get('rxnormId', ['NOT FOUND'])}")

print()

# Test 3: OpenFDA drug label
print("=== OpenFDA: Warfarin label ===")
url = "https://api.fda.gov/drug/label.json?search=openfda.generic_name:warfarin&limit=1"
r = requests.get(url, timeout=10, verify=VERIFY)
print(f"HTTP {r.status_code}")
data = r.json()
result = data["results"][0]
openfda = result.get("openfda", {})
print(f"Brand: {openfda.get('brand_name', ['N/A'])[0]}")
print(f"Drug class: {openfda.get('pharm_class_epc', ['N/A'])[0]}")
di = result.get("drug_interactions", ["N/A"])[0]
print(f"Drug Interactions (first 400 chars):\n{di[:400]}")
ci = result.get("contraindications", ["N/A"])[0]
print(f"\nContraindications (first 300 chars):\n{ci[:300]}")

print()

# Test 4: ICD WHO API
print("=== ICD WHO API ===")
url = "https://icd.who.int/icdapi"
r = requests.get(url, timeout=10, verify=VERIFY)
print(f"HTTP {r.status_code}")
print(f"Content-Type: {r.headers.get('content-type', '')}")
print("Note: Requires free registration + OAuth2 token for actual data queries")

import requests
import json

def test_api():
    base_url = "http://localhost:4001"
    
    print("🧪 Probando MS-Text-Analysis-Service...")
    
    # Test 1: Health Check
    print("\n1. Health Check:")
    response = requests.get(f"{base_url}/health")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
    
    # Test 2: Sentiment Analysis
    print("\n2. Análisis de Sentimiento:")
    data = {
        "text": "El sistema funciona perfectamente, estoy muy contento con el servicio.",
        "ticket_id": "TEST-001",
        "language": "spanish"
    }
    response = requests.post(f"{base_url}/api/text/sentiment", json=data)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"   Sentimiento: {result['sentiment']} ({result['label']})")
        print(f"   Confianza: {result['confidence']}")
    else:
        print(f"   Error: {response.text}")
    
    # Test 3: Tokenización
    print("\n3. Tokenización:")
    data = {
        "text": "Este es un texto de prueba para tokenizar.",
        "language": "spanish"
    }
    response = requests.post(f"{base_url}/api/text/tokenize", json=data)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"   Tokens: {result['tokens'][:5]}...")  # Primeros 5 tokens
        print(f"   Total tokens: {result['token_count']}")
    
    # Test 4: Vectorización
    print("\n4. Vectorización:")
    data = {
        "text": "El sistema de gestión logística necesita mejoras urgentes",
        "ticket_id": "TEST-002",
        "language": "spanish"
    }
    response = requests.post(f"{base_url}/api/text/vectorize?method=tfidf&reduce_dims=true", json=data)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"   Método: {result['method']}")
        print(f"   Dimensiones: {result['dimensions']}")
        print(f"   Vector (primeros 5): {result['vector'][:5]}")
    else:
        print(f"   Error: {response.text}")
    
    print(f"\n✅ Pruebas completadas!")
    print(f"📚 Visita http://localhost:4001/docs para más pruebas interactivas")

if __name__ == "__main__":
    test_api()

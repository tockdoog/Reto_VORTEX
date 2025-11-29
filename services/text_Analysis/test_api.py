import requests
import json

<<<<<<< HEAD
def test_classification_service():
    base_url = "http://localhost:4002"
    
    print("🧪 Probando MS-Classification-Service...")
    
    # Test 1: Health Check
    print("\n1. Health Check:")
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 2: Clasificación con texto
    print("\n2. Clasificación con texto:")
    try:
        data = {
            "text": "Error crítico en el módulo de facturación, el sistema se cierra inesperadamente",
            "ticket_id": "TS-2025-01142"
        }
        response = requests.post(f"{base_url}/api/classification/predict", json=data, timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"   Predicción: {result['prediction']}")
            print(f"   Confianza: {result['confidence']}")
            print(f"   Ticket ID: {result['ticket_id']}")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 3: Clasificación con vector
    print("\n3. Clasificación con vector:")
    try:
        # Vector de ejemplo (1000 dimensiones)
        example_vector = [0.1] * 1000
        data = {
            "vector": example_vector,
            "ticket_id": "TS-2025-01143"
        }
        response = requests.post(f"{base_url}/api/classification/predict", json=data, timeout=5)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"   Predicción: {result['prediction']}")
            print(f"   Confianza: {result['confidence']}")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 4: Información del modelo
    print("\n4. Información del modelo:")
    try:
        response = requests.get(f"{base_url}/api/classification/model-info", timeout=5)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"   Versión: {result['model_version']}")
            print(f"   Arquitectura: {result['model_architecture']}")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 5: Entrenamiento (solo si es necesario, puede tomar tiempo)
    print("\n5. Entrenamiento del modelo (2 épocas rápidas):")
    try:
        data = {
            "epochs": 2,
            "validation_split": 0.2
        }
        response = requests.post(f"{base_url}/api/classification/train", json=data, timeout=30)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"   Estado: {result['status']}")
            print(f"   Precisión: {result['accuracy']}")
            print(f"   Pérdida: {result['loss']}")
            print(f"   Tiempo: {result['training_time']}s")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"   Error: {e}")
    
    print(f"\n✅ Pruebas completadas!")
    print(f"📚 Visita http://localhost:4002/docs para más pruebas interactivas")

if __name__ == "__main__":
    test_classification_service()
=======
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
>>>>>>> Text-Analysis

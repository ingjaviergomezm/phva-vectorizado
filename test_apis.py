import os
from dotenv import load_dotenv
from litellm import completion

load_dotenv()

def test_api(name, model_string):
    print(f"\n--- Probando {name} ({model_string}) ---")
    try:
        response = completion(
            model=model_string, 
            messages=[{"role": "user", "content": "Responde únicamente con la palabra 'Éxito'."}]
        )
        print(f"[{name}] OK -> Respuesta: {response.choices[0].message.content}")
    except Exception as e:
        print(f"[{name}] ERROR -> {str(e)}")

def main():
    print("Iniciando validación de APIs cloud disponibles...")
    
    # 1. OpenAI
    test_api("OpenAI", "gpt-4o-mini")
    
    # 2. Gemini (Ajustando formato para API de Google AI Studio en v1beta)
    test_api("Gemini", "gemini/gemini-flash-latest")
    
    # 3. Perplexity (Usando alias oficiales de su API: sonar-pro o sonar)
    test_api("Perplexity", "perplexity/sonar-pro")

if __name__ == "__main__":
    main()

import os
from praisonaiagents import Knowledge
from telemetry import logger

class AntigravityRAG:
    """
    Gestor de RAG Local para el ecosistema Antigravity.
    Utiliza ChromaDB como Vector Store y Sentence-Transformers para embeddings locales.
    """
    
    def __init__(self, collection_name="antigravity_memory"):
        self.base_path = r"C:\Users\Usuario\.gemini\antigravity\scratch\ingjaviergomezm"
        self.db_path = os.path.join(self.base_path, "vector_store")
        self.collection_name = collection_name
        self.knowledge = None
        
    def initialize_knowledge(self, source_directory=None):
        """
        Inicializa o carga la base de conocimientos.
        """
        if source_directory is None:
            source_directory = self.base_path
            
        try:
            logger.info(f"💾 Inicializando RAG local en: {self.db_path}")
            
            # Configuración de Knowledge para PraisonAI v1.5+
            config = {
                "vector_store": {
                    "provider": "chroma",
                    "config": {
                        "collection_name": self.collection_name,
                        "path": self.db_path
                    }
                },
                "embedder": {
                    "provider": "sentence-transformers",
                    "config": {
                        "model_name": "all-MiniLM-L6-v2"
                    }
                }
            }
            
            # Nota: En algunas versiones de PraisonAI, las fuentes se pasan en el config o 
            # se agregan después. Intentamos pasarlo en el config bajo la llave 'sources'.
            config["sources"] = [source_directory]
            
            self.knowledge = Knowledge(config=config)
            logger.info("✅ Sistema RAG inicializado correctamente.")
            return True
        except Exception as e:
            logger.error(f"❌ Error al inicializar RAG: {str(e)}")
            return False

    def query(self, text, limit=3):
        """
        Realiza una búsqueda semántica en la base de conocimientos.
        """
        if not self.knowledge:
            logger.warning("Intentando consultar RAG sin inicializar.")
            return ""
            
        try:
            # PraisonAI Knowledge.search retorna los fragmentos más relevantes
            results = self.knowledge.search(text, limit=limit)
            return results
        except Exception as e:
            logger.error(f"❌ Error en consulta RAG: {str(e)}")
            return ""

if __name__ == "__main__":
    # Test rápido de indexación
    print("Iniciando indexación de memoria local...")
    rag = AntigravityRAG()
    success = rag.initialize_knowledge()
    if success:
        print("Indexación completada. Probando búsqueda...")
        # Probamos buscar un patrón definido en ROUTER_PHVA.md
        resultado = rag.query("¿Qué hacer si el prompt es muy largo para lógica?")
        print(f"\nResultado de búsqueda:\n{resultado}")
    else:
        print("Falló la inicialización del RAG.")

import uvicorn
import os
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 4001))
    print(f"🚀 Iniciando MS-Text-Analysis-Service en puerto {port}")
    print(f"📚 Documentación disponible en: http://localhost:{port}/docs")
    print(f"🔍 API Explorer disponible en: http://localhost:{port}/redoc")
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=port,
        reload=True,
        log_level="info"
    )

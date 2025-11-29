import uvicorn
import os
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
<<<<<<< HEAD
    port = int(os.getenv("PORT", 4002))
    print(f"🚀 Iniciando MS-Classification-Service en puerto {port}")
=======
    port = int(os.getenv("PORT", 4001))
    print(f"🚀 Iniciando MS-Text-Analysis-Service en puerto {port}")
>>>>>>> Text-Analysis
    print(f"📚 Documentación disponible en: http://localhost:{port}/docs")
    print(f"🔍 API Explorer disponible en: http://localhost:{port}/redoc")
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=port,
        reload=True,
        log_level="info"
    )
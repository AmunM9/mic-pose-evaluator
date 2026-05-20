import sys
import os

# Exponer el backend al path para que los imports de app.* funcionen
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

from mangum import Mangum  # noqa: E402
from app.main import app  # noqa: E402

# Mangum adapta FastAPI (ASGI) al handler Lambda/Vercel
# lifespan="off" porque Vercel no mantiene el ciclo de vida entre invocaciones
handler = Mangum(app, lifespan="off")

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware           # ← zaten import etmişsiniz
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address
from starlette.responses import RedirectResponse

from app.api.api import api_router
from app.settings import settings

# -------------------------------------------------
# 1) Uygulama nesnesi
app = FastAPI(title="Transfermarkt API")

# 2) CORS middleware – rate-limit’ten ÖNCE ekleyin
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,          # geliştirmede “*” da verebilirsiniz
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3) Rate-limit (SlowAPI) middleware
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[settings.RATE_LIMITING_FREQUENCY],
    enabled=settings.RATE_LIMITING_ENABLE,
)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

# 4) Router’lar
app.include_router(api_router)

# -------------------------------------------------
@app.get("/", include_in_schema=False)
def docs_redirect():
    return RedirectResponse(url="/docs")

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)


#çalıştırma: 

#cd ~/transfermarkt-api          # proje kökünde olun
#eval "$(poetry env activate)"    # venv hâlâ aktif değilse

#uvicorn app.main:app --reload d

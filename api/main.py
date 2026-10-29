from fastapi import FastAPI
from routes.basics import router as basics_router
from routes.users import router as users_router
from routes.franquias import router as franquias_router
from routes.franquiados import router as franquiados_router
from routes.frotas import router as frotas_router
from routes.custos_anuais import router as custos_anuais_router
from routes.multas import router as multas
from routes.notas import router as notas
from routes.oficina import router as oficina
from routes.planos import router as planos
from routes.calcoes import router as calcoes
from routes.codigos import router as codigos
from routes.cobrancas import router as cobrancas
from routes.despesas_fixas import router as despesas_fixas
from routes.faturamentos import router as faturamentos
from routes.semanais import router as semanais
from routes.despesas import router as despesas
from routes.locatarios import router as locatarios
from routes.filtros import router as filtros
from routes.anexos import router as anexos
from routes.relatorios import router as relatorios

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(basics_router, prefix="/api")
app.include_router(users_router, prefix="/api/user")
app.include_router(franquias_router, prefix="/api/franquia")
app.include_router(franquiados_router, prefix="/api/franquiado")
app.include_router(frotas_router, prefix="/api/frota")
app.include_router(custos_anuais_router, prefix="/api/custo")
app.include_router(multas, prefix="/api/multas")
app.include_router(notas, prefix="/api/notas")
app.include_router(oficina, prefix="/api/oficina")
app.include_router(planos, prefix="/api/planos")
app.include_router(calcoes, prefix="/api/calcoes")
app.include_router(codigos, prefix="/api/codigos")
app.include_router(cobrancas, prefix="/api/cobrancas")
app.include_router(despesas_fixas, prefix="/api/despesasFixas")
app.include_router(faturamentos, prefix="/api/faturamentos")
app.include_router(semanais, prefix="/api/semanais")
app.include_router(despesas, prefix="/api/despesas")
app.include_router(locatarios, prefix="/api/locatarios")
app.include_router(filtros, prefix="/api/filtros")
app.include_router(anexos, prefix="/api/anexos")
app.include_router(relatorios, prefix="/api/relatorios")
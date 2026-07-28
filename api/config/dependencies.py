from fastapi import Request, HTTPException
from config.funcoes import ler_token

def usuario_logado(request: Request):
    auth = request.headers.get("Authorization")

    if not auth:
        raise HTTPException(
            status_code=401,
            detail="Token não enviado"
        )

    token = auth.replace("Bearer ", "")

    dados = ler_token(token)

    if not dados["valido"]:
        raise HTTPException(
            status_code=401,
            detail=dados["erro"]
        )

    return dados
from fastapi import Request, HTTPException, Depends
from sqlalchemy.orm import Session

from config.funcoes import ler_token
from config.database import get_db
from models.Franquia import Franquia
from models.User import User


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


def usuario_logado_opcional(
    request: Request,
    db: Session = Depends(get_db)
):
    master = request.query_params.get("master")

    # master não informado ou valor diferente de 1 e 2
    if master is None:
        return usuario_logado(request)

    # master=1 -> verifica Franquia
    if master == "1":
        existe = db.query(Franquia).first()

    # master=2 -> verifica User
    elif master == "2":
        existe = db.query(User).first()

    # master informado, mas inválido
    else:
        raise HTTPException(
            status_code=400,
            detail="Parâmetro master inválido"
        )

    # Primeiro cadastro: não exige token
    if not existe:
        return None

    # Já existe cadastro: exige token
    return usuario_logado(request)
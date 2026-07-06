from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models.User import User
from models.Franquia import Franquia
from models.Franqueado import Franqueado
from models.Locatario import Locatario
from models.Frota import Frota
from models.FranquiaFraqueadoLocatario import FranquiaFraqueadoLocatario
from config.funcoes import remove_campos, apenasNumeros, verify_password, create_access_token, ler_token
from sqlalchemy import func
import os
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta

from repositories.FrotasRepository import FrotasRepository
from repositories.CalcoesRepository import CalcoesRepository


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UsersRepository:
    def __init__(self, db: Session):
        # Guarda a conexão com o banco para usar nos métodos da classe.
        self.db = db

    def helloa(self):
        return {"message": "API funcionando 🚀 sim"}

    def hello(self):
        return {"message": "API funcionando 🚀 "}

    def db_info(self):
        return {"database_url": os.getenv("DATABASE_URL")}

    def create_user(self, data, dados_token):
        try:
            njson = {}
            data['log_id'] = dados_token['dados']['id']
            password = data["password"]
            hashed_password = pwd_context.hash(password)
            user_data = {
                "nome": data["nome"],
                "email": data["email"],
                "password": hashed_password,
                "tipoAcessoID": data["tipoAcessoID"],
                "status": data["status"],
                "log_id": data['log_id']
            }
            user = User(**user_data)
            
            self.db.add(user)
            self.db.flush()
            # flush gera o ID sem dar commit ainda

            # 🔹 Criar entidade vinculada conforme tipo
            franquia = self.db.query(Franquia).filter(
                Franquia.id == data["franquia_id"]
            ).first()

            if not franquia:
                raise ValueError("Franquia não encontrada")

            if user.tipoAcessoID == 1:
                json = {
                    'user_id':user.id,
                    'franquia_id': franquia.id,
                    'franquiado_id':None,
                    'locatarios_id':None,
                    "log_id": data['log_id']
                }

                relacionamentos = self.relacionamentos(json)
            elif user.tipoAcessoID == 2:
                json_franqueados = {
                    "nome": data["nome"],
                    "status_id": data["status"],
                    'user_id':user.id,
                    'franquia_id': franquia.id,
                    'franqueado_id': data["franqueado_id"],
                    "log_id": data['log_id']
                }

                njson = self.franqueados(json_franqueados)

            elif user.tipoAcessoID == 3:
                data["user_id"] = user.id
                njson = self.locatarios(data)

            else:
                raise ValueError("tipoAcessoID inválido")

            # 🔹 Commit final (salva tudo)
            self.db.commit()
            self.db.refresh(user)
            return {
                "id": user.id,
                "nome": user.nome,
                "email": user.email,
                "tipoAcessoID": user.tipoAcessoID,
                "status": user.status,
                "franqueador":njson
            }

        except IntegrityError:
            self.db.rollback()
            raise ValueError("Email já cadastrado")

        except Exception as e:
            self.db.rollback()
            raise e

    def relacionamentos(self, json):
        relacionamento = FranquiaFraqueadoLocatario(**json)
        self.db.add(relacionamento)
        self.db.commit()
        self.db.refresh(relacionamento)

        return relacionamento

    def franqueados(self, json):
        
        user_id = json["user_id"]
        franquia_id = json["franquia_id"]

        
        try:
            # 🔎 verifica se já existe (ajuste campo conforme seu model)
            franqueado = self.db.query(Franqueado).filter(
                Franqueado.id == json["franqueado_id"]  # ou outro campo único
            ).first()

            if not franqueado:
                raise ValueError("Franqueado não existe favor cadastrar!")

            # 🔗 cria relacionamento independente
            relacionamento_data = {
                "user_id": user_id,
                "franquia_id": franquia_id,
                "franquiado_id": franqueado.id,
                "locatarios_id": None,
                "log_id": json['log_id']
            }

            self.relacionamentos(relacionamento_data)

            self.db.commit()
            self.db.refresh(franqueado)

            return franqueado.__dict__

        except Exception as e:
            self.db.rollback()
            raise e

    def locatarios(self, json):
        user_id = json["user_id"]
        franquia_id = json["franquia_id"]
        status = json["status"]
        franqueado_id = json["franqueado_id"]
        log_id = json['log_id']

        campos_para_remover = ["user_id","franquia_id","status","franqueado_id","email","password","tipoAcessoID"]
        novojson = remove_campos(json, campos_para_remover)
        novojson["status_id"] = status
        novojson["log_id"] = log_id
        try:
            locatario = Locatario(**novojson)
            self.db.add(locatario)
            self.db.flush()

            relacionamento_data = {
                "user_id": user_id,
                "franquia_id": franquia_id,
                "franquiado_id": franqueado_id,
                "locatarios_id": locatario.id,
                "log_id": log_id
            }

            self.relacionamentos(relacionamento_data)

            self.db.commit()
            self.db.refresh(locatario)

            frotas_repository = FrotasRepository(self.db)
            frotas_repository.fechar_liberar_veiculo(locatario.frota_id, 2, log_id)

            franqueado = self.db.query(Franqueado).filter(
                Franqueado.id == franqueado_id  # ou outro campo único
            ).first()

            json_retorno = franqueado.__dict__
            json_retorno["locatario"] = locatario.__dict__

            return json_retorno

        except IntegrityError:
            self.db.rollback()
            raise ValueError("Registro ja cadastrado ou faltando dados")

        except Exception as e:
            self.db.rollback()
            raise e

    def sfdelete_users(self, user_id, ativa, dados_token):
        try:
            log_id = dados_token['dados']['id']
            user = self.db.query(User).filter(User.id==user_id).first()
            tipo_acesso = user.tipoAcessoID

            if ativa is None:
                raise ValueError("paramentro ativa não foi passado")

            if ativa == 2:
                user.deleted_at = func.now()
            elif ativa == 1:
                user.deleted_at = None
            else:
                raise ValueError("parametro incorreto")

            user.status = ativa
            user.log_id = log_id
  
            if user.tipoAcessoID == 3:
                locatario = (
                    self.db.query(Locatario)
                    .join(
                        FranquiaFraqueadoLocatario,
                        FranquiaFraqueadoLocatario.locatarios_id == Locatario.id
                    )
                    .filter(
                        FranquiaFraqueadoLocatario.user_id == user.id,
                        Locatario.deleted_at == None
                    )
                    .first()
                )
                if not locatario:
                    raise ValueError("locatario nao existe ou ja deletado")

                if ativa == 2:
                    locatario.deleted_at = func.now()
                    frotas_repository = FrotasRepository(self.db)
                    frotas_repository.fechar_liberar_veiculo(locatario.frota_id, 1, log_id)

                    calcoes_repository = CalcoesRepository(self.db)
                    calcoes_repository.baixar_calcao(locatario.frota_id, dados_token)

                elif ativa == 1:
                    locatario.deleted_at = None
                locatario.status_id=ativa
                locatario.log_id = log_id

                self.db.commit()
                self.db.refresh(locatario)

            self.db.commit()  
            self.db.refresh(user)

            return user

        except Exception as e:
            self.db.rollback()
            raise e

    def login(self, data):
        try:
            user = (
                self.db.query(User, FranquiaFraqueadoLocatario)
                .join(
                    FranquiaFraqueadoLocatario,
                    User.id == FranquiaFraqueadoLocatario.user_id
                )
                .filter(
                    User.email == data["email"],
                    User.status == 1
                )
                .first()
            )

            if not user:
                raise Exception("Usuário não encontrado ou inativo")

            user_obj, franquia_obj = user

            if not verify_password(data["password"], user_obj.password):
                raise Exception("Senha inválida")

            # Dados que vão no token
            token_data = {
                "id": user_obj.id,
                "nome": user_obj.nome,
                "email": user_obj.email,
                "tipoAcessoID": user_obj.tipoAcessoID,
                "franquia_id": franquia_obj.franquia_id,
                "franquia_franquiador_locatario_id": franquia_obj.id,
                "franquia_id": franquia_obj.franquia_id,
                "franquiado_id": franquia_obj.franquiado_id,
                "locatarios_id": franquia_obj.locatarios_id                
            }

            access_token = create_access_token(token_data)

            return {
                "access_token": access_token,
                "token_type": "bearer",
                "user": token_data,
            }

        except Exception as e:
            self.db.rollback()
            raise e

    def update_users(self, user_id, data, dados_token, request):

        try:
            log_id = dados_token['dados']['id']
            user = self.db.query(User).filter(
                User.id == user_id, 
                User.email == data['email']
            ).first()

            if not user:
                raise ValueError("usuario não encontrada")

            password = data.get("password")
            campos_para_remover = ["email", "tipoAcessoID"]
            dados_user = remove_campos(data, campos_para_remover)

            if password:
                hashed_password = pwd_context.hash(password)
                user.password = hashed_password
                dados_user['password'] = hashed_password
            dados_user['log_id'] = log_id
            for campo, valor in dados_user.items():
                setattr(user, campo, valor)

            tipo = request.query_params.get("tipo")
            self.update_franquia(user_id, data, tipo, log_id)
            self.update_franquiados(user_id, data, tipo, log_id)
            self.update_locatarios(user_id, data, tipo, log_id)


            self.db.commit()
            self.db.refresh(user)
            return user

        except Exception as e:
            self.db.rollback()
            raise e

    def update_locatarios(self, user_id, data, tipo, log_id):
        tipo = int(tipo)
        status = data['status']
        if tipo == 3:
            locatario = (
                self.db.query(Locatario)
                .join(
                    FranquiaFraqueadoLocatario,
                    FranquiaFraqueadoLocatario.locatarios_id == Locatario.id
                )
                .filter(
                    FranquiaFraqueadoLocatario.user_id == user_id
                )
                .first()
            )
            rem_dados_locatario = ["email","password"]

            dados_locatario = remove_campos(data, rem_dados_locatario)
            dados_locatario['status_id'] = status
            dados_locatario['log_id'] = log_id
            # Atualiza os campos
            for campo, valor in dados_locatario.items():
                setattr(locatario, campo, valor)

            self.db.commit()
            self.db.refresh(locatario)

            # baixar frota

            frota = self.db.query(Frota).filter(
                Frota.id==locatario.frota_id
            ).first()

            if frota.id > 0:
                frota.status_id	= 2

            if int(data['status']) == 0:
                frota.status_id	= 1           

    def update_franquiados(self, user_id, data, tipo, log_id):
        tipo = int(tipo)
        status = data['status']
        if tipo == 2:
            franquiado = (
                self.db.query(Franqueado)
                .join(
                    FranquiaFraqueadoLocatario,
                    FranquiaFraqueadoLocatario.franquiado_id == Franqueado.id
                )
                .filter(
                    FranquiaFraqueadoLocatario.user_id == user_id
                )
                .first()
            )
            rem_dados_franquiado = ["email"]

            dados_franquiado = remove_campos(data, rem_dados_franquiado)
            dados_franquiado['status_id'] = status
            dados_franquiado['log_id'] = log_id
            # Atualiza os campos
            for campo, valor in dados_franquiado.items():
                setattr(franquiado, campo, valor)

            self.db.commit()
            self.db.refresh(franquiado)

    def update_franquia(self, user_id, data, tipo, log_id):
        tipo = int(tipo)
        status = data['status']
        if tipo == 1:
            franquia = (
                self.db.query(Franquia)
                .join(
                    FranquiaFraqueadoLocatario,
                    FranquiaFraqueadoLocatario.franquia_id == Franquia.id
                )
                .filter(
                    FranquiaFraqueadoLocatario.user_id == user_id
                )
                .first()
            )
            rem_dados_franquia = ["email"]

            dados_franquia = remove_campos(data, rem_dados_franquia)
            dados_franquia['status_id'] = status
            dados_franquia['log_id'] = log_id
            # Atualiza os campos
            for campo, valor in dados_franquia.items():
                setattr(franquia, campo, valor)

            self.db.commit()
            self.db.refresh(franquia)
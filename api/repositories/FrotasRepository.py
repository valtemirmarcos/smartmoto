from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func, or_, and_
from models.Franqueado import Franqueado
from models.Frota import Frota
from models.FranquiaFraqueadoLocatario import FranquiaFraqueadoLocatario
from models.Locatario import Locatario
from models.Codigo import Codigo
from models.User import User

from config.funcoes import remove_campos, apenasNumeros, valida_placa, validar_campos_obrigatorios, formatar_placa
from config.filtros import filtros_basicos_frota
import os
import re



class FrotasRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_frotas(self, data, dados_token):
        campos_obrigatorios = [
            "placa",
            "renavam",
            "ano",
            "modelo",
            "cor",
            "fraqueado_id",
            "status_id"
        ]
        saida = validar_campos_obrigatorios(campos_obrigatorios, data)
        placa = valida_placa(data["placa"])
        renavam = apenasNumeros(data["renavam"])
        campos_para_remover = ["placa", "renavam"]
        dados_frota = remove_campos(data, campos_para_remover)
        dados_frota['placa'] = placa
        dados_frota['renavam'] = renavam
        dados_frota['log_id'] = dados_token['dados']['id']
        
        try:
            buscaFrota = self.db.query(Frota).filter(
                or_(
                    Frota.placa == placa,
                    Frota.renavam == renavam
                )
            ).first()

            if buscaFrota:
                raise ValueError("Placa ou renavam já cadastrado")

            frota = Frota(**dados_frota)
            self.db.add(frota)
            self.db.commit()
            self.db.refresh(frota)
            return dados_frota
        
        except IntegrityError:
            self.db.rollback()
            raise ValueError("placa ou renavam já cadastrado")

        except Exception as e:
            self.db.rollback()
            raise e

    def update_frotas(self, frota_id, data, dados_token):
        try:
            frota = self.db.query(Frota).filter(
                Frota.id == frota_id
            ).first()
            if not frota:
                raise ValueError("Item da frota não encontrado")
            
            placa = valida_placa(data["placa"])
            campos_para_remover = ["id"]
            data['placa'] = placa
            dados_frota = remove_campos(data, campos_para_remover)
            dados_frota['log_id'] = dados_token['dados']['id']

            for campo, valor in dados_frota.items():
                if hasattr(frota, campo):
                    setattr(frota, campo, valor)
            
            self.db.commit()
            self.db.refresh(frota)
            return dados_frota.items()

        except Exception as e:
            self.db.rollback()
            raise e

    def delete_frotas(self, frota_id):
        try:
            frota = self.db.query(Frota).filter(
                Frota.id == frota_id
            ).first()

            if not frota:
                raise ValueError("Frota não encontrada")

            self.db.delete(frota)
            self.db.commit()

            return {"message": "Franqueado removida com sucesso"}

        except Exception as e:
            self.db.rollback()
            raise e

    def sfdelete_frotas(self, frota_id, ativa, dados_token):
        try:
            log_id = dados_token['dados']['id']
            frota = self.db.query(Frota).filter(
                Frota.id == frota_id
            ).first()

            if not frota:
                raise ValueError("Frota não encontrada")

            if ativa == 2:
                frota.deleted_at = func.now()

            elif ativa == 1:
                frota.deleted_at = None

            frota.status_id = ativa
            frota.log_id = log_id

            self.db.commit()
            self.db.refresh(frota)

            return {
                "id": frota.id,
                "status_id": frota.status_id,
                "deleted_at": frota.deleted_at
            }

        except Exception as e:
            self.db.rollback()
            raise e

    def fechar_liberar_veiculo(self, frota_id, ativo, log_id):
        try:
            frota = self.db.query(Frota).filter(
                Frota.id == frota_id
            ).first()

            if not frota:
                raise ValueError("Frota não encontrada")

            frota.status_id = ativo
            frota.log_id = log_id

            self.db.commit()
            self.db.refresh(frota)

            return {
                "id": frota.id,
                "status_id": frota.status_id
            }

        except Exception as e:
            self.db.rollback()
            raise e

    def listar_frotas(self, dados_token, filtro):
        try:
            dados = dados_token["dados"]
            tipo_acesso = dados.get("tipoAcessoID")

            query = (
                self.db.query(Frota, Codigo.descricao.label("status_descricao"), Franqueado.nome.label("nome_franquiado"),Locatario.nome.label("nome_locatario"), User)
                .join(
                    Franqueado,
                    Franqueado.id == Frota.fraqueado_id
                )
                .outerjoin(
                    Locatario,
                    and_(
                        Locatario.frota_id == Frota.id,
                        Locatario.status_id == 1
                    ) 
                    
                )
                .outerjoin(
                    Codigo, 
                    and_(
                        Codigo.depara_id == 2,
                        Codigo.codigo == Frota.status_id
                    )
                )
                .outerjoin(
                    User,
                    User.id == Frota.log_id
                )
                .filter(Frota.deleted_at.is_(None))
            )

            if tipo_acesso == 3:
                query = query.filter(Locatario.id == dados.get("locatarios_id"))
            elif tipo_acesso == 2:
                query = query.filter(Frota.fraqueado_id == dados.get("franquiado_id"))
            elif tipo_acesso == 1:
                pass

            query = filtros_basicos_frota(query, filtro)

            resultado = query.all()
            saida = []
            for frota, status_descricao, nome_franquiado, nome_locatario, user in resultado:
                item = {**frota.__dict__}
                item['placa_formatado'] = formatar_placa(frota.placa)
                item['status'] = status_descricao
                item['nome_franquiado'] = nome_franquiado
                item["usuario"] = user.nome if user else None
                item['nome_locatario'] = nome_locatario
                
                saida.append(item)
            return saida

        except Exception as e:
            print("ERRO:", str(e))  # <-- mostra o erro real
            self.db.rollback()
            raise e
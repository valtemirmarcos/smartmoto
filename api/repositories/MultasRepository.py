from sqlalchemy.orm import Session, aliased
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func, or_, and_

from models.Multa import Multa
from models.Frota import Frota
from models.FranquiaFraqueadoLocatario import FranquiaFraqueadoLocatario
from models.Locatario import Locatario
from models.Codigo import Codigo
from models.User import User

from config.funcoes import remove_campos, apenasNumeros, valida_placa, validar_campos_obrigatorios, formatar_placa

import os
import re

from config.filtros import filtro_basico_token, filtros_basicos_multas

class MultasRepository:
    def __init__(self, db: Session):
        self.db = db



    def create_multas(self, data, dados_token):

        campos_obrigatorios = [
            "franquia_franquiador_locatario_id",
            "frota_id",
            "codigo",
            "pontos",
            "data_infracao",
            "data_notificacao",
            "data_indicacao",
            "valor_multa",
            "status_id"
        ]
        saida = validar_campos_obrigatorios(campos_obrigatorios, data)
        codigo = str(data['codigo']).strip().upper()
        data['codigo'] = codigo

        buscaCodigo = self.db.query(Multa).filter(
            Multa.frota_id == data['frota_id'],
            Multa.codigo == codigo
        ).first()

        if buscaCodigo:
            raise ValueError("Código já cadastrado para essa frota")

        data['log_id'] = dados_token['dados']['id']
        dados_multas = data
        try:

            multa = Multa(**dados_multas)
            self.db.add(multa)
            self.db.commit()
            self.db.refresh(multa)
            return multa
        

        except Exception as e:
            self.db.rollback()
            raise e

    def update_multas(self, multa_id, data, dados_token):
        try:
            data['log_id'] = dados_token['dados']['id']
            multa = self.db.query(Multa).filter(
                Multa.id == multa_id
            ).first()
            if not multa:
                raise ValueError("multa não encontrada")

            campos_para_remover = ["franquia_franquiador_locatario_id", "frota_id", "codigo"]
            dados_multa = remove_campos(data, campos_para_remover)

            for campo, valor in dados_multa.items():
                if hasattr(multa, campo):
                    setattr(multa, campo, valor)
            
            self.db.commit()
            self.db.refresh(multa)
            return dados_multa.items()

        except Exception as e:
            self.db.rollback()
            raise e

    def delete_multas(self, multa_id):
        try:
            multa = self.db.query(Multa).filter(
                Multa.id == multa_id
            ).first()
            if not multa:
                raise ValueError("multa não encontrada")

            self.db.delete(multa)
            self.db.commit()

            return {"message": "Multa removida com sucesso"}

        except Exception as e:
            self.db.rollback()
            raise e

    def sfdelete_multas(self, multa_id, ativa, dados_token):
        try:
            log_id = dados_token['dados']['id']
            multa = self.db.query(Multa).filter(
                Multa.id == multa_id
            ).first()
            if not multa:
                raise ValueError("multa não encontrada")

            if ativa == 2:
                multa.deleted_at = func.now()

            elif ativa == 1:
                multa.deleted_at = None

            # multa.status_id = ativa
            multa.log_id = log_id

            self.db.commit()
            self.db.refresh(multa)

            return multa

        except Exception as e:
            self.db.rollback()
            raise e

    def listar_multas(self, dados_token, filtro):
        try:
            dados = dados_token['dados']
            parametros = ["franquia_id","franquiado_id","locatarios_id"]

            filtro_token = filtro_basico_token(FranquiaFraqueadoLocatario, dados, parametros)

            Status = aliased(Codigo, name="status")
            FormaPgto = aliased(Codigo, name="forma_pgto")
            query = (
                self.db.query(Multa, Frota, Status, FormaPgto, User, Locatario)
                .join(
                    Frota,
                    Frota.id == Multa.frota_id
                )

                .join(
                    FranquiaFraqueadoLocatario,
                    and_(
                        FranquiaFraqueadoLocatario.franquiado_id == Frota.fraqueado_id,
                        FranquiaFraqueadoLocatario.id == Multa.franquia_franquiador_locatario_id,
                    )
                )
                .join(
                    Locatario,
                    and_(
                        Locatario.id == FranquiaFraqueadoLocatario.locatarios_id,
                        Locatario.frota_id == Multa.frota_id,
                    )
                )
                .outerjoin(
                    Status, 
                    and_(
                        Status.depara_id == 6,
                        Status.codigo == Multa.status_id
                    )
                )
                .outerjoin(
                    FormaPgto, 
                    and_(
                        FormaPgto.depara_id == 5,
                        FormaPgto.codigo == Multa.pagamento_id
                    )
                )
                .outerjoin(
                    User,
                    User.id == Multa.log_id
                )
                .filter(
                    Multa.deleted_at.is_(None)
                )
            )
            query = filtros_basicos_multas(query, filtro)
            multas = query.filter(*filtro_token).all()
            saida = []
            for multa, frota, status, formaPgto, user, locatario in multas:
                item = {**multa.__dict__}
                item['placa'] = formatar_placa(frota.placa) if frota else None
                item['placasf'] = frota.placa if frota else None
                item['fraqueado_id'] = frota.fraqueado_id if frota else None
                item["pagamento"] = formaPgto.descricao if formaPgto else None
                item["status"] = status.descricao if status else None
                item["usuario"] = user.nome if user else None
                item["locatario_id"] = locatario.id if user else None
                item["locatario_nome"] = locatario.nome if user else None
                saida.append(item)

            # sql = str(query.statement.compile(compile_kwargs={"literal_binds": True}))
            # return {"sql": filtro}
            return saida
        except Exception as e:
            self.db.rollback()
            raise e
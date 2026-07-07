from sqlalchemy.orm import Session, aliased
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func, or_, and_, extract

from models.Semanal import Semanal
from models.Frota import Frota
from models.Locatario import Locatario
from models.Plano import Plano
from models.FranquiaFraqueadoLocatario import FranquiaFraqueadoLocatario
from models.Codigo import Codigo
from models.User import User
from models.Franqueado import Franqueado

from config.funcoes import remove_campos, apenasNumeros, valida_placa, validar_campos_obrigatorios, dia_semana_extenso, datas_do_dia_semana_mes, filtro_basico, formatar_placa
from config.filtros import filtros_basicos_semanais
import os
import re

from datetime import date, timedelta
import calendar
import base64
from fastapi.responses import Response

class SemanaisRepository:
    def __init__(self, db: Session):
        self.db = db



    def create_semanais(self, data, dados_token):

        campos_obrigatorios = [
            "franquia_franquiador_locatario_id",
            "frota_id",
            "data_prevista",
            "valor",
            "status_id"
        ]
        saida = validar_campos_obrigatorios(campos_obrigatorios, data)
        data['log_id'] = dados_token['dados']['id']
        dados_semanais = data
        try:

            semanal = Semanal(**dados_semanais)
            self.db.add(semanal)
            self.db.commit()
            self.db.refresh(semanal)
            return semanal
        

        except Exception as e:
            self.db.rollback()
            raise e

    def update_semanais(self, semana_id, data, dados_token):
        try:
            data['log_id'] = dados_token['dados']['id']
            semanal = self.db.query(Semanal).filter(
                Semanal.id == semana_id
            ).first()
            if not semanal:
                raise ValueError("semanal não encontrada")

            campos_para_remover = ["franquia_franquiador_locatario_id", "frota_id"]
            dados_multa = remove_campos(data, campos_para_remover)
            for campo, valor in dados_multa.items():
                setattr(semanal, campo, valor)
                
            self.db.commit()
            self.db.refresh(semanal)

            return semanal

        except Exception as e:
            self.db.rollback()
            raise e

    def delete_semanais(self, semana_id, dados_token):
        try:
            semanal = self.db.query(Semanal).filter(
                Semanal.id == semana_id
            ).first()
            if not semanal:
                raise ValueError("semanal não encontrada")

            self.db.delete(semanal)
            self.db.commit()

            return {"message": "Semanal removida com sucesso"}

        except Exception as e:
            self.db.rollback()
            raise e

    def sfdelete_semanais(self, semana_id, ativa, dados_token):
        try:

            log_id = dados_token['dados']['id']
            semanal = self.db.query(Semanal).filter(
                Semanal.id == semana_id
            ).first()
            if not semanal:
                raise ValueError("semanal não encontrada")

            if ativa == 0:
                semanal.deleted_at = func.now()

            elif ativa == 1:
                semanal.deleted_at = None

            semanal.status_id = ativa
            semanal.log_id = log_id

            self.db.commit()
            self.db.refresh(semanal)

            return semanal

        except Exception as e:
            self.db.rollback()
            raise e

    def gerar_semanais(self, data, dados_token):
        
        campos_obrigatorios = [
            "status_id"
        ]
        log_id = dados_token['dados']['id']
        saida = validar_campos_obrigatorios(campos_obrigatorios, data)
        franquiado_id = dados_token['dados']["franquiado_id"]

        query = (
            self.db.query(Frota, Locatario, Plano, FranquiaFraqueadoLocatario)
            .join(
                Locatario,
                Locatario.frota_id == Frota.id
            )
            .join(
                Plano,
                Plano.id == Locatario.plano_id
            )
            .join(
                FranquiaFraqueadoLocatario,
                FranquiaFraqueadoLocatario.locatarios_id == Locatario.id
            )
            .filter(
                Frota.status_id == 2,
                Locatario.status_id == 1
            )
        )

        # se NÃO for todos, adiciona filtro
        if franquiado_id is not None:
            query = query.filter(
                Frota.fraqueado_id == franquiado_id
            )

        resultados = query.all()

        semanais = []
        retorno_semanais = []

        for frota, locatario, plano, franquiaFraqueadoLocatario in resultados:

            numero_dia = locatario.data_inicio_contrato.weekday()

            datas = datas_do_dia_semana_mes(numero_dia,data['ano'],data['mes'])
            for data_item in datas:
                retorno_semanais.append({
                    "placa":frota.placa,
                    "data_prevista":data_item,
                    "valor": plano.valor,
                    "status":"Em aberto"
                })
                existe = self.db.query(Semanal).filter(
                    Semanal.data_prevista == data_item,
                    Semanal.franquia_franquiador_locatario_id == franquiaFraqueadoLocatario.id,
                    Semanal.frota_id == frota.id
                ).first()
                if not existe:
                    semanais.append({
                        "franquia_franquiador_locatario_id":franquiaFraqueadoLocatario.id,
                        "frota_id":frota.id,
                        "data_prevista":data_item,
                        "valor": plano.valor,
                        "status_id":1,
                        "log_id":log_id
                    })
                

        semanais.sort(key=lambda x: x["data_prevista"])
        retorno_semanais.sort(key=lambda x: x["data_prevista"])

        try:

            self.db.bulk_insert_mappings(Semanal, semanais)
            self.db.commit()
            return retorno_semanais
        

        except Exception as e:
            self.db.rollback()
            raise e

    def listar_semanais(self, dados_token, filtro):
        try:
            dados = dados_token['dados']
            parametros = ["franquia_id","franquiado_id","locatarios_id"]

            filtro_token = filtro_basico(FranquiaFraqueadoLocatario, dados, parametros)

            Status = aliased(Codigo, name="status")
            query = (
                self.db.query(Semanal, Frota, Status, User, Franqueado, Locatario)
                .join(
                    Frota,
                    Frota.id == Semanal.frota_id
                )
                .join(
                    Locatario,
                    Locatario.frota_id == Semanal.frota_id
                )
                .join(
                    Franqueado,
                    Franqueado.id == Frota.fraqueado_id
                )
                .outerjoin(
                    FranquiaFraqueadoLocatario,
                    and_(
                        FranquiaFraqueadoLocatario.franquiado_id == Frota.fraqueado_id,
                        FranquiaFraqueadoLocatario.locatarios_id == Locatario.id,
                    )
                )
                .outerjoin(
                    Status, 
                    and_(
                        Status.depara_id == 3,
                        Status.codigo == Semanal.status_id
                    )
                )
                .outerjoin(
                    User,
                    User.id == Semanal.log_id
                )           
                .filter(
                    Frota.status_id == 2,
                    Locatario.status_id == 1
                )
            )

            hoje = date.today()

            # Se não vier filtro de data nem mês/ano → aplica mês atual
            if (
                not filtro.get("dataInicio")
                and not filtro.get("dataFim")
            ):
                filtro["mes"] = hoje.month
                filtro["ano"] = hoje.year

            query = filtros_basicos_semanais(query, filtro)
            query = query.filter(Semanal.deleted_at == None)

            if filtro.get("mes") and filtro.get("ano"):
                query = query.filter(
                    extract('month', Semanal.data_prevista) == filtro["mes"],
                    extract('year', Semanal.data_prevista) == filtro["ano"]
                )

            semanais = query.filter(*filtro_token).all()
            saida = []
            for semanal, frota, status, user, franqueado, locatario in semanais:
                data_prevista = semanal.data_prevista
                numero_dia = data_prevista.weekday()
                semana = dia_semana_extenso(numero_dia)
                if (
                    data_prevista
                    and data_prevista < date.today()
                    and semanal.status_id == 1
                ):
                    semanal.status_id = 3
                    self.db.commit()
                    self.db.refresh(semanal)

                item = {**semanal.__dict__}
                item['placa'] = frota.placa if frota else None
                item["status"] = status.descricao if status else None
                item["usuario"] = user.nome if user else None
                item['nome_franquiado'] = franqueado.nome if franqueado else None
                item['franquiado_id'] = franqueado.id if franqueado else None
                item['nome_locatario'] = locatario.nome if locatario else None
                item['dia_semana'] = semana
                saida.append(item)

            # sql = str(query.statement.compile(compile_kwargs={"literal_binds": True}))
            # return {"sql": filtro}

            return saida

        except Exception as e:
            self.db.rollback()
            raise e

    def salvar_imagem_semanal(self, semana_id, base64_str, tipo_arquivo, dados_token):
        try:
            log_id = dados_token['dados']['id']

            semanal = self.db.query(Semanal).filter(
                Semanal.id == semana_id
            ).first()

            if not semanal:
                raise ValueError("semanal não encontrada")

            semanal.imagem_base64 = base64_str
            semanal.imagem_tipo = tipo_arquivo
            semanal.log_id = log_id
            semanal.updated_at = func.now()

            self.db.commit()
            self.db.refresh(semanal)

            return semanal
        except Exception as error:
            self.db.rollback()
            raise error


    def buscar_por_id(self, semanal_id):
        return self.db.query(Semanal).filter(
            Semanal.id == semanal_id
        ).first()


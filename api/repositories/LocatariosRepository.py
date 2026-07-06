from sqlalchemy.orm import Session,aliased
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func, or_, and_

from models.Codigo import Codigo
from models.Locatario import Locatario
from models.Frota import Frota
from models.Plano import Plano
from models.FranquiaFraqueadoLocatario import FranquiaFraqueadoLocatario
from models.User import User

from config.funcoes import remove_campos, apenasNumeros, valida_placa, validar_campos_obrigatorios, filtro_basico,formatar_placa, dia_semana_extenso
from config.filtros import filtros_basicos_locatario
import os
import re
from datetime import datetime


class LocatariosRepository:
    def __init__(self, db: Session):
        self.db = db

    def listar_locatarios(self, dados_token, filtros_url):
        try:
            dados = dados_token['dados']
            parametros = ["franquia_id","franquiado_id","locatarios_id"]

            filtro = filtro_basico(FranquiaFraqueadoLocatario, dados, parametros)
            UsuarioLocador = aliased(User, name="usuarioLocador")
            query = (
                self.db.query(Locatario, Frota, Plano, Codigo, User, UsuarioLocador, FranquiaFraqueadoLocatario)
                .join(
                    Frota,
                    Frota.id == Locatario.frota_id
                )
                .outerjoin(
                    FranquiaFraqueadoLocatario,
                    and_(
                        FranquiaFraqueadoLocatario.franquiado_id == Frota.fraqueado_id,
                        FranquiaFraqueadoLocatario.locatarios_id == Locatario.id,
                    )
                )
                .join(
                    Plano,
                    Plano.id == Locatario.plano_id
                )
                .outerjoin(
                    Codigo, 
                    and_(
                        Codigo.depara_id == 1,
                        Codigo.codigo == Locatario.status_id
                    )
                )
                .outerjoin(
                    User,
                    User.id == Locatario.log_id
                )
                .outerjoin(
                    UsuarioLocador,
                    UsuarioLocador.id == FranquiaFraqueadoLocatario.user_id
                )
            )
            query = filtros_basicos_locatario(query, filtros_url)           
            locatarios = query.filter(*filtro).all()
            saida = []
            for locatario, frota, plano, codigo, user, usuarioLocador, franquiafraqueadolocatario in locatarios:
                diaSemana = dia_semana_extenso(locatario.data_inicio_contrato.weekday())

                item = {**locatario.__dict__}
                item['placa'] = formatar_placa(frota.placa) if frota else None
                item["plano"] = plano.plano if plano else None
                item["status"] = codigo.descricao if codigo else None
                item["usuario"] = user.nome if user else None
                item["email"] = usuarioLocador.email if usuarioLocador else None
                item["user_locatario_id"] = usuarioLocador.id if usuarioLocador else None
                item["dia_semana"] = diaSemana if locatario else None 
                item["fraqueado_id"] = frota.fraqueado_id if frota else None 
                item["franquia_franquiador_locatario_id"] = franquiafraqueadolocatario.id if franquiafraqueadolocatario else None 
                saida.append(item)

            return saida

        except Exception as e:
            self.db.rollback()
            raise e
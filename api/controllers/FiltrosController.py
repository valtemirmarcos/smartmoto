import os
from repositories.FiltrosRepository import FiltrosRepository
from config.funcoes import success_response, exception_response


class FiltrosController:
    def __init__(self, db):
        self.repository = FiltrosRepository(db)

    def frota_status(self):
        try:
            return success_response(self.repository.frota_status(), "Filtro Frota status listado com sucesso!")
        except ValueError as e:
            return exception_response(str(e), 404)
        except Exception as error:
            return exception_response(str(error), 500)

    def locatario_status(self):
        try:
            return success_response(self.repository.locatario_status(), "Filtro Locatario status listado com sucesso!")
        except ValueError as e:
            return exception_response(str(e), 404)
        except Exception as error:
            return exception_response(str(error), 500)

    def calcao_status(self):
        try:
            return success_response(self.repository.calcao_status(), "Filtro Calção status listado com sucesso!")
        except ValueError as e:
            return exception_response(str(e), 404)
        except Exception as error:
            return exception_response(str(error), 500)

    def filtro_planos(self):
        try:
            return success_response(self.repository.filtro_planos(), "Filtro planos listado com sucesso!")
        except ValueError as e:
            return exception_response(str(e), 404)
        except Exception as error:
            return exception_response(str(error), 500)

    def filtro_pagamentos(self):
        try:
            return success_response(self.repository.filtro_pagamentos(), "Filtro pagamentos listado com sucesso!")
        except ValueError as e:
            return exception_response(str(e), 404)
        except Exception as error:
            return exception_response(str(error), 500)

    def semanais_status(self):
        try:
            return success_response(self.repository.semanais_status(), "Filtro Semanais status listado com sucesso!")
        except ValueError as e:
            return exception_response(str(e), 404)
        except Exception as error:
            return exception_response(str(error), 500)

    def multas_status(self):
        try:
            return success_response(self.repository.multas_status(), "Filtro Multas status listado com sucesso!")
        except ValueError as e:
            return exception_response(str(e), 404)
        except Exception as error:
            return exception_response(str(error), 500)

    def faturamentos_status(self):
        try:
            return success_response(self.repository.faturamentos_status(), "Filtro Faturamentos status listado com sucesso!")
        except ValueError as e:
            return exception_response(str(e), 404)
        except Exception as error:
            return exception_response(str(error), 500)

    def faturamentos_tipos(self):
        try:
            return success_response(self.repository.faturamentos_tipos(), "Filtro Faturamentos tipos listado com sucesso!")
        except ValueError as e:
            return exception_response(str(e), 404)
        except Exception as error:
            return exception_response(str(error), 500)

    def custos_status(self):
        try:
            return success_response(self.repository.custos_status(), "Filtro custo status listado com sucesso!")
        except ValueError as e:
            return exception_response(str(e), 404)
        except Exception as error:
            return exception_response(str(error), 500)

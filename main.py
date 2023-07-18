import schedule
import time
from funcionalidades import Nevoeiro, Cidade, FarmExp, FarmRecursos


class Bot:
    def __init__(self):
        self.time_recursos = 1
    def realizar_acao_nevoeiro(self):
        nevoeiro = Nevoeiro(debug=True)
        success = nevoeiro.execute()
        if not success:
            nevoeiro.logger.info("Ação nevoeiro falhou")

    def realizar_acao_farmarexp(self):
        farm_exp = FarmExp(debug=True, lvl=2)
        success = farm_exp.execute()
        if not success:
            farm_exp.logger.info("Ação Farmar Exp falhou")

    def realizar_acao_cidade(self):
        cidade = Cidade(debug=True)
        success = cidade.execute()
        if not success:
            print("Ação cidade falhou")

    def realizar_acao_farmarrecursos(self):
        farm_exp = FarmRecursos(debug=True)
        success = farm_exp.execute()
        if isinstance(success, int):
            farm_exp.logger.info(f"Voltamos a ver daqui a {success} segundos.")
            schedule.clear('farmar_recursos')  # Cancelar a tarefa agendada anterior
            self.time_recursos = success
            schedule.every(success).seconds.do(self.realizar_acao_farmarrecursos).tag('farmar_recursos')  # Reagendar a função e adicionar a tag
        if not success:
            farm_exp.logger.info("Ação Farmar Exp falhou")

    def run(self):
        schedule.every(1).seconds.do(self.realizar_acao_farmarrecursos).tag('farmar_recursos')  # Agendar a função pela primeira vez e adicionar a tag
        schedule.every(10).minutes.do(self.realizar_acao_cidade)
        while True:
            schedule.run_pending()
            time.sleep(1)


if __name__ == "__main__":
    bot = Bot()
    bot.run()

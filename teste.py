from funcionalidades import Nevoeiro, Cidade, FarmExp, FarmRecursos
import schedule
import time


time_recursos = 1

def realizar_acao_nevoeiro():
    nevoeiro = Nevoeiro(debug=True)
    success = nevoeiro.execute()
    if not success:
        nevoeiro.logger.info("Ação nevoeiro falhou")

def realizar_acao_farmarexp():
    farm_exp = FarmExp(debug=True, lvl=2)
    success = farm_exp.execute()
    if not success:
        farm_exp.logger.info("Ação Farmar Exp falhou")

def realizar_acao_farmarrecursos():
    global time_recursos
    farm_exp = FarmRecursos(debug=True)
    success = farm_exp.execute()
    time_recursos = success
    if isinstance(success, int):
        farm_exp.logger.info(f"Voltamos a ver daqui a {success} segundos.")
    if not success:
        farm_exp.logger.info("Ação Farmar Exp falhou")

def realizar_acao_cidade():
    # Aqui você chamaria uma ação similar para a cidade, por exemplo:
    cidade = Cidade(debug=True)
    success = cidade.execute()
    if not success:
        print("Ação cidade falhou")
    pass

# schedule.every(10).seconds.do(realizar_acao_cidade)


while True:
    print(time_recursos)
    schedule.every(time_recursos).seconds.do(realizar_acao_farmarrecursos)
    schedule.run_pending()
    time.sleep(1)

import time
import os
import device
import random
import logging
import coloredlogs


class Acao:
    def __init__(self, debug=True):
        self.presets = {
            1: [702, 89],
            2: [745, 90]
        }
        self.debug = debug
        self.device = device.Device(self.debug)
        self.logger = logging.getLogger(__name__)
        coloredlogs.install(level='DEBUG', logger=self.logger, fmt='%(asctime)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S')

    def attempt_action(self, target, action, max_attempts=30, delay_min=0.75, delay_max=2.0, confidence=0.8):
        for attempt in range(max_attempts):
            time.sleep(random.uniform(delay_min, delay_max))
            result = action(target, confidence)
            if result:
                self.logger.info(f"Action '{action.__name__}' on target '{target}' successful")
                return True
            else:
                if self.debug:
                    self.logger.warning(
                        f"Action '{action.__name__}' on target '{target}' failed, attempt {attempt + 1}")
        return False

    def get_actions(self, directory):
        atual = os.getcwd()
        directory_completo = f"{atual}\\utils\\target\\{directory}"
        return [f"{directory}\\" + os.path.splitext(f)[0] for f in os.listdir(directory_completo) if
                os.path.isfile(os.path.join(directory_completo, f))]

    def home(self):
        home = ["home", "home1"]
        if self.attempt_action("mapa", self.device.clicar, max_attempts=3, delay_min=0, delay_max=0):
            self.logger.info("Já devemos estar na cidade")

        if not self.attempt_action(home, self.device.clicar, max_attempts=3, delay_min=0, delay_max=0, confidence=0.9):
            self.logger.info("Não encontrei o botão home")
            return False

        return True

    def hospital(self):
        if not self.home():
            self.logger.info("Não consegui voltar para a cidade")
            return False

        if not self.attempt_action("hospital", self.device.clicar, max_attempts=3, delay_max=1):
            self.logger.info("Estão todos bem")
            return False

        if not self.attempt_action("curar", self.device.clicar, max_attempts=3, delay_max=1):
            self.logger.info("Não encontrei o botão de curar")

        self.device.device.shell(f"input tap 16 24")
        return True

    def find_start_action(self, actions, home=True):
        found_actions = [action_tuple for action_tuple in actions if
                         self.device.localizar(action_tuple[0], confidence=0.8)]
        if not found_actions:
            if home:
                self.home()
                return actions[0]
            self.logger.info("Nenhuma ação foi encontrada")
            return None
        start_action = min(found_actions, key=lambda x: actions.index(x))
        return start_action

    def multiple_actions(self, actions, lvl=1, seguir_em_frente=[], home=True):
        start_action = self.find_start_action(actions, home)

        if start_action is None:
            start_action = actions[0]

        start_index = actions.index(start_action)

        for action_tuple in actions[start_index:]:
            target, action, *params = action_tuple

            for _ in range(lvl) if target == "menos" else range(1):
                if not self.attempt_action(target, action, *params):
                    if target in seguir_em_frente:
                        self.logger.info(f"Já estás no sitio certo")
                    else:
                        self.logger.info(f"Ação '{action.__name__}' no alvo '{target}' falhou")
                        return False

        return True

    def search(self, target):

        barra = ["barra", "barra_meio"]
        lupa = ["lupa", "lupa1"]
        seguir_em_frente = [target, barra]

        actions = [("mapa", self.device.clicar, 3, 0, 0),  # max_attempts=3, delay_max=1
                   (lupa, self.device.clicar, 30, 0, 0, 0.6),
                   # max_attempts=30, delay_min=0.75, delay_max=2, confidence=0.8
                   (target, self.device.clicar, 3, 0.25, 0.50),
                   (barra, self.device.arrastar, 3, 0.25, 0.50)]  # max_attempts=3, delay_max=1

        if not self.multiple_actions(actions, seguir_em_frente=seguir_em_frente):
            self.logger.info("Não foi possivel iniciar pesquisa")
            return False

        return True


class Nevoeiro(Acao):
    def __init__(self, debug=True):
        super().__init__(debug)
        self.actions = ["acampamento", "explorar", "explorar_btn",
                        "explorar_btn2", "marchar_batedor"]

    def execute(self):
        start_action = self.find_start_action(self.actions)
        if start_action is None:
            return False
        actions = self.actions
        start_index = actions.index(start_action)
        for action in actions[start_index:]:
            if not self.attempt_action(action, self.device.clicar):
                self.logger.info(f"Ação '{action}' falhou")
                return False
        return True


class Cidade(Acao):
    def __init__(self, debug=True):
        super().__init__(debug)
        self.actions = self.get_actions("cidade")
        print(f"{self.actions=}")

    def execute(self):
        if not self.home():
            self.logger.info("Não conseguimos ir para a cidade")
            return False

        acao = self.attempt_action(self.actions, self.device.clicar, max_attempts=5, delay_max=1)

        while acao:
            self.logger.info(f"Efetuamos a ação {acao}")
            acao = self.attempt_action(self.actions, self.device.clicar, max_attempts=5, delay_max=1)

        self.logger.info("Não há nada na cidade para fazer")
        return True


class FarmExp(Acao):
    def __init__(self, debug=True, lvl=1):
        self.lvl = lvl
        super().__init__(debug)
        monstros = ["monstro", "monstro2", "monstro3"]
        barra = ["barra", "barra_meio"]
        self.seguir_em_frente = ["lobscuros", barra, "mapa"]

        self.actions = [("mapa", self.device.clicar, 3, 0, 1),  # max_attempts=3, delay_max=1
                        ("lupa", self.device.clicar, 30, 0.75, 2, 0.6),
                        # max_attempts=30, delay_min=0.75, delay_max=2, confidence=0.8
                        ("lobscuros", self.device.clicar, 3, 0.75, 1),  # max_attempts=3, delay_max=1
                        (barra, self.device.arrastar, 3, 0.75, 1),  # max_attempts=3, delay_max=1
                        ("menos", self.device.clicar, 3, 0.75, 1),  # max_attempts=3, delay_max=1
                        ("buscar", self.device.clicar, 10),  # max_attempts=10
                        (monstros, self.device.clicar, 50, 0, 0, 0.65),
                        # max_attempts=50, delay_min=0, delay_max=0, confidence=0.6
                        ("ataque", self.device.clicar, 3),  # max_attempts=3
                        ("legiao_disponivel", self.device.clicar, 40, 1, 2),
                        # max_attempts=40, delay_min=4, delay_max=5
                        ("criar_legioes", self.device.clicar, 5, 0, 0),  # max_attempts=5, delay_min=0, delay_max=0
                        (self.presets, self.device.clicar, 10),  # max_attempts=10
                        ("marchar", self.device.clicar, 5),  # max_attempts=5
                        ("home", self.device.clicar, 3, 0.75, 1)]  # max_attempts=3, delay_max=1

    def execute(self):
        while self.hospital():
            self.logger.info("Estamos no hospital")

        if not self.multiple_actions(self.actions, self.lvl, self.seguir_em_frente):
            self.logger.info("Não conseguimos farmar exp")
            return False

        return True


class FarmRecursos(Acao):

    def __init__(self, debug=True):
        super().__init__()

        self.recursos = {"mouro": ["ouro1", "ouro2", "ouro3", "ouro4"],
                         "mmadeira": ["madeira1", "madeira2", "madeira3"],
                         "mminerio": ["minerio1", "minerio2", "minerio3"]}

        # Get the keys of the dictionary and convert it to a list.
        keys = list(self.recursos.keys())

        # Shuffle the list of keys.
        random.shuffle(keys)

        # Build a new dictionary with the shuffled keys.
        self.recursos = {key: self.recursos[key] for key in keys}

        self.seguir_em_frente = ["lobscuros"]
        self.coletar = ["coletar", "coletar1"]
        presets = self.presets

        self.actions = [
                        ("criar_legioes", self.device.clicar, 5, 0, 0),  # max_attempts=5, delay_min=0, delay_max=0
                        (presets, self.device.clicar, 5),  # max_attempts=10
                        ("marchar", self.device.clicar, 5)]  # max_attempts=5

    def procurar_recurso(self):

        while True:

            if not self.attempt_action("buscar", self.device.clicar, max_attempts=10, delay_min=0, delay_max=0):
                self.logger.info("Não conseguimos clicar em 'buscar'")
                return False

            if self.device.tirar_print(iguais=True):
                if not self.attempt_action("menos", self.device.clicar, max_attempts=3, confidence=0.9,
                                           delay_min=0, delay_max=0):
                    return False

            else:
                return True

    def execute(self):

        for recurso, imagens in self.recursos.items():
            self.search(recurso)
            self.procurar_recurso()

            self.attempt_action(imagens, self.device.clicar, 10, delay_min=0, delay_max=0, confidence=0.6)

            if not self.attempt_action(self.coletar, self.device.clicar, 10, delay_max=0.5, confidence=0.6):
                self.logger.info(f"Não conseguimos coletar {recurso} ")
                return False

            r, g, b = self.device.localizar_pixel([895, 84]) # verificar se há legioes disponiveis

            if 120 < r < 150 and 120 < g < 150 and 120 < b < 150:

                if not self.multiple_actions(self.actions, home=False):
                    self.logger.info("Não conseguimos farmar recursos")
                    return 1

            else:
                self.logger.info("Sem stamina para farmar recursos")
                self.device.device.shell(f"input tap 515 270")
                return 300

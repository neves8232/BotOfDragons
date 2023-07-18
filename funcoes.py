from pynput import mouse
import time
import os
import device
import random
import logging
import coloredlogs

DEBUG = True

device = device.Device(DEBUG)

directory = os.getcwd()
utils = f"{directory}\\utils"

# Create a logger object.
logger = logging.getLogger(__name__)

# Install a colored formatter into the logger.
coloredlogs.install(level='DEBUG', logger=logger, fmt='%(asctime)s %(levelname)s %(message)s', datefmt='%H:%M:%S')


def acoes_para_fazer(directory=f"{utils}\\target\\cidade"):
    return ["cidade\\" + os.path.splitext(f)[0] for f in os.listdir(directory) if
            os.path.isfile(os.path.join(directory, f))]


def attempt_action(target, action, max_attempts=30, delay_min=0.75, delay_max=2, confidence=0.8):
    for attempt in range(max_attempts):
        time.sleep(random.uniform(delay_min, delay_max))
        result = action(target, confidence)
        if result:
            logger.info(f"Action '{action.__name__}' on target '{target}' successful")
            return True
        else:
            if DEBUG:
                logger.warning(f"Action '{action.__name__}' on target '{target}' failed, attempt {attempt + 1}")
    return False


def procura_mobs(lvl=1):
    l_obscuros_x = 156  # legiao_obscuros.png
    l_obscuros_y = 484

    obscuros_x = 72  # obscuros.png
    obscuros_y = 230

    monstros = ["monstro", "monstro2", "monstro3"]

    if not attempt_action("mapa", device.clicar, max_attempts=3, delay_max=1):
        logger.info("Já devemos estar no mapa")

    if not attempt_action("lupa", device.clicar, confidence=0.6):
        logger.info("Não encontrei a lupa")

    if not attempt_action("lobscuros", device.clicar, max_attempts=3, delay_max=1):
        logger.info("Já estamos no sitio certo")


    if not attempt_action("barra", device.arrastar, max_attempts=3, delay_max=1):
        if not attempt_action("barra_meio", device.arrastar, max_attempts=3, delay_max=1):
            logger.info("Já está a nivel máximo")

    for _ in range(lvl):
        if not attempt_action("menos", device.clicar, max_attempts=3, delay_max=1):
            logger.info("Não deu para diminuir o nivel")

    if not attempt_action("buscar", device.clicar, max_attempts=10):
        logger.info("Não encontrei o botão buscar")

    time.sleep(1)

    if not attempt_action(monstros, device.clicar, delay_max=0, delay_min=0, confidence=0.6, max_attempts=50):
        logger.info("Não encontrei o grupo de monstros")

    if not attempt_action("ataque", device.clicar, max_attempts=3):
        logger.info("Não encontrei o botão de ataque")
        return procura_mobs()


def farm_exp(lvl=1):
    presets = {
        1: [702, 89],
        2: [745, 90]
    }

    procura_mobs(lvl)

    if not attempt_action("legiao_disponivel", device.clicar, max_attempts=40, delay_min=4, delay_max=5):
        logger.info("Não estás disponivel para combate")
        return farm_exp()

    if not attempt_action("criar_legioes", device.clicar, max_attempts=10):
        logger.info("Não encontrei o botão criar_legioes")

    if not attempt_action(presets, device.clicar, max_attempts=10):
        logger.info("Não encontrei o preset")

    if not attempt_action("marchar", device.clicar, max_attempts=5):
        logger.info("Não encontrei o botão marchar")

    if not attempt_action("home", device.clicar, max_attempts=3, delay_max=1):
        logger.info("Já devemos estar na cidade")


def hospital():
    if not attempt_action("hospital", device.clicar, max_attempts=5, delay_max=1):
        logger.info("Estão todos bem")
        return False

    if not attempt_action("curar", device.clicar, max_attempts=5, delay_max=1):
        logger.info("Não encontrei o botão de curar")

    device.device.shell(f"input tap 16 24")
    return True


def cidade():
    acoes = acoes_para_fazer()

    if not attempt_action("home", device.clicar, max_attempts=3, delay_max=1):
        logger.info("Já devemos estar na cidade")

    if not attempt_action(acoes, device.clicar, max_attempts=5, delay_max=1):
        logger.info("Não encontrei nada para fazer na cidade")
        return False

    return True


def nevoeiro():
    if not attempt_action("home", device.clicar, max_attempts=3):
        logger.info("Já devemos estar na cidade")

    if not attempt_action('acampamento', device.clicar, max_attempts=5, delay_max=1):
        logger.info("Não encontrei o acampamento")

    if not attempt_action('explorar', device.clicar, max_attempts=5, delay_max=1):
        logger.info("Não encontrei o 'explorar'")

    if not attempt_action('explorar_btn', device.clicar, max_attempts=20, delay_min=5, delay_max=6):
        logger.info("Não encontrei o 'explorar_btn'")

    if not attempt_action('explorar_btn2', device.clicar, max_attempts=10, delay_max=1):
        logger.info("Não encontrei o 'explorar_btn2'")

    if not attempt_action('marchar_batedor', device.clicar, max_attempts=10, delay_max=1, confidence=0.6):
        logger.info("Não encontrei o 'marchar_batedor'")

    if not attempt_action('home', device.clicar, max_attempts=10, delay_max=1):
        print("Já devemos estar na cidade")

    return True

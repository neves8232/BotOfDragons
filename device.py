import time
from PIL import ImageChops, Image
from ppadb.client import Client as AdbClient
import os
import pyautogui
import traceback


class Device:

    def __init__(self, debug):
        self.client = AdbClient(host="127.0.0.1", port=5037)
        self.device = self.client.device("emulator-5554")
        self.directory = os.getcwd()
        self.utils = f"{self.directory}\\utils"
        self.debug = False

    def tirar_print(self, file_name="screen", iguais=False):
        location = f"{self.utils}\\{file_name}.png"

        if iguais:

            time.sleep(0.5)
            # Take first screenshot
            result1 = self.device.screencap()
            location1 = f"{self.utils}\\{file_name}1.png"

            with open(location1, "wb") as fp:
                fp.write(result1)


            # Compare the two screenshots
            img1 = Image.open(location)
            img2 = Image.open(location1)

            diff = ImageChops.difference(img1, img2)

            import numpy as np

            diff_sum = np.array(diff).sum()

            threshold = 10_000_000

            # If diff_sum is below the threshold, the images are "essentially" identical
            return diff_sum < threshold

        else:
            result = self.device.screencap()

            with open(location, "wb") as fp:
                fp.write(result)

            return location

    def organizar_ficheiros(self, targets):
        if type(targets) == dict:

            return targets

        if not isinstance(targets, list):
            targets = [targets]

        target_final = [(f"{self.utils}\\target\\" + target + ".png") if not target.endswith('.png') else target for
                        target in targets]
        return target_final

    def localizar(self, target, confidence=0.8):
        screen = self.tirar_print()
        targets = self.organizar_ficheiros(target)

        for target in targets:
            try:
                x, y, w, h = pyautogui.locate(target, screen, confidence=confidence)
                x = x + round((w / 2))
                y = y + round((h / 2))

                return x, y
            except:
                if self.debug: traceback.print_exc()
                return False

    def localizar_pixel(self, coordenadas):
        time.sleep(1)
        imagem_path = self.tirar_print()
        imagem = Image.open(imagem_path).convert("RGB")
        r1, g1, b1 = imagem.getpixel((coordenadas[0], coordenadas[1]))

        print(r1, g1, b1)
        return r1, g1, b1


    def clicar(self, targets, confidence=0.8):

        targets = self.organizar_ficheiros(targets)

        if type(targets) == dict:

            r1, g1, b1 = pyautogui.pixel(703, 88)
            r2, g2, b2 = pyautogui.pixel(747, 88)

            if b2 > b1:
                self.device.shell(f"input tap {targets[2][0]} {targets[2][1]}")

            if b1 > b2:
                self.device.shell(f"input tap {targets[1][0]} {targets[1][1]}")

            if b1 == b2:
                self.device.shell(f"input tap {targets[1][0]} {targets[1][1]}")

            else:
                self.device.shell(f"input tap {16} {24}")
                return False

            return True
        for target in targets:
            try:
                x, y = self.localizar(target, confidence)
                self.device.shell(f"input tap {x} {y}")
                return True
            except TypeError:
                pass

        return False



    def arrastar(self, target, confidence=0.8):

        targets = self.organizar_ficheiros(target)

        for target in targets:
            try:
                duracao_s = 1 * 1000
                x1, y1 = self.localizar(target, confidence)
                x2, y2 = x1 + 250, y1

                self.device.shell(f"input swipe {x1} {y1} {x2} {y2} {duracao_s}")

                return True
            except TypeError:
                if self.debug: traceback.print_exc()

        return False


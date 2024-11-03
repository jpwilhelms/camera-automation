import digitalio
import board
import time

class Stopper:
    def __init__(self, pin):
        """
        Initialisiert den Stopper mit einem digitalen Eingang und einer Aktion.

        :param pin: Der Pin, der als digitaler Eingang verwendet wird.
        :param action: Eine Funktion, die ausgeführt wird, wenn der Wert von False auf True wechselt.
        """
        self.pin = digitalio.DigitalInOut(pin)
        self.pin.direction = digitalio.Direction.INPUT
        self.pin.pull = digitalio.Pull.UP
        self.previous_value = self.pin.value

    def check(self):
        """
        Überprüft den digitalen Eingang und führt die Aktion aus, wenn der Wert von False auf True wechselt.
        """
        current_value = self.pin.value
        result = self.previous_value and not current_value
        self.previous_value = current_value
        return result

    def isTriggered(self):
        return not self.pin.value

if __name__ == "__main__":
    # Stopper-Instanz erstellen
    stopper = Stopper(board.D5)

    # Endlos-Schleife zum Überprüfen des Eingangs
    while True:
        if stopper.check():
            print("Der Wert hat sich von False auf True geändert!")
        time.sleep(0.1)  # Kurze Pause, um die CPU-Auslastung zu reduzieren


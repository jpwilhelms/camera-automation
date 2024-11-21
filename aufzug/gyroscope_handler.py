import statistics
import threading
import time
from collections import deque
from gyroscope import Gyroscope


class GyroscopeHandler:
    def __init__(self, gyroscope: Gyroscope, number_for_average: int = 5):
        self.values = deque(maxlen=number_for_average) 
        self.running = False
        self.lock = threading.Lock()  # Thread-Sicherheit
        self.gyroscope = gyroscope
        self.thread = None

    def _read_gyroscope(self):
        while self.running:
            new_value = self.gyroscope.getXY()
            with self.lock:
                self.values.appendleft(new_value)

    def _is_initialized(self):
        with self.lock:
            return len(self.values) > 0

    def get_latest_result(self):
        return self.values[0]

    def get_average(self):
        """Berechnet den Mittelwert der letzten n Werte"""
        with self.lock:
            if len(self.values) == 0:
                return None
            transponiert = zip(*self.values)
            median_tupel = tuple(statistics.median(werte) for werte in transponiert)
            return median_tupel

    def is_flat(self,threshold):
        xy = self.get_average()
        result = all(abs(x) < threshold for x in xy)
        return result

    def start(self):
        """Startet den Gyroscope-Thread"""
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._read_gyroscope, daemon=True)
            self.thread.start()

            while not self._is_initialized():
                print( "waiting for init" )
                time.sleep( 0.1 )

    def stop(self):
        """Stoppt den Gyroscope-Thread"""
        self.running = False
        if self.thread:
            self.thread.join()
            self.thread = None

if __name__ == "__main__":
    hw = Hardware()
    gyroscope_handler = GyroscopeHandler( hw.gyroscope )
    gyroscope_handler.start()

    try:
        while True:
            time.sleep(2)
            avg = gyroscope_handler.get_average()
            print(f"Median der letzten Werte: {avg}")
    except KeyboardInterrupt:
        print("Beende Programm...")
    finally:
        gyroscope_handler.stop()
        hw.cleanup

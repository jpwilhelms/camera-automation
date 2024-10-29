#!/bin/env bash
if [ -n "$1" ]; then
    # Prüfen, ob der Parameter numerisch ist
    if [[ "$1" =~ ^[0-9]+$ ]]; then
        counter=$1
    else
        echo "Fehler: Der angegebene Parameter ist nicht numerisch."
        exit 1
    fi
else
    # Standardwert setzen, falls kein Parameter angegeben wurde
    counter=1
fi

raspi-gpio set 26 ip pd
raspi-gpio set 21 op dl

while true; do
  echo Kiste $counter für Foto bereitstellen
  while test $(gpioget gpiochip0 26) == 1; do
    sleep 0.1
  done
  echo Foto wird aufgenommen
  raspi-gpio set 21 dh
  raspistill -o bild-$counter.jpg
  raspi-gpio set 21 dl
  echo Kiste entnehmen
  while test $(gpioget gpiochip0 26) == 0; do
    sleep 0.1
  done
  ((counter++))
done

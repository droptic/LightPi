#!/usr/local/bin/python
import RPi.GPIO as GPIO
import time
from subprocess import call

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

# Pin al que está conectado el sensor LDR
PIN_TO_CIRCUIT = 7
# Punto de corte para luz encendida y apagada
LUX_THRESHOLD = 10000
# Tiempo que la lectura debe mantenerse en oscuridad antes de apagar
OFF_DELAY_SECONDS = 5
# Tiempo entre mediciones consecutivas
SAMPLE_INTERVAL = 1


def rc_time(pin_to_circuit: int) -> int:
    """Lee el tiempo de carga del sensor conectado al pin indicado."""
    count = 0

    # Output on the pin for
    GPIO.setup(pin_to_circuit, GPIO.OUT)
    GPIO.output(pin_to_circuit, GPIO.LOW)
    time.sleep(0.1)

    # Change the pin back to input
    GPIO.setup(pin_to_circuit, GPIO.IN)

    # Count until the pin goes high
    while GPIO.input(pin_to_circuit) == GPIO.LOW:
        count += 1

    return count


def set_display_power(turn_on: bool, reading: int) -> None:
    """Enciende o apaga la pantalla según el estado solicitado."""
    state = "1" if turn_on else "0"
    action = "Screen on" if turn_on else "Screen off"
    print(f"{action} {reading}")
    call(["/usr/bin/vcgencmd", "display_power", state])


def main() -> None:
    screen_on = False
    darkness_started_at = None

    while True:
        reading = rc_time(PIN_TO_CIRCUIT)

        if reading < LUX_THRESHOLD:
            # Reiniciamos el temporizador de oscuridad y encendemos si es necesario.
            darkness_started_at = None
            if not screen_on:
                set_display_power(True, reading)
                screen_on = True
        else:
            if darkness_started_at is None:
                darkness_started_at = time.monotonic()
            elif screen_on and (time.monotonic() - darkness_started_at) >= OFF_DELAY_SECONDS:
                # Comprobamos nuevamente que la oscuridad persista antes de apagar.
                confirmation = rc_time(PIN_TO_CIRCUIT)
                if confirmation >= LUX_THRESHOLD:
                    set_display_power(False, confirmation)
                    screen_on = False
                    darkness_started_at = None

        time.sleep(SAMPLE_INTERVAL)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()

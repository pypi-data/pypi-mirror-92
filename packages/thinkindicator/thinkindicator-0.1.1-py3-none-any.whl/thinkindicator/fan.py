import re

from .errors import ProcReadException, ProcWriteException

LEVELS = [
    "0",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "auto",
    "disengaged",
    "full-speed",
]


def get_level():
    try:
        with open("/proc/acpi/ibm/fan") as fan:
            for line in fan:
                if not line.startswith("level"):
                    continue

                match = re.search(r"([0-7]|auto|disengaged|full-speed)$", line)

                if not match:
                    raise ProcReadException(
                        "The fan is in an unknown state! " + line
                    )

                return match[1]
    except FileNotFoundError:
        raise ProcReadException(
            "There is no /proc/acpi/ibm/fan on your computer. "
            "Load kernel module thinkpad_acpi."
        )


def set_level(level: str):
    if level not in LEVELS:
        raise ProcWriteException("Invalid level.")

    with open("/proc/acpi/ibm/fan", "w") as fan:
        fan.write(f"level {level}")

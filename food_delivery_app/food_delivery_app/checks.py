import re
from typing import List
from django.core.checks import register
from django.core.checks.messages import CheckMessage, DEBUG, INFO, WARNING, ERROR
from django.conf import settings

from mypy import api


class MyPyErrorLocation:
    def __init__(self, location):
        self.location = location

    def __str__(self):
        return self.location


@register()
def mypy(app_configs, **kwargs) -> List:
    print("Performing mypy checks...\n")

    mypy_args = [str(settings.BASE_DIR)]
    results = api.run(mypy_args)
    error_messages = results[0]

    if not error_messages:
        return []

    pattern = re.compile("^(.+\d+): (\w+): (.+)")

    errors = []
    for message in error_messages.rstrip().split("\n"):
        parsed = re.match(pattern, message)
        if not parsed:
            continue

        location = parsed.group(1)
        mypy_level = parsed.group(2)
        message = parsed.group(3)

        level = DEBUG
        if mypy_level == "note":
            level = INFO
        elif mypy_level == "warning":
            level = WARNING
        elif mypy_level == "error":
            level = ERROR
        else:
            print(f"Unrecognized mypy level: {mypy_level}")

        errors.append(CheckMessage(level, message, obj=MyPyErrorLocation(location)))

    return errors
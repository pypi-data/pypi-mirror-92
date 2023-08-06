import logging
import typing
from typing import Optional, Text

from convo.shared.utils.cli import print_info, print_success
from convo.shared.nlu.interpreter import RegexInterpreter
from convo.shared.constants import INTENT_MESSAGE_PREFIX
from convo.nlu.model import Interpreter
from convo.shared.utils.io import json_to_string
import convo.utils.common

if typing.TYPE_CHECKING:
    from convo.nlu.components import ComponentBuilder

logger = logging.getLogger(__name__)


def run_cmdline(
    model_path: Text, component_builder: Optional["ComponentBuilder"] = None
) -> None:
    interpreter = Interpreter.load(model_path, component_builder)
    regex_interpreter = RegexInterpreter()

    print_success("NLU model loaded. Type a message and press enter to parse it.")
    while True:
        print_success("Next message:")
        try:
            message = input().strip()
        except (EOFError, KeyboardInterrupt):
            print_info("Wrapping up command line chat...")
            break

        if message.startswith(INTENT_MESSAGE_PREFIX):
            result = convo.utils.common.run_in_loop(regex_interpreter.parse(message))
        else:
            result = interpreter.parse(message)

        print(json_to_string(result))

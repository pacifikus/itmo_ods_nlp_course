from dialogic import COMMANDS
from dialogic.cascade import DialogTurn

from dialog_manager import csc
from scenarios.translator import make_translation_response


def is_single_pass(turn: DialogTurn) -> bool:
    if not turn.ctx.yandex:
        return False
    if not turn.ctx.yandex.session.new:
        return False
    return bool(turn.ctx.yandex.request.command)


def is_new_session(turn: DialogTurn):
    return turn.ctx.session_is_new() or not turn.text


@csc.add_handler(priority=100, checker=is_single_pass)
def single_pass(turn: DialogTurn):
    make_translation_response(turn)
    turn.commands.append(COMMANDS.EXIT)


@csc.add_handler(priority=10, regexp='(hello|hi|привет|здравствуй|старт)')
@csc.add_handler(priority=3, checker=is_new_session)
@csc.add_handler(priority=0)
def hello(turn: DialogTurn):
    turn.response_text = 'Привет! Вы в навыке "Переводчик". ' \
                         'Напишите любую фразу на украинском языке, ' \
                         'а я переведу ее на русский'
    turn.suggests.append('выход')


@csc.add_handler(priority=10, intents=['help', 'Yandex.HELP', 'like_alice'])
def do_help(turn: DialogTurn):
    turn.response_text = 'Привет! Вы в навыке "Переводчик". ' \
                         'Напишите любую фразу на украинском языке, ' \
                         'а я переведу ее на русский' \
                         '\nЧтобы выйти, скажите "хватит".'
    turn.suggests.append('выход')


@csc.add_handler(priority=10, intents=['total_exit'])
def total_exit(turn: DialogTurn):
    turn.response_text = 'Было приятно пообщаться! ' \
                         'Чтобы обратиться ко мне снова, ' \
                         'запустите навык "Супер переводчик".'
    turn.commands.append(COMMANDS.EXIT)


@csc.add_handler(priority=1)
def translation_fallback(turn: DialogTurn):
    if not turn.text:
        return
    make_translation_response(turn)

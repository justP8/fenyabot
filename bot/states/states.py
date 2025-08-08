from aiogram.fsm.state import State, StatesGroup


class MyStates(StatesGroup):
    setting_rules = State()
    rules_confirmation = State()
    resetting_rules = State()

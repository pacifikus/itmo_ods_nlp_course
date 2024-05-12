import yaml
from dialogic.cascade import Cascade, DialogTurn
from dialogic.dialog import Response
from dialogic.dialog_manager import TurnDialogManager


from dialogic.nlu.matchers import make_matcher_with_regex, TextDistanceMatcher

csc = Cascade()


class SmartDM(TurnDialogManager):
    def postprocess_response(self, response: Response, turn: DialogTurn):
        response.updated_user_object['prev'] = {
            'text': response.text,
            'voice': response.voice,
            'suggests': response.suggests,
            'stage': turn.next_stage
        }

    def load_intents(self, intents_file=None):
        with open(intents_file, 'r', encoding='utf-8') as f:
            self.intents = yaml.safe_load(f)

        self.intent_matcher = make_matcher_with_regex(
            base_matcher=TextDistanceMatcher(),
            intents=self.intents,
        )


def make_dm() -> TurnDialogManager:
    dm = SmartDM(
        cascade=csc,
        intents_file='data/intents.yaml',
    )
    return dm

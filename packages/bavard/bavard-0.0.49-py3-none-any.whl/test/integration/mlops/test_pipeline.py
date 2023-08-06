from unittest import TestCase
import os

import requests

from bavard.dialogue_policy.data.conversations.conversation import Conversation
from bavard.mlops.pydantics import ChatbotPipelinePredictions, ChatbotPipelineInputs


class TestPipeline(TestCase):
    def setUp(self) -> None:
        self.test_conv = Conversation.parse_obj({
            "turns": [
                {
                    "actor": "USER",
                    "state": {
                        "slotValues": []
                    },
                    "userAction": {
                        "type": "UTTERANCE_ACTION",
                        "utterance": "Bon matin, David.",
                        "translatedUtterance": "Good morning, David.",
                        "intent": ""
                    }
                }
            ]
        })
        self.API_HOST = os.environ["API_HOST"]
        self.pipeline_inputs = ChatbotPipelineInputs(instances=[self.test_conv])

    def test_running_prediction_container(self):
        # Makes requests directly to a running prediction container.
        res = requests.post(f"{self.API_HOST}/predict", data=self.pipeline_inputs.json())
        self.assertEqual(res.status_code, 200)
        # Return value should be a valid prediction
        preds = ChatbotPipelinePredictions.parse_obj(res.json())
        self.assertEqual(len(preds.predictions), 1)

        self.assertDictEqual(res.json()['predictions'][0]['nlu']['tags'][0], {
            'tagType': 'TIME',
            'value': 'morning'
        })
        self.assertDictEqual(res.json()['predictions'][0]['nlu']['tags'][1], {
            'tagType': 'PERSON',
            'value': 'David'
        })

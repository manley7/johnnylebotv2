from rasa_core.channels.telegram import TelegramInput
from rasa_core.agent import Agent
from rasa_core.interpreter import RasaNLUInterpreter
import yaml
from rasa_core.utils import EndpointConfig


nlu_interpreter = RasaNLUInterpreter('./models/banque_finalv2/nlu')
action_endpoint = EndpointConfig(url="http://localhost:5055/webhook")
agent = Agent.load('./models/banque_finalv2/dialogue', interpreter = nlu_interpreter, action_endpoint = action_endpoint)

input_channel = TelegramInput("699840177:AAF0m4L7MzeyJroyC9Wx944W1VNOsOZjkXY", "JohnnyMonConseiller_bot", "https://1a36a98b.ngrok.io/webhooks/telegram/webhook", True)

agent.handle_channels([input_channel], 5004, serve_forever=True)


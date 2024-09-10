from agent import AIServiceAgent
from services import example_service_1, example_service_2, service_info_1, service_info_2

agent = AIServiceAgent()
agent.register(example_service_1, service_info_1)
agent.register(example_service_2, service_info_2)
ret = agent.run_service("너무 심심해서 웃고 싶어. 하늘과 해가 날 재밌게 만들어 줬으면")
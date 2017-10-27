from channels import route
from . import consumers

#Routing específico para los channels
channel_routing = [
    route("websocket.connect", consumers.ws_connect),
    route("websocket.disconnect", consumers.ws_disconnect),
    route("websocket.receive", consumers.ws_receive)
]

#Routing espefífico para el chat
chat_routing = [
    #En caso de recibir un mensaje con command join
    route("chat.receive", consumers.chat_join, command="^join$"),
    #En caso de recibir un mensaje con command join
    route("chat.receive", consumers.chat_leave, command="^leave$"),
    #En caso de recibir un mensaje con command join
    route("chat.receive", consumers.chat_send, command="^send$"),
]
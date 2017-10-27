from channels import include

channel_routing = [
    include("demo.routing.channel_routing", path=r'^/chat/stream/'),
    include("demo.routing.chat_routing"),
]
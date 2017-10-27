from channels.auth import channel_session_user_from_http, channel_session_user
from .models import Room
import json
from channels import Channel

'''Agregamos esté decorador para obtener el usario desde la sesión http 
y agregarlo a la sesión del channel correspondiente'''
@channel_session_user_from_http
def ws_connect(message):
    '''función (no obligatoria) para cuándo un usuario se conecte a nuestros sockets'''
    print(message.reply_channel)
    message.reply_channel.send({"accept":True})
    message.channel_session["rooms"] = []
    print("conectado " + message.user.username)

@channel_session_user
def ws_disconnect(message):
    '''función (no obligatoria) para cuándo un usuario se desconecte de nuestros sockets'''
    for roomid in message.channel_session.get('rooms', set()):
        try:
            room = Room.objects.get(pk=roomid)
            room.websocket_group.discard(message.reply_channel)
        except Room.DoesNotExist:
            pass

def ws_receive(message):
    '''función para cachar los mensaje que envié el usuario'''
    #obtenemos el content del message del browser
    payload = json.loads(message["text"]) 
    #Quien envió el mensaje y lo agregamos a payload
    payload['reply_channel'] = message.content["reply_channel"] 
    #Mandamos el mensaje al chat.receive, este lo cachará el chat_routing en routing.py
    Channel('chat.receive').send(payload)

@channel_session_user
def chat_join(message):
    '''Función para cuando un usuario elija una sala de chat'''
    #obtenemos el room al que se quiere conectar
    room = Room.objects.get(pk=message["room"])
    #obtenemos el usuario que se quiere conectar
    usr = message.user
    
    #Mandamos un mensaje al grupo de que se unió un channel al chat de ese grupo
    room.send_message("Bienvenido", usr)
    #Agregamos el channel al grupo, esté channel contiene la info del usuario
    room.websocket_group.add(message.reply_channel)
    #Agregamos a la sesión el roomid a los cuales el usuario está conectado
    message.channel_session["rooms"] = list(set(message.channel_session['rooms']).union([room.id]))

    #Mandamos un mensaje al channel de que fue aceptado en la sala
    message.reply_channel.send({
        "text": json.dumps({
            "join": str(room.id),
            "title": room.title,
        }),
    })

@channel_session_user
def chat_send(message):
    #obtenemos el room al que se quiere enviar el mensaje
    room = Room.objects.get(pk=message["room"])
    #enviamos el mensaje al grupo
    room.send_message(message["message"], message.user)


def chat_leave(message):
    #obtenemos el room del que se quiere desconectar
    room = Room.objects.get(pk=message["room"])
    #obtenemos el usuario que se quiere desconectar
    usr = message.user

    #Eliminamos al usuario del grupo
    room.websocket_group.discard(message.reply_channel)

    #Eliminamos de la sesión del channel el room del qué se desconectó
    message.channel_session["rooms"] = list(set(message.channel_session["room"]).difference(room.id))

    #Enviamos un mensaje al channel de desconexión
    message.reply_channel.send({
        "text": json.dumps({
            "leave": str(room.id),
        }),
    })





from django.db import models
from channels import Group
import json
# Create your models here.
class Room(models.Model):
    title = models.CharField(max_length=255)
    staff_only = models.BooleanField(default=False)

    '''Creamos una propiedad del tipo Group, para qué
    al momento de crearse un nuevo room esté tenga ya 
    una instancia creada del tipo Group en donde se 
    irán agregando los channels que así lo deseen a 
    travéz de los consumers'''
    @property
    def websocket_group(self):
        return Group(f"room-{self.id}")

    '''Se envía un mensaje al grupo de este room,
    en el mensaje. Como argumentos recibimos el 
    texto del mensaje que vamos a enviar, así como
    el usuario qué lo está enviando'''
    def send_message(self, message, user):
        msg = {"room": str(self.id), 'message':message, 'username':user.username}
        
        '''Utiliza la instancia de group del propio room para enviar el
        mensaje a sus integrantes'''
        self.websocket_group.send(
            {"text":json.dumps(msg)}
        )

    def __str__(self):
        return self.title
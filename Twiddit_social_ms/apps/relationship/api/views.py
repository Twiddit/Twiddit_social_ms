from apps.relationship.models import *
from apps.relationship.api.serializers import *
from rest_framework import generics
from rest_framework.response import Response
from .sender import MQConnection

class FollowersList(generics.ListAPIView): #Obtener usuarios que siguen a una cuenta
    serializer_class = RelationshipSerializer
    queryset = Relationship.objects.all()

    def get(self, request, id): 
        qs = self.queryset.filter(followedId = id).filter(blocked = False)
        serializer = self.serializer_class(qs, many = True)
        return Response(serializer.data)

class FollowingList(generics.ListAPIView): #Obtener usuarios que a los que sigue una cuenta
    serializer_class = RelationshipSerializer
    queryset = Relationship.objects.all()

    def get(self, request, id): 
        qs = self.queryset.filter(followerId = id).filter(blocked = False)
        serializer = self.serializer_class(qs, many = True)
        return Response(serializer.data)


class BlockedList(generics.ListAPIView): #Obtener usuarios que siguen a una cuenta
    serializer_class = RelationshipSerializer
    queryset = Relationship.objects.all()

    def get(self, request, id): 
        qs = self.queryset.filter(followedId = id).filter(blocked = True)
        serializer = self.serializer_class(qs, many = True)
        return Response(serializer.data)

class NumberFollowers(generics.RetrieveAPIView): #Obtener numero de seguidores de una cuenta
    serializer_class = RelationshipFollowersSerializer
    queryset = Relationship.objects.all()

    def get(self, request, id): 
        qs = self.queryset.filter(followedId = id).filter(blocked = False).first()
        if qs != None:
            qs = Relationship.objects.filter(id = qs.id)
            serializer = self.serializer_class(qs, many = True)
            return Response(serializer.data[0])
        else:
            return Response({"numberFollowers" : 0})

class NumberFollowing(generics.RetrieveAPIView): #obtener numero de seguidos de una cuenta
    serializer_class = RelationshipFollowingSerializer
    queryset = Relationship.objects.all()

    def get(self, request, id): 
        qs = self.queryset.filter(followerId = id).filter(blocked = False).first()
        if qs != None:
            qs = Relationship.objects.filter(id = qs.id)
            serializer = self.serializer_class(qs, many = True)
            return Response(serializer.data[0])
        else:
            return Response({"numberFollowing" : 0})

class NumberBlocked(generics.RetrieveAPIView): #Obtener numero de bloqueados de una cuenta
    serializer_class = RelationshipBlockedSerializer
    queryset = Relationship.objects.all()

    def get(self, request, id): 
        qs = self.queryset.filter(followedId = id).filter(blocked = True).first()
        if qs != None:
            qs = Relationship.objects.filter(id = qs.id)
            serializer = self.serializer_class(qs, many = True)
            return Response(serializer.data[0])
        else:
            return Response({"numberBlocked" : 0})

class Disblock(generics.RetrieveDestroyAPIView):
    serializer_class = RelationshipSerializer

    def get(self, request, followerId, followedId): #Consultar si un usuario bloqueo a otro usuario
        try:
            obj = Relationship.objects.get(followerId = followerId, followedId = followedId, blocked = True)
            return Response({"blocked" : True})
        except:
            return Response({"blocked" : False})


    def delete(self, request, followerId, followedId): #Desbloquear una cueenta
        try:
            obj = Relationship.objects.get(followerId = followerId, followedId = followedId, blocked = True)
            obj.delete()
            return Response({"message" : "Se ha desbloqueado al usuario correctamente"})
        except:
            return Response({"message" : "Ha ocurrido un error"})


class Unfollow(generics.RetrieveDestroyAPIView):
    serializer_class = RelationshipSerializer


    def get(self, request, followerId, followedId):#Cnosultar si un usuario sigue a otro
        try:
            obj = Relationship.objects.get(followerId = followerId, followedId = followedId, blocked = False)
            return Response({"follow" : True})
        except:
            return Response({"follow" : False})


    def delete(self, request, followerId, followedId): #Dejar de seguir a un usuario
        try:
            obj = Relationship.objects.get(followerId = followerId, followedId = followedId, blocked = False)
            obj.delete()
            return Response({"message" : "Se ha dejado de seguir al usuario correctamente"})
        except:
            return Response({"message" : "Ha ocurrido un error"})


class CreateRelationship(generics.CreateAPIView): #Empezar a seguir o bloquear a un usuario


    serializer_class = RelationshipSerializer

    def post(self, request):
        mensaje = "seguido"
        try:
            if request.data["blocked"]:
                mensaje = "bloqueado"
        except:
            pass
        try:
            relationship = Relationship.objects.get(followerId = request.data["followerId"], followedId = request.data["followedId"])
            if relationship.blocked:
                return Response({"message" : "Primero debes desbloquear a este usuario antes de seguirlo"})
            relationship.delete()
        except: 
            pass
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            # Creación de una instancia de la cola de mensajes 
            messageQueue = MQConnection()
            # Configuración de la cola 
            messageQueue.createConnection('172.17.0.1', 'notifications')
            # Crear la notificacion
            if mensaje == "seguido":
                follower = request.data["followerId"]
                followed = request.data["followedId"]
                notification = f"{follower}.{followed}"
                messageQueue.sendNotification('notifications', notification)
            # Cerramos la conexión de envio en la cola    
            messageQueue.closeConnection()
        
            serializer.save()
            return Response({"message" : f"usuario {mensaje} exitosamente"})
        return Response(serializer.errors)



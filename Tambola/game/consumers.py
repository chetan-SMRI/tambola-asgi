import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from game.views import last_called_no
import asyncio
from threading import Thread
import time
from asgiref.sync import sync_to_async


class GetLastValues(AsyncJsonWebsocketConsumer):
    async def websocket_connect(self,event):
        self.room = self.scope['url_route']['kwargs']['room_code']
        await self.channel_layer.group_add(
            self.room,
            self.channel_name
        )
        
        
        await self.accept()
        
                    
    async def websocket_receive(self, text_data):
        """
        Receive message from WebSocket.
        Get the event and send the appropriate event
        """
        # response = json.loads(text_data)

        message = await last_called_no()
        await self.send(json.dumps({
            'type': 'websocket.send',
            'text': message,
            "event": "MOVE"
        }))
        

    async def websocket_disconnect(self, close_code):
        print("Disconnected")
        # Leave room group
        # await self.channel_layer.group_discard(
        #     self.room_group_name,
        #     self.channel_name
        # )

    

    async def websocket_send_message(self):
        """ Receive message from room group """
        # Send message to WebSocket
        await self.send(json.dumps({
            'type': 'websocket.send',
            'payload': 'pong',
        }))
        # self.websocket_send_message()

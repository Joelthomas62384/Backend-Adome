from channels.generic.websocket import AsyncWebsocketConsumer
import json
from channels.db import database_sync_to_async
from . serializers import *
from app.models import *
from asgiref.sync import sync_to_async


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"chat_{self.room_name}"
        self.tenant = self.scope['tenant']
        self.tenantuser = self.scope['tenantuser']
        self.user = self.scope['user']
        self.userscope = self.scope['userscope']
        self.community = await self.get_community()
        # print(self.scope.path)

        # if not (self.tenant and self.tenantuser and self.user and self.community) : 
        #     self.close()
        #     return

        await self.channel_layer.group_add(self.room_group_name , self.channel_name)
        tenantuser_str = await sync_to_async(str)(self.tenantuser)
        print(tenantuser_str)
        print(await sync_to_async(str)(self.community))
        print("Connected")
        await self.accept()
    
    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)

        # messages = text_data_json["message"]
        # print(messages)
        if text_data_json['contenttype'] in ['1', '2', '3', '4']:
            messages = await self.save_message(text_data_json)


            await self.channel_layer.group_send(
                self.room_group_name, {"type": "chat.message", "message": messages}
            )
    
    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )



    async def chat_message(self, event):
        message = event["message"]

        await self.send(text_data=json.dumps({
            "message": message
        }))

    @database_sync_to_async
    def get_community(self):
        try:
            community = Community.objects.get(id=self.room_name)
            return community
        except Exception as e :
            print(e)
            return None
    
    @database_sync_to_async
    def save_message(self , message) :
        serializer = CommunityChatSerializer(data =message)
        if serializer.is_valid():
            serializer.save(tenant = self.tenant , user=self.tenantuser, community = self.community)
            return serializer.data
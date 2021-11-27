import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from account.models import MyUser
from myapp.models import Chat

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        
        self.accept()

    
    chat_collection = []
    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        
        )

    def list_collection(self):
        
        for msg in  Chat.last_ten_msg(self,self.room_name):
            self.chat_collection.append({
                'objs' :{'user_name':msg.author.username,'message' : msg.message}
            })
        return self.chat_collection

    def create_object(self,author_name,text_message):
        Chat.objects.create(room_name = self.room_name,author = author_name, message = text_message)

    def print_statement(self):
        print('hello hi howa areah')


    def receive(self, text_data):
        self.chat_collection = []
        text_data = json.loads(text_data)
        print(text_data)
        if(text_data['command'] == 'chat_message'):
            json_data = self.list_collection()
            self.chat_msg(json_data)
        
        

        else:
            
            text_message = text_data['message']
            user = text_data['user_name']
            author_name = MyUser.objects.get(username = user)
            self.create_object(author_name,text_message)

        
            async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': text_message,
                'message_type':text_data['command'],
                'user_name' : user
            }
        )

        # print(json.dumps(self.chat_collection))
        

        

    def chat_message(self,event):
        message = event['message']
        message_type = event['message_type']
        user_name = event['user_name']
        self.send(json.dumps({'message':message,'message_type':message_type,'user_name':user_name}))
        

    def chat_msg(self,event):
        self.send(json.dumps(event))



        
            
        



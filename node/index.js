const express = require('express');
const app = new express();
var cors = require('cors')
const http = require('http');
const server = http.createServer(app);
const {Server} = require('socket.io');
const io = require('socket.io')(server,{
  cors:{
    origin:'http://127.0.0.1:8000'
  }
});
let id =  {}
let users = {}




io.on('connection',(socket)=>{
    console.log(socket.id);
    
    console.log("connected");
    socket.on('disconnect', () => {
        console.log('user disconnected');
        if(socket.id in users){
          console.log('hello')
          delete users[socket.id]
          console.log('user disconnected',id)
          io.emit('disconnects',id);
        }
        else{
          delete id[socket.id]
          console.log('user disconnected',id)
          io.emit('disconnects',id);

        }
        
      });
    
    socket.on("private chat",(data)=>{
      users[socket.id]=data.user
      console.log(data.room_name)
      socket.join(data.room_name)
      io.emit("private chat",users)
      //io.sockets.in(data.room_name).emit('private chat', users);

    })

    // console.log("socket id",socket.id)
    socket.on('chat message' ,(msg)=>{
        console.log('user disconnects')
        console.log('message:',msg.user);

        //id.push({'msg':msg.user,'id':id});
        id[socket.id] = [{'user':msg.user,'socket':socket.id}];
        console.log(id)
        
        io.emit('chat message',id);
        

        //socket.broadcast.to('home').emit(' chat message', msg);
    });

    //private chat
    socket.on('new message',(data)=>{
      console.log(data.receiver)
      function getKeyByValue(object, value) {
        return Object.keys(object).find(key => object[key] === value);
      }
    let x = getKeyByValue(users,data.receiver);
    console.log('socket-id',x)
    //socket.broadcast.to(x).emit('new message', data.msg);
    io.sockets.in(data.room_name).emit('new message', data);

    })


    

});

app.get('/',(req,res) =>{
    res.send('hello');
});

// app.get('/home',(req,res)=>{
    
    // res.sendFile(__dirname + '/home.html');
// });
PORT = 3000;

server.listen(PORT,()=>{console.log(`server started at port${PORT}`)});

var http = require("http");
const socketio = require("socket.io")
const express = require("express");
const path = require("path");

const app = express();
const port =  "8000";

app.use(express.static(path.join(__dirname, './src')))

const server = http.createServer(app) 

server.listen(3000, () => {
  console.log("Server Running")
})

const io = socketio(server)

app.set("view engine", "ejs")
const {PythonShell} =require('python-shell');

app.get('/', (req, res) => {
  res.render(path.resolve(__dirname + '/src/pages/home'))
});


io.on('connection', socket => {
    let options = {
      mode: 'text',
      pythonOptions: ['-u'], // get print results in real-time
      args: [''] //An argument which can be accessed in the script using sys.argv[1]
    };
    var dataVar
    
    PythonShell.run('./src/pysrc/getNewTitle.py', options, function (err, result){
      if (err) throw err;
      dataVar = result.toString()
      socket.emit('getArticle', dataVar)
    });
    socket.on('anotherArticle', () => {
      PythonShell.run('./src/pysrc/getNewTitle.py', options, function (err, result){
        if (err) throw err;
        dataVar = result.toString()
        socket.emit('getArticle', dataVar)
      });
    })
})




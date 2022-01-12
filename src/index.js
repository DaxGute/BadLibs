var https = require("https");
const socketio = require("socket.io")
var fs = require("fs");
var request = require('request');
const bodyParser = require('body-parser');
const express = require("express");
const path = require("path");

const app = express();
const port =  "8000";

app.use(express.static(path.join(__dirname, './')))

app.listen(3000, () => {
  console.log("Server Running")
})

const io = socketio(app.server)

app.set("view engine", "ejs")
const { spawn } = require('child_process');

app.get('/', (req, res) => {
  // const pyProg = spawn('python', ['./pysrc/getNewTitle.py']);

  // pyProg.stdout.on('data', function(data) {
  //   console.log(data.toString());
  //   res.write(data);
  //   res.end('end');
  // });

  res.render(path.resolve(__dirname + '/pages/home'))
});
app.get()
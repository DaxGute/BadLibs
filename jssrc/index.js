/**
 * Required External Modules
 */

var https = require("https");
const socketio = require("socket.io")
var fs = require("fs");
var request = require('request');
const bodyParser = require('body-parser');

var agentOptions;
var agent;

const express = require("express");
const path = require("path");

const app = express();
const port = process.env.PORT || "8000";

app.use(express.static(path.join(__dirname, './')))

app.listen(3000, () => {
  console.log("Server Running")
})

const io = socketio(app.server)

app.set("view engine", "ejs")
app.get('/', (req, res) => {
  res.render(path.resolve(__dirname + '/pages/home'))
});
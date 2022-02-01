'use strict';

// [START appengine_websockets_app]
const express = require('express');
const app = require('express')();
app.set('view engine', 'pug');

const server = require('http').Server(app);
const io = require('socket.io')(server);

const path = require("path");
app.use(express.static(path.join(__dirname, './src')))

app.get('/', (req, res) => {
  res.render('home.ejs');
});

const {PythonShell} = require('python-shell');
io.on('connection', socket => {
  let options = {
    mode: 'text',
    pythonOptions: ['-u'], // get print results in real-time
    args: [''] //An argument which can be accessed in the script using sys.argv[1]
  };
  var dataVar
  

  PythonShell.run('./src/pysrc/getNewTitle.py', options, function (err, result){
    if (err) throw err;
    var dataVar = result.toString()
    socket.emit('getArticle', dataVar)
  });
  socket.on('anotherArticle', () => {
    PythonShell.run('./src/pysrc/getNewTitle.py', options, function (err, result){
      if (err) throw err;
      dataVar = result.toString()
      socket.emit('getArticle', dataVar)
    });
  })
});

if (module === require.main) {
  const PORT = process.env.PORT || 8080;
  server.listen(PORT, () => {
    console.log(`App listening on port ${PORT}`);
    console.log('Press Ctrl+C to quit.');
  });
}
// [END appengine_websockets_app]

module.exports = server;


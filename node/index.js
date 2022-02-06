'use strict';

// [START appengine_websockets_app]
const express = require('express');
const app = require('express')();
const fetch = require('node-fetch');
app.set('view engine', 'pug');

const server = require('http').Server(app);
const io = require('socket.io')(server);

const path = require("path");
app.use(express.static(path.join(__dirname, './src')))

app.get('/', (req, res) => {
  res.render('home.ejs');
});

io.on('connection', socket => {

  fetch('https://python-dot-badlibs.uc.r.appspot.com')
        .then(res => res.json())
        .then((json) => {
            var dataVar = json.message;
            socket.emit('getArticle', dataVar)
        });

  socket.on('anotherArticle', () => {
    fetch('https://python-dot-badlibs.uc.r.appspot.com')
        .then(res => res.json())
        .then((json) => {
            var dataVar = json.message;
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


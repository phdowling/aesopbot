var express = require('express');
var router = express.Router();
var app = require("../app");

app.io.on("connection", function (socket) {
  socket.emit("general", "Hello!");
});

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: 'Express' });
});

router.post('/new_lyrics', function (req, res, next) {
  var lyrics = req.body.lyrics;
  var isGenerated = req.body.isGenerated;
  io.sockets.emit(isGenerated? "lyrics": "seed", lyrics)
});


module.exports = router;

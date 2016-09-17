var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
  res.io.emit("general", "Hello!");
  res.render('index', { title: 'Express' });
});

router.post('/new_lyrics', function (req, res, next) {
  //console.log("New lyrics!");
  //console.log(JSON.stringify(req.body));
  var lyrics = req.body.lyrics;
  var isGenerated = req.body.isGenerated;
  res.io.sockets.emit(isGenerated? "lyrics": "seed", lyrics)
  res.send("Okay");
});


module.exports = router;

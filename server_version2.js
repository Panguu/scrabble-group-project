const express = require('express')
const app = express()
const port = 3000
const rows = 15
const cols = 15

player_rack = {}

board = {}
var maxplayers = 2
var turn = 1
var i;
for (i = 0; i < rows; i++) {
  board[i] = [];
  for (j = 0; j < cols; j++) {
    board[i].push('-');
  }
}

app.get('/', (req, res) => {
  res.send('Scrabble Game')
})

app.get('/setmaxplayers', (req, res) => {
  maxplayers = Number(req.param('maxplayers'))
})

app.get('/getmaxplayers', (req, res) => {
  res.send(turn)
})

app.get('/reset', (req, res) => {
  board = {}
  var i;
  for (i = 0; i < rows; i++) {
    board[i] = [];
    for (j = 0; j < cols; j++) {
      board[i].push('-');
    }
  }
  res.send(req.param('tilepos'));
})
app.get('/display', (req, res) => {
  var state_text = '';
  for(i=0; i<Object.keys(board).length; i++) {
    for(j=0; j<board[i].length; j++) {
      state_text += ' ';
      state_text += board[i][j];
      state_text += ' ';
    }
    state_text += "<br>";
  }
  state_text += 'Turn: Player '
  state_text += turn
  state_text += '<br>'
  Object.keys(player_rack).forEach(function(key) {
    state_text += 'player '
    state_text += key
    state_text += ': '
    state_text += player_rack[key]
    state_text += '<br>'
  });
  res.send(state_text)
})

app.get('/settile', (req, res) => {
  console.log("Set tile")
  turn = Number(req.param('turn'))
  if (Number(turn) > Number(maxplayers)) {
	turn = 1
  }
  //console.log(board)
  if (player_rack[req.param('player')].includes(req.param('char'))) {
    board[Number(req.param('y'))].splice(Number(req.param('x')), 1, req.param('char'));
    //turn = Number(req.param('turn'));
    //delete(player_rack[req.param('player')].req.param('char'))
    /*
    for (var i = player_rack[req.param('player')].length - 1; i >= 0; i--) {
      if (player_rack[req.param('player')][i] === req.param('char')) {
	console.log(player_rack[req.param('player')])
        player_rack[req.param('player')].splice(i, 1);
      }
    }
    */
    res.send('character set.');
  } else {
	  if ((player_rack[req.param('player')].length) == 0) {
		  res.send("no more tiles in rack.")
	} else {
	    res.send('character not set, since tile not in rack')
	}
  }
})
app.get('/setrack', (req, res) => {
  player_rack[req.param('player')] = (req.param('rack'))
  console.log(player_rack[req.param('player')])
  res.send('New rack for player ' + req.param('player') + 'now set' + req.param('rack'))
})
app.get('/getrack', (req, res) => {
  res.send(player_rack[req.param('player')])
})

app.get('/getturn', (req, res) => {
  res.send(String(turn));
})
app.get('/setturn', (req, res) => {
  turn = Number(req.param('turn'))
  res.send("Turn set")
})


app.get('/getdata', (req, res) => {
  res.send(board)
})

app.listen(port, () => {
  console.log(`Example app listening at http://localhost:${port}`)
})

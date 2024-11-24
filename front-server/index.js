const express = require("express");
const app = express();

var http = require("http");
const server = http.createServer(app);

app.use(express.static("dist"));

app.get("*", function (req, res) {
  res.sendFile(__dirname + "/dist/index.html");
});

server.listen(5500, "26.130.41.84");

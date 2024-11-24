const express = require("express");
const app = express();

//var https = require("https");
var http = require("http");

const server = http.createServer(app);

const { Server } = require("socket.io");
const io = new Server(server, {
  cors: {
    origin: "http://localhost:5173",
    methods: ["GET", "POST"],
  },
});
const { ExpressPeerServer } = require("peer");
const peerServer = ExpressPeerServer(server, {
  debug: true,
});
const peers = {};

app.use("/peerjs", peerServer);

io.on("connection", (socket) => {
  console.log(
    `New connection '${socket.id}' from '${socket.handshake.headers.referer}'`,
  );

  socket.on("join-room", (roomId, userId, userJson) => {
    if (roomId in peers) {
      peers[roomId] = peers[roomId].filter(
        (item) => item.userJson !== userJson,
      );
      peers[roomId].push({ userId: userId, userJson: userJson });
    } else {
      peers[roomId] = [{ userId: userId, userJson: userJson }];
    }

    socket.join(roomId);
    setTimeout(() => {
      socket.to(roomId).emit("user-connected", userId, userJson);
      for (let i in peers[roomId]) {
        if (peers[roomId][i].userId !== userId) {
          io.to(socket.id).emit(
            "user-connected",
            peers[roomId][i].userId,
            peers[roomId][i].userJson,
          );
        }
      }
    }, 1000);

    socket.on("disconnect", () => {
      console.log("User Disconnected");
      io.emit("user-disconnected", userId);
    });
  });
});

server.listen(3030);

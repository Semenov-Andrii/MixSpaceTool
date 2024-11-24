import { io } from "socket.io-client";
import Peer from "peerjs";
import { getFullUrl, VIDEO_SERVER } from "./data";

let myVideoStream = null;

const socket = io(getFullUrl());
const peer = new Peer(VIDEO_SERVER);

export const onAll = (newUser, newStream, disconnectUser, meetingId, userJson) => {
    peer.on("open", (id) => {
        newUser(id, userJson);
        socket.emit("join-room", meetingId, id, userJson);
    });

    socket.on("user-connected", (userId, userJson) => {
        newUser(userId, userJson);
        connectToNewUser(userId, myVideoStream, newStream);
    });
    socket.on("user-disconnected", (id) => {
        disconnectUser(id);
    });
};

export const getMediaStream = (newStream, videoOn, microOn) => {
    navigator.mediaDevices.getUserMedia({ audio: true, video: true }).then((stream) => {
        myVideoStream = stream;
        newStream(stream);

        const videoTrack = myVideoStream.getVideoTracks()[0];
        videoTrack.enabled = videoOn;

        const audioTrack = myVideoStream.getAudioTracks()[0];
        audioTrack.enabled = microOn;

        peer.on("call", (call) => {
            call.answer(stream);
            // call.on("stream", (userVideoStream) => {
            //     videos.value.push(userVideoStream);
            // });
        });
    });
};

const connectToNewUser = (userId, stream, newStream) => {
    const call = peer.call(userId, stream);
    call.on("stream", (userVideoStream) => {
        newStream(userId, userVideoStream);
    });
};

export const toggleMute = () => {
    const audioTrack = myVideoStream.getAudioTracks()[0];
    const isEnabled = audioTrack.enabled;

    audioTrack.enabled = !isEnabled;
};

export const toggleVideo = () => {
    const videoTrack = myVideoStream.getVideoTracks()[0];
    const isEnabled = videoTrack.enabled;

    videoTrack.enabled = !isEnabled;
};

export const disconnect = () => {
    peer.destroy();
    socket.disconnect();
    window.close();
};

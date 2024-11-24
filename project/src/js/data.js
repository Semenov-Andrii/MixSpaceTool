export const VIDEO_SERVER = {
    host: "127.0.0.1",
    port: 3030,
    path: "/peerjs",
    secure: false
};

export const getFullUrl = () => {
    let url = "http";
    if (VIDEO_SERVER.secure) url += "s";

    return `${url}://${VIDEO_SERVER.host}:${VIDEO_SERVER.port}`;
};

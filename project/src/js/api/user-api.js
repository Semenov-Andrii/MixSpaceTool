import { sendAsync } from "../request.js";
import { API } from "./api.js";

export const registerApi = (fullname, email, position, password, avatar) => {
    const request = {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            "fullname": fullname,
            "username": email,
            "position": position,
            "password": password,
            "avatar": avatar
        })
    };
    return sendAsync(API + "register/", request);
};

export const loginApi = (email, password) => {
    const request = {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            "username": email,
            "password": password
        })
    };
    return sendAsync(API + "login/", request);
};
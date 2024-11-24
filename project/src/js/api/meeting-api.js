import { sendAsync } from "../request.js";
import { API } from "./api.js";
import { getToken } from "../auth.js";

export const meetingCreateApi = (icon, title) => {
    const request = {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            Authorization: `Token ${getToken()}`
        },
        body: JSON.stringify({
            icon: icon,
            title: title
        })
    };
    return sendAsync(API + "meeting/", request);
};

export const meetingListApi = () => {
    const request = {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
            Authorization: `Token ${getToken()}`
        }
    };
    return sendAsync(API + "meetings/", request);
};

export const meetingSaveApi = (meeting_id) => {
    const request = {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            Authorization: `Token ${getToken()}`
        },
        body: JSON.stringify({
            id: meeting_id
        })
    };
    return sendAsync(API + "save/meeting/", request);
};

export const savedMeetingListApi = () => {
    const request = {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
            Authorization: `Token ${getToken()}`
        }
    };
    return sendAsync(API + "save/meetings/", request);
};

export const meetingInviteApi = (meeting_id, email) => {
    const request = {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            Authorization: `Token ${getToken()}`
        },
        body: JSON.stringify({
            id: meeting_id,
            email: email
        })
    };
    return sendAsync(API + "invite/meeting/", request);
};

export const meetingGetApi = (meeting_id) => {
    const request = {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
            Authorization: `Token ${getToken()}`
        }
    };
    return sendAsync(`${API}save/meeting/${meeting_id}`, request);
};
export const meetingUnsaveApi = (meeting_id) => {
    const request = {
        method: "DELETE",
        headers: {
            "Content-Type": "application/json",
            Authorization: `Token ${getToken()}`
        }
    };
    return sendAsync(`${API}save/meeting/${meeting_id}`, request);
};

export const meetingDeleteApi = (meeting_id) => {
    const request = {
        method: "DELETE",
        headers: {
            "Content-Type": "application/json",
            Authorization: `Token ${getToken()}`
        }
    };
    return sendAsync(`${API}meeting/${meeting_id}`, request);
};

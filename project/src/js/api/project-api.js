import { getToken } from "../auth";
import { sendAsync } from "../request";
import { API } from "./api";

export const projectCreateApi = (title, description, icon) => {
    const request = {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            Authorization: `Token ${getToken()}`
        },
        body: JSON.stringify({
            title: title,
            description: description,
            icon: icon
        })
    };
    return sendAsync(API + "project/", request);
};

export const taskListCreateApi = (projectId, title) => {
    const request = {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            Authorization: `Token ${getToken()}`
        },
        body: JSON.stringify({
            title: title
        })
    };
    return sendAsync(`${API}task-list/project/${projectId}`, request);
};

export const taskListRemoveApi = (taskListId) => {
    const request = {
        method: "DELETE",
        headers: {
            "Content-Type": "application/json",
            Authorization: `Token ${getToken()}`
        }
    };
    return sendAsync(`${API}task-list/${taskListId}`, request);
};

export const taskCreateApi = (taskListId, title, description, is_done, label, member) => {
    const request = {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            Authorization: `Token ${getToken()}`
        },
        body: JSON.stringify({
            title: title,
            description: description,
            is_done: is_done,
            label: label,
            member: member
        })
    };

    return sendAsync(`${API}task/project/${taskListId}`, request);
};

export const taskUpdateApi = (taskId, title, description, is_done, label, member) => {
    const request = {
        method: "PATCH",
        headers: {
            "Content-Type": "application/json",
            Authorization: `Token ${getToken()}`
        },
        body: JSON.stringify({
            title: title,
            description: description,
            is_done: is_done,
            label: label,
            member: member
        })
    };

    return sendAsync(`${API}task/${taskId}/`, request);
};

export const taskLabelsListApi = (projectId) => {
    const request = {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
            Authorization: `Token ${getToken()}`
        }
    };
    return sendAsync(`${API}task-label/${projectId}`, request);
};

export const taskRemoveApi = (taskId) => {
    const request = {
        method: "DELETE",
        headers: {
            "Content-Type": "application/json",
            Authorization: `Token ${getToken()}`
        }
    };
    return sendAsync(`${API}task/${taskId}`, request);
};

export const projectGetApi = (projectId) => {
    const request = {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
            Authorization: `Token ${getToken()}`
        }
    };
    return sendAsync(`${API}project/${projectId}`, request);
};
export const projectDeleteApi = (projectId) => {
    const request = {
        method: "DELETE",
        headers: {
            "Content-Type": "application/json",
            Authorization: `Token ${getToken()}`
        }
    };
    return sendAsync(`${API}project/${projectId}`, request);
};

export const ownProjectListApi = () => {
    const request = {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
            Authorization: `Token ${getToken()}`
        }
    };
    return sendAsync(API + "projects/", request);
};

export const projectListApi = () => {
    const request = {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
            Authorization: `Token ${getToken()}`
        }
    };
    return sendAsync(API + "member/projects/", request);
};

export const memberCreateApi = (projectId, email, memberType) => {
    const request = {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            Authorization: `Token ${getToken()}`
        },
        body: JSON.stringify({
            email: email,
            [`${memberType}Id`]: projectId
        })
    };
    return sendAsync(`${API}member/${memberType}/`, request);
};

export const memberListApi = (projectId, memberType) => {
    const request = {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
            Authorization: `Token ${getToken()}`
        }
    };
    return sendAsync(`${API}members/${memberType}/${projectId}`, request);
};
export const memberDeleteApi = (projectId, memberId, memberType) => {
    const request = {
        method: "DELETE",
        headers: {
            "Content-Type": "application/json",
            Authorization: `Token ${getToken()}`
        }
    };
    return sendAsync(`${API}member/${memberType}/${projectId}/${memberId}`, request);
};

export const timerCreateApi = (projectId) => {
    const request = {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            Authorization: `Token ${getToken()}`
        }
    };
    return sendAsync(`${API}project/timer/create/${projectId}`, request);
};

export const timerEndApi = (timerId) => {
    const request = {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
            Authorization: `Token ${getToken()}`
        }
    };
    return sendAsync(`${API}project/timer/end/${timerId}`, request);
};

export const timerCommentApi = (timerId, comment) => {
    const request = {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
            Authorization: `Token ${getToken()}`
        },
        body: JSON.stringify({ comment: comment })
    };
    return sendAsync(`${API}project/timer/comment/${timerId}`, request);
};

export const timerListApi = (projectID) => {
    const request = {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
            Authorization: `Token ${getToken()}`
        }
    };
    return sendAsync(`${API}project/timers/${projectID}`, request);
};

export const memberTimerListApi = (projectID) => {
    const request = {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
            Authorization: `Token ${getToken()}`
        }
    };
    return sendAsync(`${API}project/timers/member/${projectID}`, request);
};

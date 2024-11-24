import { getToken } from "@/js/auth.js";
import { sendAsync } from "@/js/request.js";
import { API } from "@/js/api/api.js";

export const repositoryCreateApi = (title, description, icon) => {
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
    return sendAsync(API + "repository/", request);
};

export const ownRepositoryListApi = () => {
    const request = {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
            Authorization: `Token ${getToken()}`
        }
    };
    return sendAsync(API + "repositories/", request);
};

export const repositoryListApi = () => {
    const request = {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
            Authorization: `Token ${getToken()}`
        }
    };
    return sendAsync(API + "member/repositories/", request);
};

export const repositoryGetApi = (repositoryId) => {
    const request = {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
            Authorization: `Token ${getToken()}`
        }
    };
    return sendAsync(`${API}repository/${repositoryId}`, request);
};

export const repositoryDeleteApi = (repositoryId) => {
    const request = {
        method: "DELETE",
        headers: {
            "Content-Type": "application/json",
            Authorization: `Token ${getToken()}`
        }
    };
    return sendAsync(`${API}repository/${repositoryId}`, request);
};

export const fileCreateApi = (repositoryId, filename, parentId, fileType) => {
    const request = {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            Authorization: `Token ${getToken()}`
        },
        body: JSON.stringify({
            name: filename,
            parent: parentId,
            repository: repositoryId,
            fileType: fileType
        })
    };

    return sendAsync(`${API}repository/file/new`, request);
};

export const fileUpdateApi = (fileId, content) => {
    const request = {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
            Authorization: `Token ${getToken()}`
        },
        body: JSON.stringify({
            content: content
        })
    };

    return sendAsync(`${API}repository/file/${fileId}`, request);
};

export const fileRenameApi = (fileId, filename) => {
    const request = {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
            Authorization: `Token ${getToken()}`
        },
        body: JSON.stringify({
            name: filename
        })
    };

    return sendAsync(`${API}repository/file/${fileId}`, request);
};

export const fileUploadApi = (repositoryId, parentId, name, file) => {
    const formData = new FormData();
    formData.append("repository", repositoryId);
    if (parentId) formData.append("parent", parentId);
    formData.append("name", name);
    formData.append("file", file);

    const request = {
        method: "POST",
        headers: {
            Authorization: `Token ${getToken()}`
        },
        body: formData
    };

    return sendAsync(`${API}repository/file/upload`, request);
};

export const getDownloadFileUrl = (fileId) => {
    return `${API}repository/file/download/${fileId}`;
};

export const downloadFileContent = (fileId) => {
    const request = {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
            Authorization: `Token ${getToken()}`
        }
    };

    return fetch(getDownloadFileUrl(fileId), request).then((res) => res.text());
};

export const fileDeleteApi = (fileId) => {
    const request = {
        method: "DELETE",
        headers: {
            "Content-Type": "application/json",
            Authorization: `Token ${getToken()}`
        }
    };

    return fetch(`${API}repository/file/delete/${fileId}`, request).then((res) => res.text());
};

export const commitCreateApi = (repositoryId, title) => {
    const request = {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            Authorization: `Token ${getToken()}`
        },
        body: JSON.stringify({ title: title })
    };

    return sendAsync(`${API}repository/commit/${repositoryId}`, request);
};

export const commitListApi = (repositoryId) => {
    const request = {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
            Authorization: `Token ${getToken()}`
        }
    };

    return sendAsync(`${API}repository/commits/${repositoryId}`, request);
};
export const commitGotoApi = (repositoryId, versionId) => {
    const request = {
        method: "DELETE",
        headers: {
            "Content-Type": "application/json",
            Authorization: `Token ${getToken()}`
        }
    };

    return sendAsync(`${API}repository/commit/goto/${versionId}/${repositoryId}`, request);
};

import i18n from "@/i18n";
import { loginApi, registerApi } from "./api/user-api";

const saveData = (data) => {
    localStorage.setItem("data", JSON.stringify(data));
};

export const getUser = () => {
    const data = localStorage.getItem("data");
    if (!data) return undefined;

    try {
        const user = JSON.parse(data);
        if (!("token" in user)) return undefined;

        return user;
    }
    catch (error) {
        console.log(error);

        return undefined;
    }
};

export const getToken = () => {
    const user = getUser();
    if (user) return user.token;

    return undefined
}

export const registerUser = (user) => {
    return registerApi(user.fullname, user.email, user.position, user.password, user.avatar)
        .then(res => {
            saveData(res);
            window.dispatchEvent(new CustomEvent("auth", { detail: res }));
            return res;
        });
};

export const loginUser = (email, password) => {
    return loginApi(email, password)
        .then(res => {
            saveData(res);
            window.dispatchEvent(new CustomEvent("auth", { detail: res }));
            return res;
        });
};

export const logoutUser = () => {
    localStorage.removeItem("data");
    document.location.reload();
};

export const ifAuthenticated = (to, from, next) => {
    const user = getUser();

    if (user) {
        next();
        return;
    }

    next({ name: "auth", params: { locale: i18n.getLocale() } });
};
import { getUser } from "@/js/auth.js";

export const errorToString = (err) => {
    if (typeof err === "string") {
        try {
            err = JSON.parse(err);
        } catch (err) {
            console.log(err);
        }
    }

    if (typeof err === "object" && "detail" in err) {
        const detail = err.detail;
        if (typeof detail === "string") return detail;

        let res = "";
        detail.forEach((error) => {
            res += error + " ";
        });

        return res;
    }

    return err;
};

export const truncateString = (str, maxLength, useEllipsis = false) => {
    if (str.length <= maxLength) {
        return str;
    }

    return useEllipsis && maxLength > 3
        ? str.slice(0, maxLength - 3) + "..."
        : str.slice(0, maxLength);
};

export const isOwner = (ownerId) => {
    const user = getUser();
    return user?.id === ownerId;
};

const invalidChars = /[<>:"/\\|?*+@]/g;

export const validateFilename = (name) => {
    return name.replace(invalidChars, "_");
};

export const getTimeDifference = (
    date1,
    date2,
    { day = "days", hour = "hours", minute = "minutes", second = "seconds" }
) => {
    if (!date1 || !date2) return "";

    const timeDifference = new Date(date2) - new Date(date1);

    const days = Math.floor(timeDifference / (1000 * 60 * 60 * 24));
    const hours = Math.floor((timeDifference / (1000 * 60 * 60)) % 24);
    const minutes = Math.floor((timeDifference / (1000 * 60)) % 60);
    const seconds = Math.floor((timeDifference / 1000) % 60);

    let result = [];
    if (days > 0) result.push(`${days} ${day}`);
    if (hours > 0) result.push(`${hours} ${hour}`);
    if (minutes > 0) result.push(`${minutes} ${minute}`);
    if (seconds > 0) result.push(`${seconds} ${second}`);

    return result.length > 0 ? result.join(", ") : "0 seconds";
};

import { programmingLanguages } from "@/js/languages.js";

export const detectLanguage = (filename) => {
    const extension = filename.split(".").pop().toLowerCase();

    return programmingLanguages[extension] || "text";
};

import { createI18n, useI18n } from 'vue-i18n';
import { en } from './en';
import { uk } from './uk';


const savedLocale = localStorage.getItem("locale");

export const defaultLocale = savedLocale ? savedLocale : "uk";

let _i18n;
let use;

const messages = {
    en: en,
    uk: uk
};

const setup = (options = { locale: defaultLocale }) => {

    _i18n = createI18n({

        locale: options.locale,
        fallbackLocale: defaultLocale,
        messages: messages,
        legacy: false,
    });

    setLocale(options.locale);

    return _i18n;
};


const setLocale = (newLocale) => {
    if (messages[newLocale]) {
        _i18n.global.locale.value = newLocale;
        localStorage.setItem("locale", newLocale);
    }

};
const getLocale = () => {
    return _i18n.global.locale.value;
};

const useT = () => {
    if (!use) use = useI18n();
};

const t = (key) => {
    useT();

    return use.t(key);
};

export default {

    get vueI18n() {
        return _i18n
    },
    setup,
    setLocale,
    getLocale,
    t,
    useT
};

export const supportedLocales = {
    "en": { name: "English", flag: "flag-icon-gb" },
    "uk": { name: "Українська", flag: "flag-icon-ua" }
};
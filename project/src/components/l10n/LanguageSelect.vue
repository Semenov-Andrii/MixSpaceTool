<script setup>
import { ref } from "vue";
import i18n, { supportedLocales } from "@/i18n";
import { useRoute } from "vue-router";
import router from "@/router";


const locales = ref(supportedLocales);
const locale = ref(supportedLocales[i18n.getLocale()]);
const onUpdated = ref(i18n.vueI18n);

const route = useRoute();

const onLanguageChanged = (language) => {
    if (language === i18n.getLocale()) return;
    const path = route.path.replace(`/${i18n.getLocale()}`, `/${language}`);
    i18n.setLocale(language);

    router.push(path);
};
const updateLocale = () => {
    locale.value = supportedLocales[i18n.getLocale()];
};

</script>
<template>
    <div class="dropdown">
        <a class="btn dropdown-toggle" href="#" role="button" id="dropdownMenuLink2" style="border:none;"
            data-bs-toggle="dropdown" aria-expanded="false">
            <i :class="`${locale.flag} flag-icon m-0`" v-bind="updateLocale(onUpdated)"></i>
        </a>

        <ul class="dropdown-menu" aria-labelledby="dropdownMenuLink2" style="background-color: white;">
            <li>
                <a class="dropdown-item" href="#"><i :class="`${locale.flag} flag-icon`"></i> {{ locale.name
                    }}
                    <i class="fa fa-check text-success ms-2"></i></a>
            </li>
            <li>
                <hr class="dropdown-divider" />
            </li>
            <li v-for="(data, index) in locales" :key="index" @click="onLanguageChanged(index)">
                <a class="dropdown-item" href="#"><i :class="`${data.flag} flag-icon`"></i>
                    {{ data.name }}</a>
            </li>
        </ul>
    </div>
</template>
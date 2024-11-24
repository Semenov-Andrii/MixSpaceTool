<script setup>
import i18n from "@/i18n";
import { useRouter } from "vue-router";
import CreateForm from "@/components/CreateForm.vue";
import { repositoryCreateApi } from "@/js/api/repository-api.js";

const router = useRouter();

const createFunc = (title, description, icon) => {
    return repositoryCreateApi(title, description, icon).then((res) => {
        router.push({
            name: "repository",
            params: { locale: i18n.getLocale(), repositoryId: res.id }
        });
    });
};
</script>
<template>
    <CreateForm
        :create-func="createFunc"
        :def-title="$t('repository')"
        :name="$t('repositoryCreateLabel')"
    ></CreateForm>
</template>

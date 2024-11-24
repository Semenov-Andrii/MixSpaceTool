<script setup>
import i18n from "@/i18n";
import { useRouter } from "vue-router";
import { projectCreateApi } from "@/js/api/project-api";
import CreateForm from "@/components/CreateForm.vue";

const router = useRouter();

const createFunc = (title, description, icon) => {
    return projectCreateApi(title, description, icon).then((res) => {
        router.push({
            name: "project",
            params: { locale: i18n.getLocale(), projectId: res.id }
        });
    });
};
</script>
<template>
    <CreateForm
        :create-func="createFunc"
        :def-title="$t('project')"
        :name="$t('projectCreateLabel')"
    ></CreateForm>
</template>

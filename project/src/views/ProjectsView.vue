<script setup>
import { ref } from "vue";
import { ownProjectListApi, projectListApi } from "@/js/api/project-api";
import ProjectList from "@/components/project/ProjectList.vue";

const ownProjects = ref([]);

ownProjectListApi().then((res) => {
    ownProjects.value.push(...res);
});

const projects = ref([]);

projectListApi().then((res) => {
    projects.value.push(...res);
});
</script>
<template>
    <div>
        <div class="header-row m-4 ms-0 mb-0">
            <h3 class="fw-bold mb-3">{{ $t("ownProjects") }}</h3>
            <RouterLink
                class="btn btn-icon btn-round btn-info"
                :to="{ name: 'new-project' }"
                :title="$t('addProjectTitle')"
            >
                <i class="fa-solid fa-plus"></i>
            </RouterLink>
        </div>
        <div class="row">
            <ProjectList :projects="ownProjects"></ProjectList>
        </div>
        <div class="row">
            <h3 class="fw-bold mb-3 mt-3">{{ $t("projects") }}</h3>
        </div>
        <div class="row">
            <ProjectList :projects="projects"></ProjectList>
        </div>
    </div>
</template>

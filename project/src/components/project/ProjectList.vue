<script setup>
import ProjectItem from "./ProjectItem.vue";

defineProps({
    projects: {
        type: Array,
        required: true
    }
});
</script>
<template>
    <div v-if="projects.length !== 0">
        <ProjectItem
            v-for="project in projects"
            :key="project.id"
            :id="project.id"
            :owner-name="project.owner.fullname"
            :title="project.title"
            :icon="project.icon"
        ></ProjectItem>
    </div>
    <div v-else>
        <div class="col-12">{{ $t("missing") }}</div>
    </div>
</template>

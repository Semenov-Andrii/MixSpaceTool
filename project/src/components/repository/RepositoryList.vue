<script setup>
import RepositoryItem from "@/components/repository/RepositoryItem.vue";

defineProps({
    repos: {
        type: Array,
        required: true
    }
});
</script>
<template>
    <div v-if="repos.length !== 0">
        <RepositoryItem
            v-for="repo in repos"
            :key="repo.id"
            :id="repo.id"
            :owner-name="repo.owner.fullname"
            :title="repo.title"
            :icon="repo.icon"
        ></RepositoryItem>
    </div>
    <div v-else>
        <div class="col-12">{{ $t("missing") }}</div>
    </div>
</template>

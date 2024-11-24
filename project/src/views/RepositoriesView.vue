<script setup>
import { ref } from "vue";
import { ownRepositoryListApi, repositoryListApi } from "@/js/api/repository-api.js";
import RepositoryList from "@/components/repository/RepositoryList.vue";

const ownRepos = ref([]),
    repos = ref([]);

ownRepositoryListApi().then((res) => ownRepos.value.push(...res));
repositoryListApi().then((res) => repos.value.push(...res));
</script>
<template>
    <div>
        <div class="header-row m-4 ms-0 mb-0">
            <h3 class="fw-bold mb-3">{{ $t("ownRepositories") }}</h3>
            <RouterLink
                class="btn btn-icon btn-round btn-warning"
                :to="{ name: 'new-repository' }"
                :title="$t('addRepositoryTitle')"
            >
                <i class="fa-solid fa-plus"></i>
            </RouterLink>
        </div>
        <div class="row">
            <RepositoryList :repos="ownRepos"></RepositoryList>
        </div>
        <div class="row">
            <h3 class="fw-bold mb-3 mt-3">{{ $t("repositories") }}</h3>
        </div>
        <div class="row">
            <RepositoryList :repos="repos"></RepositoryList>
        </div>
    </div>
</template>

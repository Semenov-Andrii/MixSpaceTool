<script setup>
defineProps({
    id: {
        type: String,
        required: true
    },
    title: {
        type: String,
        required: true
    },
    icon: {
        type: String,
        required: true
    },
    ownerName: {
        type: String,
        required: true
    }
});
</script>

<template>
    <div class="col-12 col-md-6 col-xl-4">
        <div class="card list-item">
            <div class="card-header header-row">
                <div>
                    <div class="card-title"><i :class="icon"></i> {{ title }}</div>
                    <div class="card-category">{{ ownerName }}</div>
                </div>

                <RouterLink
                    class="btn btn-icon btn-round btn-warning"
                    :to="{ name: 'repository', params: { repositoryId: id } }"
                    :title="$t('goRepositoryTitle')"
                >
                    <i class="fa-solid fa-angles-right"></i>
                </RouterLink>
            </div>
        </div>
    </div>
</template>
<style>
.list-item {
    flex: 1;
}
</style>

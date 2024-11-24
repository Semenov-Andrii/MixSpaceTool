<script setup>
import CommitItem from "@/components/repository/CommitItem.vue";
import { computed } from "vue";

const props = defineProps({
    commits: {
        type: Array,
        required: true
    },
    owner: {
        type: Object
    },
    goTo: {
        type: Function,
        required: true
    }
});

const commits = computed(() => props.commits);
const model = defineModel({ default: false });
</script>

<template>
    <div v-if="model" class="member-window">
        <div class="row">
            <div class="col-0 col-md-4"></div>
            <div class="col-12 col-md-4">
                <div class="member-list">
                    <div class="header-row">
                        <h4>{{ $t("commits") }}</h4>
                        <div>
                            <button type="button" class="btn-none list-color">
                                <i class="fa-solid fa-xmark" @click="model = false"></i>
                            </button>
                        </div>
                    </div>

                    <div class="members" id="style-3">
                        <CommitItem
                            v-for="commit in commits"
                            :key="commit.id"
                            :id="commit.id"
                            :title="commit.title"
                            :created="commit.created"
                            :go-to="
                                () => {
                                    model = false;
                                    goTo(commit.id);
                                }
                            "
                            :owner-id="owner?.id"
                            :member="commit.member"
                        />
                    </div>
                </div>
            </div>
            <div class="col-0 col-md-4"></div>
        </div>
    </div>
</template>

<style scoped></style>

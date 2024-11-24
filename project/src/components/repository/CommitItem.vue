<script setup>
import QuestionWindow from "@/components/modal/QuestionWindow.vue";
import { ref } from "vue";
import { isOwner } from "@/js/utility.js";
import DotsButton from "@/components/DotsButton.vue";
import { IMAGES } from "@/js/resources.js";

defineProps({
    id: {
        type: Number,
        required: true
    },
    title: {
        type: String,
        required: true
    },
    created: {
        type: String,
        required: true
    },
    goTo: {
        type: Function,
        required: true
    },
    ownerId: {
        type: String,
        required: true
    },
    member: {
        type: Object,
        required: true
    }
});

const active = ref(false);
</script>

<template>
    <QuestionWindow
        :title="$t('goToTitle')"
        :success="goTo"
        :message="$t('goToMsg')"
        v-model="active"
    ></QuestionWindow>
    <div class="card list-color mt-2">
        <div class="card-body">
            <div class="header-row">
                <h4>
                    {{ title }}
                </h4>
                <div v-if="isOwner(ownerId)">
                    <DotsButton>
                        <template v-slot:list>
                            <a class="dropdown-item" href="#" @click="active = true">
                                {{ $t("goTo") }}
                            </a>
                        </template>
                    </DotsButton>
                </div>
            </div>

            <p>{{ new Date(created).toLocaleString() }}</p>
        </div>
        <div class="card-footer">
            <h4>
                <img
                    :src="IMAGES[member.avatar]"
                    alt="image profile"
                    class="avatar-img rounded-circle"
                />{{ member.fullname }} - {{ member.position }}
            </h4>
        </div>
    </div>
</template>
<style scoped>
.card {
    margin-bottom: 1px;
}

.card-body > p {
    font-size: 1em;
    margin-bottom: 1px;
}

.card-body {
    padding: 10px;
}
.avatar-img {
    width: 35px;
    height: 35px;
    padding-right: 2px;
}
</style>

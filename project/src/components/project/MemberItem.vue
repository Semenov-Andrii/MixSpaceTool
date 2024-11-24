<script setup>
import { IMAGES } from "@/js/resources.js";
import QuestionWindow from "@/components/modal/QuestionWindow.vue";
import { ref } from "vue";
import { isOwner } from "@/js/utility.js";
import DotsButton from "@/components/DotsButton.vue";

defineProps({
    id: {
        type: String,
        required: true
    },
    fullname: {
        type: String,
        required: true
    },
    email: {
        type: String,
        required: true
    },
    position: {
        type: String,
        required: true
    },
    avatar: {
        type: String,
        required: true
    },
    removeMember: {
        type: Function,
        required: true
    },
    ownerId: {
        type: String,
        required: true
    }
});

const active = ref(false);

const onRemoveMember = () => {
    active.value = true;
};
</script>

<template>
    <QuestionWindow
        :title="$t('removeMember')"
        :success="() => removeMember(id)"
        :message="$t('removeMemberMsg')"
        v-model="active"
    ></QuestionWindow>
    <div class="card" :class="(ownerId === id ? 'bg-info text-dark' : '') + 'mt-2'">
        <div class="card-body">
            <div class="header-row">
                <h4>
                    <img
                        :src="IMAGES[avatar]"
                        alt="image profile"
                        class="avatar-img rounded-circle"
                    />{{ fullname }} - {{ position }}
                </h4>
                <DotsButton v-if="ownerId !== id && isOwner(ownerId)">
                    <template v-slot:list>
                        <a class="dropdown-item" href="#" @click="onRemoveMember">
                            {{ $t("removeMember") }}
                        </a>
                    </template>
                </DotsButton>
            </div>

            <p>{{ email }}</p>
        </div>
    </div>
</template>
<style scoped>
.avatar-img {
    width: 35px;
    height: 35px;
    padding-right: 2px;
}

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
</style>

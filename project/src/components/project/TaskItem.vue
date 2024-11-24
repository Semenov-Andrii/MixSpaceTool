<script setup>
import { IMAGES } from "@/js/resources.js";
import { truncateString } from "@/js/utility.js";
import QuestionWindow from "@/components/modal/QuestionWindow.vue";
import { ref } from "vue";
import TaskForm from "@/components/project/TaskForm.vue";
import DotsButton from "@/components/DotsButton.vue";

defineProps({
    id: {
        type: Number,
        required: true
    },
    title: {
        type: String,
        required: true
    },
    description: {
        type: String,
        required: true
    },
    isDone: {
        type: Boolean,
        required: true
    },
    member: {
        type: Object,
        default: null
    },
    label: {
        type: Object,
        default: null
    },
    removeTask: {
        type: Function,
        required: true
    },
    updateTask: {
        type: Function,
        required: true
    }
});

const active = ref(false);

const onRemoveTask = () => {
    active.value = true;
};
</script>

<template>
    <QuestionWindow
        :title="$t('removeTask')"
        :success="() => removeTask(id)"
        :message="$t('removeTaskMsg')"
        v-model="active"
    ></QuestionWindow>
    <div class="card" :style="isDone ? 'background-color:#b1ff9e' : ''">
        <div class="card-body">
            <span v-if="label" class="label-text" :style="`color: ${label.color};`">
                {{ label.text }}
            </span>
            <div class="header-row">
                <h5>
                    {{ title }}
                </h5>
                <DotsButton>
                    <template v-slot:list>
                        <a class="dropdown-item" href="#" @click="() => updateTask(id)">
                            {{ $t("updateTask") }}
                        </a>
                        <a class="dropdown-item" href="#" @click="onRemoveTask">
                            {{ $t("removeTask") }}
                        </a>
                    </template>
                </DotsButton>
            </div>

            <p>{{ truncateString(description, 20, true) }}</p>
            <div v-if="member" class="card-member">
                <img
                    :src="IMAGES[member.avatar]"
                    alt="image profile"
                    class="avatar-img rounded-circle"
                />{{ member.fullname }}
            </div>
        </div>
    </div>
</template>
<style scoped>
.avatar-img {
    width: 25px;
    height: 25px;
    padding-right: 2px;
}

.card {
    margin-bottom: 1px;
    z-index: 1;
}

.card > * {
    z-index: 1;
}

.label-text {
    font-size: 0.8em;
}

.card-body > p {
    font-size: 1em;
    margin-bottom: 1px;
}

.card-body {
    padding: 10px;
}

.card-member {
    display: flex;
    justify-content: end;
    width: 100%;
}
</style>

<script setup>
import TaskItem from "@/components/project/TaskItem.vue";
import TaskForm from "@/components/project/TaskForm.vue";
import { ref } from "vue";
import { taskRemoveApi } from "@/js/api/project-api.js";
import NotifyBox from "@/components/modal/NotifyBox.vue";
import LoadingWindow from "@/components/modal/LoadingWindow.vue";
import i18n from "@/i18n/index.js";
import { errorToString } from "@/js/utility.js";
import QuestionWindow from "@/components/modal/QuestionWindow.vue";
import DotsButton from "@/components/DotsButton.vue";

const props = defineProps({
    projectId: {
        type: String,
        required: true
    },
    taskListId: {
        type: Number,
        required: true
    },
    title: {
        type: String,
        required: true
    },
    tasks: {
        type: Array,
        required: true
    },
    removeList: {
        type: Function,
        required: true
    },
    labelList: {
        type: Array,
        required: true
    },
    addLabel: {
        type: Function,
        required: true
    }
});

const activeLoading = ref(false);

const error = ref({
    active: false,
    title: "",
    message: ""
});

i18n.useT();

const tasks = ref(props.tasks);

const active = ref(false);

const removeActive = ref(false);
const initTask = ref(null);

const addTask = () => {
    active.value = true;
    initTask.value = null;
};
const removeTask = (id) => {
    taskRemoveApi(id)
        .then(() => {
            tasks.value = tasks.value.filter((item) => item.id !== id);
        })
        .catch((err) => {
            console.log(err);
            error.value.title = i18n.t("registerError");
            error.value.message = errorToString(err);
            error.value.active = true;
        });
};

const onTaskCreated = (res) => {
    const itemIndex = tasks.value.findIndex((item) => item.id === res.id);
    if (itemIndex >= 0 && itemIndex < tasks.value.length) {
        tasks.value[itemIndex] = res;
    } else {
        tasks.value.push(res);
    }

    active.value = false;
};

const onRemoveList = () => {
    removeActive.value = true;
};

const updateTask = (id) => {
    const task = tasks.value.find((item) => item.id === id);
    if (task) {
        active.value = true;
        initTask.value = task;
    }
};
</script>

<template>
    <QuestionWindow
        :title="$t('removeList')"
        :success="() => removeList(taskListId)"
        :message="$t('removeListMsg')"
        v-model="removeActive"
    ></QuestionWindow>
    <NotifyBox
        v-model="error.active"
        :message="error.message"
        :title="error.title"
        type="danger"
    ></NotifyBox>
    <LoadingWindow v-if="activeLoading"></LoadingWindow>
    <TaskForm
        v-model="active"
        :project-id="projectId"
        :on-success="onTaskCreated"
        :task-list-id="taskListId"
        :label-list="labelList"
        :add-label="addLabel"
        :init="initTask"
    ></TaskForm>
    <div class="col-12 col-md-4 mb-4">
        <div class="task-list">
            <div class="header-row">
                <h4>{{ title }}</h4>
                <DotsButton>
                    <template v-slot:list>
                        <a class="dropdown-item" href="#" @click="addTask">
                            {{ $t("addTask") }}
                        </a>
                        <a class="dropdown-item" href="#" @click="onRemoveList">
                            {{ $t("removeList") }}
                        </a>
                    </template>
                </DotsButton>
            </div>

            <div class="tasks" id="style-3">
                <TaskItem
                    v-for="task in tasks"
                    :key="task"
                    :id="task.id"
                    :title="task.title"
                    :is-done="task.isDone"
                    :description="task.description"
                    :member="task.member"
                    :label="task.label"
                    :remove-task="removeTask"
                    :update-task="updateTask"
                ></TaskItem>
            </div>
        </div>
    </div>
</template>
<style scoped>
.task-list {
    display: flex;
    flex-direction: column;

    border: #0a0b11 1px solid;
    padding: 15px;
    border-radius: 10px;
    background-color: #eaecee;
}

.tasks {
    max-height: 70vh;
    overflow-y: auto;
}

#style-3::-webkit-scrollbar-track {
    -webkit-box-shadow: inset 0 0 6px rgba(0, 0, 0, 0.3);
    background-color: #f5f5f5;
}

#style-3::-webkit-scrollbar {
    width: 6px;
    background-color: #f5f5f5;
}

#style-3::-webkit-scrollbar-thumb {
    background-color: gray;
}
</style>

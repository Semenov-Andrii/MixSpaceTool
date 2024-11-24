<script setup>
import {
    memberTimerListApi,
    projectDeleteApi,
    projectGetApi,
    taskLabelsListApi,
    taskListRemoveApi,
    timerListApi
} from "@/js/api/project-api";
import { ref, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import NotifyBox from "@/components/modal/NotifyBox.vue";
import LoadingWindow from "@/components/modal/LoadingWindow.vue";
import i18n from "@/i18n/index.js";
import { errorToString, isOwner } from "@/js/utility.js";
import TaskList from "@/components/project/TaskList.vue";
import TaskListForm from "@/components/project/TaskListForm.vue";
import QuestionWindow from "@/components/modal/QuestionWindow.vue";
import MemberList from "@/components/project/MemberList.vue";
import DotsButton from "@/components/DotsButton.vue";
import { eventBusTimer } from "@/js/event-bus.js";
import TimerList from "@/components/project/TimerList.vue";

const { projectId } = useRoute().params;

const router = useRouter();

const project = ref(null);

const active = ref(true);

const error = ref({
    active: false,
    title: "",
    message: ""
});

i18n.useT();

const timers = ref([]);

const updateTimers = (res) => {
    let api = memberTimerListApi;
    if (isOwner(res.owner.id)) {
        api = timerListApi;
    }

    return api(res.id).then((tms) => {
        timers.value = tms;
    });
};

const refreshTimers = () => {
    if (!project.value) return;
    updateTimers(project.value);
};

watch(() => eventBusTimer.actionId, refreshTimers);

projectGetApi(projectId)
    .then((res) => {
        project.value = res;
        return updateTimers(res);
    })
    .catch((err) => {
        console.log(err);
        error.value.title = i18n.t("projectError");
        error.value.message = errorToString(err);
        error.value.active = true;
    })
    .finally(() => {
        active.value = false;
    });

const formActive = ref(false);
const addTaskList = () => {
    formActive.value = true;
};

const onTaskListCreated = (res) => {
    formActive.value = false;
    project.value?.taskLists?.push(res);
};

const removeList = (id) => {
    taskListRemoveApi(id)
        .then(() => {
            project.value.taskLists = project.value.taskLists?.filter((item) => item.id !== id);
        })
        .catch((err) => {
            console.log(err);
            error.value.title = i18n.t("removeError");
            error.value.message = errorToString(err);
            error.value.active = true;
        });
};

const labelList = ref([]);

taskLabelsListApi(projectId).then((res) => {
    labelList.value = res;
});

const addLabel = (label) => {
    const item = labelList.value.find((item) => item.text === label.text);
    if (!item) {
        labelList.value = [...labelList.value, label];
    }
};

const removeActive = ref(false);

const removeProject = () => {
    removeActive.value = true;
};

const onRemoveProject = () => {
    projectDeleteApi(projectId)
        .then(() => {
            router.push({ name: "projects", params: { locale: i18n.getLocale() } });
        })
        .catch((err) => {
            console.log(err);
            error.value.title = i18n.t("removeError");
            error.value.message = errorToString(err);
            error.value.active = true;
        });
};

const memberActive = ref(false);

const showMembers = () => {
    memberActive.value = true;
};

const timerActive = ref(false);
</script>
<template>
    <MemberList
        :item-id="projectId"
        v-model="memberActive"
        :owner="project?.owner"
        member-type="project"
    ></MemberList>

    <TimerList :timers="timers" v-model="timerActive" :refresh="refreshTimers" />

    <NotifyBox
        v-model="error.active"
        :message="error.message"
        :title="error.title"
        type="danger"
    ></NotifyBox>
    <QuestionWindow
        :title="$t('removeProject')"
        :success="onRemoveProject"
        :message="$t('removeProjectMsg')"
        v-model="removeActive"
    ></QuestionWindow>
    <LoadingWindow v-if="active"></LoadingWindow>
    <TaskListForm
        :on-success="onTaskListCreated"
        :project-id="projectId"
        v-model="formActive"
    ></TaskListForm>
    <div>
        <div class="m-4">
            <div class="header-row">
                <h3 class="fw-bold mb-3"><i :class="project?.icon"></i> {{ project?.title }}</h3>
                <DotsButton>
                    <template v-slot:list>
                        <a class="dropdown-item" href="#" @click="addTaskList">
                            {{ $t("addTaskList") }}
                        </a>
                        <a class="dropdown-item" href="#" @click="showMembers">
                            {{ $t("members") }}
                        </a>
                        <a
                            class="dropdown-item"
                            href="#"
                            @click="() => eventBusTimer.open(project)"
                        >
                            {{ $t("timer") }}
                        </a>
                        <a class="dropdown-item" href="#" @click="timerActive = true">
                            {{ $t("timers") }}
                        </a>
                        <a
                            v-if="isOwner(project?.owner?.id)"
                            class="dropdown-item"
                            href="#"
                            @click="removeProject"
                        >
                            {{ $t("removeProject") }}
                        </a>
                    </template>
                </DotsButton>
            </div>
            <p>{{ project?.description }}</p>
        </div>
        <div class="row">
            <TaskList
                v-for="list in project?.taskLists"
                :key="list"
                :project-id="projectId"
                :task-list-id="list.id"
                :tasks="list.tasks"
                :title="list.title"
                :remove-list="removeList"
                :label-list="labelList"
                :add-label="addLabel"
            ></TaskList>
        </div>
    </div>
</template>

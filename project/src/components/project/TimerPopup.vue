<script setup>
import PopupWindow from "@/components/modal/PopupWindow.vue";
import { computed, ref, watch } from "vue";
import { eventBusTimer } from "@/js/event-bus.js";
import { timerCommentApi, timerCreateApi, timerEndApi } from "@/js/api/project-api.js";
import InputWindow from "@/components/modal/InputWindow.vue";

const project = computed(() => eventBusTimer.project);
const timer = ref(null);
const visible = computed(() => eventBusTimer.bus.popupVisible);

let interval = null;

const time = ref("00:00:00");

const countTime = () => {
    if (!timer.value) return;

    const now = new Date();

    const startTime = new Date(timer.value.startTime);
    const differenceInMilliseconds = now - startTime;

    const totalSeconds = Math.floor(differenceInMilliseconds / 1000);
    const hours = Math.floor(totalSeconds / 3600);
    const minutes = Math.floor((totalSeconds % 3600) / 60);
    const seconds = totalSeconds % 60;

    time.value = `${String(hours).padStart(2, "0")}:${String(minutes).padStart(2, "0")}:${String(seconds).padStart(2, "0")}`;
};

const jsonTimer = localStorage.getItem("timer");
const jsonProject = localStorage.getItem("project");
if (jsonTimer && jsonProject) {
    try {
        timer.value = JSON.parse(jsonTimer);
        const pr = JSON.parse(jsonProject);
        eventBusTimer.open(pr);
        interval = setInterval(countTime, 1000);
    } catch (e) {
        localStorage.removeItem("timer");
        localStorage.removeItem("project");
    }
}

const start = () => {
    if (timer.value) {
        return;
    }
    time.value = "00:00:00";

    timerCreateApi(project.value.id)
        .then((res) => {
            timer.value = res;
            interval = setInterval(countTime, 1000);
            eventBusTimer.update();

            localStorage.setItem("timer", JSON.stringify(timer.value));
            localStorage.setItem("project", JSON.stringify(project.value));
        })
        .catch((err) => {
            console.log(err);
        });
};

const inputActive = ref(false);

const stop = (text = true) => {
    if (interval) {
        clearInterval(interval);
        interval = null;
    }

    if (timer.value) {
        timerEndApi(timer.value.id, "")
            .then(() => {
                localStorage.removeItem("timer");
                localStorage.removeItem("project");

                if (text) inputActive.value = true;
                else {
                    timer.value = null;
                    eventBusTimer.update();
                }
            })
            .catch((err) => {
                console.log(err);
            });
    }
};

watch(
    () => eventBusTimer.project,
    (new_, old_) => {
        if (!old_ || new_ === old_ || !timer.value) return;

        stop(false);
    }
);

watch(visible, () => {
    if (!visible.value) {
        stop();
    }
});

const inputSuccess = (text) => {
    timerCommentApi(timer.value.id, text)
        .then(() => {
            timer.value = null;
            eventBusTimer.update();
        })
        .catch((err) => {
            console.log(err);
        });
};

const inputCancel = () => {
    timer.value = null;
    eventBusTimer.update();
};
</script>

<template>
    <InputWindow
        :title="$t('timerComment')"
        :success="inputSuccess"
        :cancel="inputCancel"
        :message="$t('timerMsg')"
        v-model="inputActive"
    />

    <PopupWindow v-model="eventBusTimer.bus" v-if="!inputActive">
        <template v-slot:header> <i :class="project?.icon"></i> {{ project.title }} </template>
        <template v-slot:content>
            <div class="header-row">
                <div>
                    <i
                        v-if="!timer"
                        class="fa-solid fa-play ms-2 text-success dots-btn"
                        @click="start"
                    ></i>
                    <i v-else class="fa-solid ms-2 fa-stop text-danger dots-btn" @click="stop"></i>
                </div>
                <div :class="timer === null ? 'text-danger' : ''">{{ time }}</div>
            </div>
        </template>
    </PopupWindow>
</template>

<style scoped></style>

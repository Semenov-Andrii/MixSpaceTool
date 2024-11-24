<script setup>
import { ref } from "vue";

import { meetingGetApi, meetingSaveApi, meetingUnsaveApi } from "@/js/api/meeting-api";
import i18n from "@/i18n";
import { errorToString } from "@/js/utility.js";
import NotifyBox from "@/components/modal/NotifyBox.vue";

const props = defineProps({
    meetingId: {
        type: String,
        required: true
    }
});

const meetingId = props.meetingId;

const saved = ref(false);

meetingGetApi(meetingId)
    .then(() => {
        saved.value = true;
    })
    .catch(() => {
        saved.value = false;
    });

const error = ref({
    active: false,
    title: "",
    message: ""
});

const saveMeeting = () => {
    let api = meetingSaveApi;

    if (saved.value) {
        api = meetingUnsaveApi;
    }

    api(meetingId)
        .then(() => {
            saved.value = !saved.value;
        })
        .catch((err) => {
            console.log(err);
            error.value.title = i18n.t("saveMeetingError");
            error.value.message = errorToString(err);
            error.value.active = true;
        });
};
</script>

<template>
    <NotifyBox
        :title="error.title"
        :message="error.message"
        type="danger"
        v-model="error.active"
    ></NotifyBox>
    <button class="icon-btn" @click="saveMeeting">
        <i :class="saved ? 'fa-solid fa-star text-warning' : 'fa-regular fa-star'"></i>
    </button>
</template>

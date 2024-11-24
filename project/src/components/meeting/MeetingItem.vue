<script setup>
import SaveIcon from "@/components/SaveIcon.vue";
import QuestionWindow from "@/components/modal/QuestionWindow.vue";
import { ref } from "vue";
import DotsButton from "@/components/DotsButton.vue";
import InputWindow from "@/components/modal/InputWindow.vue";
import { meetingInviteApi } from "@/js/api/meeting-api.js";
import NotifyBox from "@/components/modal/NotifyBox.vue";
import i18n from "@/i18n/index.js";
import { errorToString } from "@/js/utility.js";

const props = defineProps({
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
    },
    removeSelf: {
        type: Function,
        required: false,
        default: null
    }
});

const questionActive = ref(false);
const inputActive = ref(false);

const notify = ref({
    active: false,
    msg: "",
    title: "",
    type: "success"
});

i18n.useT();

const invite = (email) => {
    meetingInviteApi(props.id, email)
        .then(() => {
            notify.value.msg = i18n.t("addedMsg");
            notify.value.title = i18n.t("addedTitle");
            notify.value.type = "success";
            notify.value.active = true;
        })
        .catch((err) => {
            notify.value.msg = errorToString(err);
            notify.value.title = i18n.t("failedTitle");
            notify.value.type = "danger";
            notify.value.active = true;
        });
};
</script>

<template>
    <NotifyBox
        :title="notify.title"
        :type="notify.type"
        :message="notify.msg"
        v-model="notify.active"
    />
    <QuestionWindow
        :title="$t('removeMeeting')"
        :success="removeSelf"
        :message="$t('removeMeetingMsg')"
        v-model="questionActive"
    />
    <InputWindow
        :title="$t('inviteMember')"
        :success="invite"
        :message="$t('inviteMsg')"
        v-model="inputActive"
    />
    <div class="col-12 col-md-6 col-xl-4">
        <div class="card list-item">
            <div class="card-header header-row">
                <div>
                    <div class="card-title">
                        <i :class="icon"></i> {{ title }}
                        <DotsButton v-if="removeSelf">
                            <template v-slot:list>
                                <a class="dropdown-item" href="#" @click="questionActive = true">
                                    {{ $t("removeMeeting") }}
                                </a>
                                <a class="dropdown-item" href="#" @click="inputActive = true">
                                    {{ $t("inviteMember") }}
                                </a>
                            </template>
                        </DotsButton>
                    </div>
                    <div class="card-category">{{ ownerName }}</div>
                </div>
                <div class="header-row">
                    <div class="card-title">
                        <SaveIcon :meeting-id="id"></SaveIcon>
                    </div>

                    <RouterLink
                        class="btn btn-icon btn-round btn-success"
                        :to="{ name: 'meeting', params: { meetingId: id } }"
                        :title="$t('goMeetTitle')"
                        target="_blank"
                    >
                        <i class="fa-solid fa-angles-right"></i>
                    </RouterLink>
                </div>
            </div>
        </div>
    </div>
</template>
<style>
.list-item {
    flex: 1;
}
</style>

<script setup>
import { ref } from "vue";
import LoadingWindow from "@/components/modal/LoadingWindow.vue";
import NotifyBox from "@/components/modal/NotifyBox.vue";
import i18n from "@/i18n";
import { errorToString } from "@/js/utility";
import { useRouter } from "vue-router";
import { meetingCreateApi } from "@/js/api/meeting-api";
import { ICONS } from "@/js/resources";
import IconSelector from "@/components/IconSelector.vue";

const router = useRouter();
i18n.useT();

const createData = ref({
    icon: ICONS[0],
    title: i18n.t("meeting")
});
const active = ref(false);

const error = ref({
    active: false,
    title: "",
    message: ""
});

const onCreate = () => {
    active.value = true;

    meetingCreateApi(createData.value.icon, createData.value.title)
        .then((res) => {
            const url = router.resolve({
                name: "meeting",
                params: { locale: i18n.getLocale(), meetingId: res.id }
            }).href;
            window.open(url, "_blank");

            router.push({ name: "home" });
        })
        .catch((err) => {
            console.log(err);
            error.value.title = i18n.t("createMeetingError");
            error.value.message = errorToString(err);
            error.value.active = true;
        })
        .finally(() => {
            active.value = false;
        });
};
</script>
<template>
    <LoadingWindow v-if="active"></LoadingWindow>
    <NotifyBox
        :title="error.title"
        :message="error.message"
        type="danger"
        v-model="error.active"
    ></NotifyBox>

    <div class="row">
        <div class="col-0 col-md-3 col-xl-4"></div>
        <div class="col-12 col-md-6 col-xl-4">
            <div class="card">
                <form @submit="onCreate" action="#" onsubmit="return false;">
                    <div class="card-header">
                        <div class="card-title">{{ $t("meetingCreateLabel") }}</div>
                    </div>
                    <div class="card-body">
                        <div class="row">
                            <div class="col-12">
                                <div class="form-group">
                                    <label>{{ $t("titleLabel") }}</label>
                                    <input
                                        type="text"
                                        class="form-control"
                                        v-model.trim="createData.title"
                                        minlength="2"
                                        maxlength="255"
                                        required
                                    />
                                </div>
                                <div class="form-group">
                                    <label>{{ $t("iconLabel") }}</label>
                                    <IconSelector
                                        :icons="ICONS"
                                        v-model="createData.icon"
                                    ></IconSelector>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="card-action">
                        <button class="btn btn-success">{{ $t("create") }}</button>
                    </div>
                </form>
            </div>
        </div>
        <div class="col-0 col-md-3 col-xl-4"></div>
    </div>
</template>

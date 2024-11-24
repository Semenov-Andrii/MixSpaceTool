<script setup>
import { ref } from "vue";
import { memberCreateApi } from "@/js/api/project-api.js";
import NotifyBox from "@/components/modal/NotifyBox.vue";
import LoadingWindow from "@/components/modal/LoadingWindow.vue";
import i18n from "@/i18n/index.js";
import { errorToString } from "@/js/utility.js";

const props = defineProps({
    itemId: {
        type: String,
        required: true
    },
    onSuccess: {
        type: Function,
        required: true
    },
    memberType: {
        type: String,
        required: true
    }
});

const model = defineModel({ default: false });

const emptyData = () => {
    return {
        email: ""
    };
};

const formData = ref(emptyData());

const active = ref(false);

const error = ref({
    active: false,
    title: "",
    message: ""
});

i18n.useT();
const onCreated = () => {
    active.value = true;

    memberCreateApi(props.itemId, formData.value.email, props.memberType)
        .then((res) => {
            formData.value = emptyData();
            props.onSuccess(res);
        })
        .catch((err) => {
            console.log(err);
            error.value.title = i18n.t("memberCreateError");
            error.value.message = errorToString(err);
            error.value.active = true;
        })
        .finally(() => {
            active.value = false;
        });
};

const onCancel = () => {
    model.value = false;
};
</script>

<template>
    <NotifyBox
        :title="error.title"
        :message="error.message"
        type="warning"
        v-model="error.active"
    ></NotifyBox>
    <LoadingWindow v-if="active"></LoadingWindow>
    <div v-if="model" class="loading-window" style="z-index: 1030">
        <div class="card">
            <form @submit="onCreated" action="#" onsubmit="return false;">
                <div class="card-header">
                    <div class="card-title">{{ $t("member") }}</div>
                </div>
                <div class="card-body">
                    <div class="row">
                        <div class="col-12">
                            <div class="form-group">
                                <label>{{ $t("emailLabel") }}</label>
                                <input
                                    type="email"
                                    class="form-control"
                                    v-model.trim="formData.email"
                                    minlength="1"
                                    maxlength="200"
                                    required
                                />
                            </div>
                        </div>
                    </div>
                </div>
                <div class="card-action">
                    <button class="btn btn-success me-3" type="submit">
                        {{ $t("addLabel") }}
                    </button>
                    <button class="btn btn-danger" type="button" @click="onCancel">
                        {{ $t("cancelLabel") }}
                    </button>
                </div>
            </form>
        </div>
    </div>
</template>
<style scoped>
.card {
    min-width: 50vw;
}
</style>

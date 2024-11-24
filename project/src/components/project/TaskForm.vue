<script setup>
import { ref, watch } from "vue";
import { memberListApi, taskCreateApi, taskUpdateApi } from "@/js/api/project-api.js";
import i18n from "@/i18n/index.js";
import { errorToString } from "@/js/utility.js";
import NotifyBox from "@/components/modal/NotifyBox.vue";
import LoadingWindow from "@/components/modal/LoadingWindow.vue";

const props = defineProps({
    projectId: {
        type: String,
        required: true
    },
    taskListId: {
        type: Number,
        required: true
    },
    onSuccess: {
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
    },
    init: {
        type: Object,
        default: null
    }
});

const model = defineModel({ default: false });

const emptyData = () => {
    return {
        title: "",
        description: "",
        isDone: false,
        label: null,
        member: null
    };
};

const formData = ref(emptyData());

const active = ref(false);

const error = ref({
    active: false,
    title: "",
    message: ""
});

const labelData = ref({
    text: "",
    color: "#e74c3c"
});

const memberEmail = ref("");

const members = ref([]);

watch(
    () => props.init,
    () => {
        if (props.init) {
            formData.value = props.init;
            labelData.value = props.init.label;
            memberEmail.value = props.init.member?.email ?? i18n.t("notAssigned");
        } else {
            formData.value = emptyData();
            labelData.value = {
                text: "",
                color: "#e74c3c"
            };
            memberEmail.value = i18n.t("notAssigned");
        }
    }
);

memberListApi(props.projectId, "project").then((res) => {
    members.value.push(...res);
});

const onCreated = () => {
    active.value = true;

    const value = formData.value;
    if (labelData.value.text !== "") value.label = labelData.value;
    value.member = members.value.find((item) => item.email === memberEmail.value);

    if (props.init) {
        taskUpdateApi(
            props.init.id,
            value.title,
            value.description,
            value.isDone,
            value.label,
            value.member
        )
            .then((res) => {
                props.onSuccess(res);

                if (labelData.value.text !== "") {
                    props.addLabel(labelData.value);
                }
            })
            .catch((err) => {
                console.log(err);
                error.value.title = i18n.t("taskError");
                error.value.message = errorToString(err);
                error.value.active = true;
            })
            .finally(() => {
                active.value = false;
            });
        return;
    }

    taskCreateApi(
        props.taskListId,
        value.title,
        value.description,
        value.isDone,
        value.label,
        value.member
    )
        .then((res) => {
            formData.value = emptyData();
            props.onSuccess(res);

            if (labelData.value.text !== "") {
                props.addLabel(labelData.value);
            }
        })
        .catch((err) => {
            console.log(err);
            error.value.title = i18n.t("taskError");
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

const onLabelSelected = (event) => {
    const item = props.labelList.find((item) => item.text === event.target.value);
    if (item) {
        labelData.value.color = item.color;
    }
};
</script>

<template>
    <NotifyBox
        :title="error.title"
        :message="error.message"
        type="danger"
        v-model="error.active"
    ></NotifyBox>
    <LoadingWindow v-if="active"></LoadingWindow>
    <div v-if="model" class="loading-window" style="z-index: 1030">
        <div class="card">
            <form @submit="onCreated" action="#" onsubmit="return false;">
                <div class="card-header">
                    <div class="card-title">{{ $t("task") }}</div>
                </div>
                <div class="card-body">
                    <div class="row">
                        <div class="col-12">
                            <div>
                                <label>{{ $t("labelLabel") }}</label>
                                <div class="header-row">
                                    <input
                                        class="form-control form-control-color"
                                        type="color"
                                        v-model="labelData.color"
                                    />
                                    <input
                                        list="labelList"
                                        class="form-control"
                                        v-model.trim="labelData.text"
                                        @change="onLabelSelected"
                                        autocomplete="false"
                                        maxlength="20"
                                    />
                                    <datalist id="labelList" v-if="labelList.length > 0">
                                        <option v-for="label in labelList" :key="label">
                                            {{ label.text }}
                                        </option>
                                    </datalist>
                                </div>
                            </div>
                            <div class="form-group">
                                <label>{{ $t("titleLabel") }}</label>
                                <input
                                    type="text"
                                    class="form-control"
                                    v-model.trim="formData.title"
                                    minlength="1"
                                    maxlength="255"
                                    required
                                />
                            </div>
                            <div class="form-group">
                                <label>{{ $t("descriptionLabel") }}</label>
                                <textarea
                                    type="text"
                                    class="form-control"
                                    v-model.trim="formData.description"
                                    minlength="1"
                                    maxlength="1000"
                                ></textarea>
                            </div>
                            <div class="form-check">
                                <input
                                    type="checkbox"
                                    class="input"
                                    v-model="formData.isDone"
                                    id="flexCheckDefault"
                                />
                                <label class="form-check-label" for="flexCheckDefault">{{
                                    $t("isDoneLabel")
                                }}</label>
                            </div>
                            <div class="form-group">
                                <label>{{ $t("member") }}</label>
                                <select class="form-select" v-model="memberEmail" required>
                                    <option>{{ $t("notAssigned") }}</option>
                                    <option v-for="member in members" :key="member">
                                        {{ member.email }}
                                    </option>
                                </select>
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

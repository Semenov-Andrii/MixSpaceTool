<script setup>
import { ref } from "vue";

const props = defineProps({
    title: {
        type: String,
        required: true
    },
    success: {
        type: Function,
        required: true
    }
});
const model = defineModel({ required: true, default: false });
const input = ref(null);

const onSuccess = () => {
    model.value = false;
    props.success(input.value.files);
};

const onCancel = () => {
    model.value = false;
};
</script>

<template>
    <div v-if="model" class="question-window">
        <div class="row">
            <div class="col-0 col-md-4"></div>
            <div class="col-12 col-md-4 justify-content-center">
                <div class="card">
                    <div class="card-header">
                        <h5>{{ title }}</h5>
                    </div>
                    <div class="card-body">
                        <input ref="input" type="file" multiple="multiple" />
                    </div>
                    <div class="card-footer">
                        <button
                            class="swal-button swal-button--confirm btn btn-success me-4"
                            @click="onSuccess"
                        >
                            {{ $t("upload") }}
                        </button>
                        <button
                            class="swal-button swal-button--cancel btn btn-danger"
                            @click="onCancel"
                        >
                            {{ $t("cancelLabel") }}
                        </button>
                    </div>
                </div>
            </div>
            <div class="col-0 col-md-4"></div>
        </div>
    </div>
</template>

<style scoped>
.question-window {
    top: 0;
    left: 0;
    position: fixed;

    width: 100vw;
    height: 100vh;
    z-index: 2031;
    background-color: #0000001f;

    display: flex;
    justify-content: center;
    align-items: center;
}

.question-window > * {
    width: 100%;
}
</style>

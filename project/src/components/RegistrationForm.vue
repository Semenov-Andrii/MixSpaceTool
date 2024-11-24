<script setup>
import { ref } from "vue";
import { registerUser } from "@/js/auth";
import LoadingWindow from "@/components/modal/LoadingWindow.vue";
import ImageSelector from "@/components/ImageSelector.vue";
import NotifyBox from "./modal/NotifyBox.vue";
import i18n from "@/i18n";
import { errorToString } from "@/js/utility.js";
import { useRouter } from "vue-router";
import { IMAGES } from "@/js/resources";

const router = useRouter();
i18n.useT();

const registerData = ref({
    fullname: "",
    email: "",
    password: "",
    repeatPassword: "",
    position: "",
    avatar: Object.keys(IMAGES)[0]
});

const active = ref(false);

const error = ref({
    active: false,
    title: "",
    message: ""
});

const onRegister = () => {
    active.value = true;

    registerUser(registerData.value)
        .then((res) => {
            console.log(res);
            router.push({ name: "home" });
        })
        .catch((err) => {
            console.log(err);
            error.value.title = i18n.t("registerError");
            error.value.message = errorToString(err);
            error.value.active = true;
        })
        .finally(() => {
            active.value = false;
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
    <LoadingWindow v-if="active"></LoadingWindow>
    <div class="card">
        <form @submit="onRegister" action="#" onsubmit="return false;">
            <div class="card-header">
                <div class="card-title">{{ $t("registration") }}</div>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-12">
                        <div class="form-group">
                            <label>{{ $t("avatarLabel") }}</label>
                            <ImageSelector
                                :images="IMAGES"
                                v-model="registerData.avatar"
                            ></ImageSelector>
                        </div>
                        <div class="form-group">
                            <label>{{ $t("nameLabel") }}</label>
                            <input
                                type="text"
                                class="form-control"
                                v-model.trim="registerData.fullname"
                                minlength="2"
                                maxlength="255"
                                required
                                name="fullname"
                            />
                        </div>
                        <div class="form-group">
                            <label>{{ $t("emailLabel") }}</label>
                            <input
                                type="email"
                                class="form-control"
                                v-model.trim="registerData.email"
                                minlength="5"
                                maxlength="200"
                                required
                                name="email"
                            />
                        </div>
                        <div class="form-group">
                            <label>{{ $t("positionLabel") }}</label>
                            <input
                                type="text"
                                class="form-control"
                                v-model.trim="registerData.position"
                                maxlength="50"
                                required
                                name="position"
                            />
                        </div>
                        <div class="form-group">
                            <label for="password">{{ $t("passwordLabel") }}</label>
                            <input
                                type="password"
                                class="form-control"
                                v-model.trim="registerData.password"
                                minlength="8"
                                maxlength="1000"
                                required
                                name="password"
                            />
                        </div>
                        <div
                            :class="
                                registerData.password !== registerData.repeatPassword
                                    ? 'form-group has-error'
                                    : 'form-group'
                            "
                        >
                            <label for="repeat-password">{{ $t("repeatPasswordLabel") }}</label>
                            <input
                                type="password"
                                class="form-control"
                                v-model.trim="registerData.repeatPassword"
                                minlength="8"
                                maxlength="1000"
                                required
                            />
                        </div>
                    </div>
                </div>
            </div>
            <div class="card-action">
                <button
                    class="btn btn-success"
                    type="submit"
                    :disabled="registerData.password !== registerData.repeatPassword"
                >
                    {{ $t("register") }}
                </button>
            </div>
        </form>
    </div>
</template>

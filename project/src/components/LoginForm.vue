<script setup>
import { ref } from "vue";
import LoadingWindow from "./modal/LoadingWindow.vue";
import { loginUser } from "@/js/auth";
import NotifyBox from "./modal/NotifyBox.vue";
import i18n from "@/i18n";
import { errorToString } from "@/js/utility";
import { useRouter } from "vue-router";

const router = useRouter();

const loginData = ref({
    email: "",
    password: ""
});
const active = ref(false);

const error = ref({
    active: false,
    title: "",
    message: ""
});

const onLogin = () => {
    active.value = true;

    loginUser(loginData.value.email, loginData.value.password)
        .then(() => {
            router.push({ name: "home" });
        })
        .catch((err) => {
            console.log(err);
            error.value.title = i18n.t("loginError");
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
    <div class="card">
        <form @submit="onLogin" action="#" onsubmit="return false;">
            <div class="card-header">
                <div class="card-title">{{ $t("loginLabel") }}</div>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-12">
                        <div class="form-group">
                            <label>{{ $t("emailLabel") }}</label>
                            <input
                                type="email"
                                class="form-control"
                                v-model.trim="loginData.email"
                                maxlength="200"
                                required
                                name="email"
                            />
                        </div>
                        <div class="form-group">
                            <label for="password">{{ $t("passwordLabel") }}</label>
                            <input
                                type="password"
                                class="form-control"
                                v-model.trim="loginData.password"
                                maxlength="1000"
                                required
                                name="password"
                            />
                        </div>
                    </div>
                </div>
            </div>
            <div class="card-action">
                <button class="btn btn-success">{{ $t("login") }}</button>
            </div>
        </form>
    </div>
</template>

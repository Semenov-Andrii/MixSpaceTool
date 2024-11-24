<script setup>
import { getUser, logoutUser } from "@/js/auth.js";
import LocalizedLink from "../l10n/LocalizedLink.vue";
import { ref } from "vue";
import { IMAGES } from "@/js/resources";

const user = ref(getUser());

window.addEventListener("auth", (data) => {
    user.value = data.detail;
});
</script>
<template>
    <div v-if="user">
        <a
            class="dropdown-toggle profile-pic"
            data-bs-toggle="dropdown"
            href="#"
            aria-expanded="false"
        >
            <div class="avatar-sm">
                <img
                    :src="IMAGES[user.avatar]"
                    alt="image profile"
                    class="avatar-img rounded-circle"
                />
            </div>
            <span class="profile-username">
                <span class="op-7">{{ $t("hi") }},</span>
                <span class="fw-bold">{{ user.fullname }}</span>
            </span>
        </a>
        <ul class="dropdown-menu dropdown-user animated fadeIn">
            <div class="dropdown-user-scroll scrollbar-outer">
                <li>
                    <div class="user-box">
                        <div class="avatar-lg">
                            <img
                                :src="IMAGES[user.avatar]"
                                alt="image profile"
                                class="avatar-img rounded"
                            />
                        </div>
                        <div class="u-text">
                            <h4>{{ user.fullname }}</h4>
                            <p class="text-muted">{{ user.username }}</p>
                        </div>
                    </div>
                </li>
                <li>
                    <div class="dropdown-divider"></div>
                    <a class="dropdown-item" href="#">My Profile</a>
                    <div class="dropdown-divider"></div>
                    <button class="dropdown-item" @click="logoutUser">Logout</button>
                </li>
            </div>
        </ul>
    </div>
</template>

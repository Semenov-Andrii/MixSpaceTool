<script setup>
import { ref } from "vue";
import MenuItem from "./MenuItem.vue";
import MenuSeparator from "./MenuSeparator.vue";
import CollapsedMenuItem from "./CollapsedMenuItem.vue";
import { getUser } from "@/js/auth";

const user = ref(getUser());

window.addEventListener("auth", (data) => {
    user.value = data.detail;
});
</script>

<template>
    <div class="sidebar-wrapper scrollbar scrollbar-inner">
        <div class="sidebar-content">
            <ul v-if="user" class="nav nav-secondary">
                <MenuItem url="/" :text="$t('home')" icon="fa-solid fa-house"> </MenuItem>

                <MenuSeparator :text="$t('meetings')"></MenuSeparator>
                <MenuItem url="/meeting" :text="$t('newMeeting')" icon="fa-solid fa-video">
                </MenuItem>
                <MenuItem url="/meetings" :text="$t('allMeetings')" icon="fa-solid fa-file-video">
                </MenuItem>

                <MenuSeparator :text="$t('projects')"></MenuSeparator>
                <MenuItem url="/project" :text="$t('newProject')" icon="fa-solid fa-list-check">
                </MenuItem>
                <MenuItem url="/projects" :text="$t('allProjects')" icon="fa-solid fa-briefcase">
                </MenuItem>

                <MenuSeparator :text="$t('repositories')"></MenuSeparator>
                <MenuItem url="/repository" :text="$t('newRepository')" icon="fa-solid fa-code">
                </MenuItem>
                <MenuItem url="/repositories" :text="$t('allRepositories')" icon="fa-solid fa-file">
                </MenuItem>
            </ul>
            <ul v-else class="nav nav-secondary">
                <MenuItem
                    url="/auth"
                    :text="$t('login')"
                    icon="fa-solid fa-person-walking-arrow-right"
                >
                </MenuItem>
            </ul>
        </div>
    </div>
</template>

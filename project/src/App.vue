<script setup>
import { RouterView } from "vue-router";
import LocalizedLink from "@/components/l10n/LocalizedLink.vue";
import MainMenu from "./components/app/MainMenu.vue";
import AccountWidget from "./components/app/AccountWidget.vue";
import LanguageSelect from "./components/l10n/LanguageSelect.vue";
import TimerPopup from "@/components/project/TimerPopup.vue";
</script>

<template>
    <TimerPopup></TimerPopup>
    <div v-if="$route.name !== 'meeting'" class="wrapper">
        <div class="sidebar scrollbar" data-background-color="dark">
            <div class="sidebar-logo">
                <!-- Logo Header -->
                <div class="logo-header" data-background-color="dark">
                    <LocalizedLink to="/" class="logo">
                        <img
                            src="./assets/logo_light.png"
                            alt="navbar brand"
                            class="navbar-brand"
                            height="20"
                        />
                    </LocalizedLink>
                    <div class="nav-toggle">
                        <button class="btn btn-toggle toggle-sidebar">
                            <i class="gg-menu-right"></i>
                        </button>
                        <button class="btn btn-toggle sidenav-toggler">
                            <i class="gg-menu-left"></i>
                        </button>
                    </div>
                    <button class="topbar-toggler more">
                        <i class="gg-more-vertical-alt"></i>
                    </button>
                </div>
                <!-- End Logo Header -->
            </div>

            <MainMenu></MainMenu>
        </div>
        <div class="main-panel">
            <div class="main-header">
                <div class="main-header-logo">
                    <!-- Logo Header -->
                    <div class="logo-header" data-background-color="dark">
                        <LocalizedLink to="/" class="logo">
                            <img
                                src="./assets/logo_light.png"
                                alt="navbar brand"
                                class="navbar-brand"
                                height="20"
                            />
                        </LocalizedLink>
                        <div class="nav-toggle">
                            <button class="btn btn-toggle toggle-sidebar">
                                <i class="gg-menu-right"></i>
                            </button>
                            <button class="btn btn-toggle sidenav-toggler">
                                <i class="gg-menu-left"></i>
                            </button>
                        </div>
                        <button class="topbar-toggler more">
                            <i class="gg-more-vertical-alt"></i>
                        </button>
                    </div>
                    <!-- End Logo Header -->
                </div>

                <nav
                    class="navbar navbar-header navbar-header-transparent navbar-expand-lg border-bottom"
                >
                    <div class="container-fluid">
                        <ul class="navbar-nav topbar-nav ms-md-auto align-items-center">
                            <li class="nav-item">
                                <div>
                                    <LanguageSelect></LanguageSelect>
                                </div>
                            </li>

                            <li class="nav-item topbar-user dropdown hidden-caret">
                                <AccountWidget></AccountWidget>
                            </li>
                        </ul>
                    </div>
                </nav>
            </div>

            <div class="container">
                <div class="page-inner">
                    <div
                        class="d-flex align-items-center flex-column flex-md-row pt-2 pb-4 full-width"
                    >
                        <RouterView />
                    </div>
                </div>
            </div>
        </div>
    </div>
    <div v-else class="container-meet">
        <div class="container">
            <div class="page-inner">
                <div class="d-flex align-items-center flex-column flex-md-row pt-2 pb-4 full-width">
                    <RouterView />
                </div>
            </div>
        </div>
    </div>
</template>
<style>
.full-width > * {
    width: 100%;
}
</style>

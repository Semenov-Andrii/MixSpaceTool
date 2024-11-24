import { createRouter, createWebHistory } from "vue-router";
import i18n, { defaultLocale } from "@/i18n";
import { ifAuthenticated } from "@/js/auth";

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: "/",
            redirect: `/${defaultLocale}`
        },
        {
            path: "/:locale",
            children: [
                {
                    path: "",
                    name: "home",
                    component: () => import("../views/HomeView.vue"),
                    beforeEnter: ifAuthenticated
                },
                {
                    path: "auth",
                    name: "auth",
                    component: () => import("../views/AuthView.vue")
                },
                {
                    path: "meetings",
                    name: "meetings",
                    component: () => import("../views/MeetingsView.vue"),
                    beforeEnter: ifAuthenticated
                },
                {
                    path: "meeting",
                    name: "new-meeting",
                    component: () => import("../views/NewMeetingView.vue"),
                    beforeEnter: ifAuthenticated
                },
                {
                    path: "meeting/:meetingId",
                    name: "meeting",
                    component: () => import("../views/MeetingView.vue"),
                    beforeEnter: ifAuthenticated
                },
                {
                    path: "projects",
                    name: "projects",
                    component: () => import("../views/ProjectsView.vue"),
                    beforeEnter: ifAuthenticated
                },
                {
                    path: "project",
                    name: "new-project",
                    component: () => import("../views/NewProjectView.vue"),
                    beforeEnter: ifAuthenticated
                },
                {
                    path: "project/:projectId",
                    name: "project",
                    component: () => import("../views/ProjectView.vue"),
                    beforeEnter: ifAuthenticated
                },
                {
                    path: "repository",
                    name: "new-repository",
                    component: () => import("../views/NewRepositoryView.vue"),
                    beforeEnter: ifAuthenticated
                },
                {
                    path: "repository/:repositoryId",
                    name: "repository",
                    component: () => import("../views/RepositoryView.vue"),
                    beforeEnter: ifAuthenticated
                },
                {
                    path: "repositories",
                    name: "repositories",
                    component: () => import("../views/RepositoriesView.vue"),
                    beforeEnter: ifAuthenticated
                }
            ]
        },
        {
            path: "/:pathMatch(.*)*",
            name: "not-found",
            component: () => import("../views/NotFoundView.vue")
        }
    ],
    scrollBehavior(to, from, savedPosition) {
        if (to === from) return savedPosition;

        return { top: 0 };
    }
});

router.beforeEach((to, from) => {
    const newLocale = to.params.locale;
    const prevLocale = from.params.locale;
    if (newLocale === prevLocale) {
        return;
    }
    i18n.setLocale(newLocale);
});

export default router;

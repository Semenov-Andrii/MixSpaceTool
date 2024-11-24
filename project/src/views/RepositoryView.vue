<script setup>
import { useRoute, useRouter } from "vue-router";
import { ref } from "vue";
import i18n from "@/i18n/index.js";
import { errorToString, validateFilename } from "@/js/utility.js";
import {
    commitCreateApi,
    commitGotoApi,
    commitListApi,
    downloadFileContent,
    fileUpdateApi,
    repositoryDeleteApi,
    repositoryGetApi
} from "@/js/api/repository-api.js";
import NotifyBox from "@/components/modal/NotifyBox.vue";
import LoadingWindow from "@/components/modal/LoadingWindow.vue";
import FileTree from "@/components/repository/FileTree.vue";
import AceScriptEditor from "@/components/repository/AceScriptEditor.vue";
import { mapFiles } from "@/js/file-utility.js";
import InputWindow from "@/components/modal/InputWindow.vue";
import CommitList from "@/components/repository/CommitList.vue";
import DotsButton from "@/components/DotsButton.vue";
import MemberList from "@/components/project/MemberList.vue";
import QuestionWindow from "@/components/modal/QuestionWindow.vue";

const { repositoryId } = useRoute().params;

const repository = ref(null);
const instance = ref(0);

const active = ref(true);

const error = ref({
    active: false,
    title: "",
    message: ""
});

const errorCatch = (promise) => {
    return promise.catch((err) => {
        console.log(err);
        error.value.title = i18n.t("repositoryError");
        error.value.message = errorToString(err);
        error.value.active = true;
    });
};

i18n.useT();

errorCatch(
    repositoryGetApi(repositoryId).then((res) => {
        repository.value = res;
        instance.value++;
    })
).finally(() => {
    active.value = false;
});

const currentFile = ref(null);

const editingNow = ref(false);

const refreshRepo = () => {
    currentFile.value = null;

    active.value = true;
    errorCatch(
        repositoryGetApi(repositoryId).then((res) => {
            repository.value = res;
            instance.value++;
        })
    ).finally(() => {
        active.value = false;
    });
};

const onChange = (defaultValue = true) => {
    editingNow.value = defaultValue;
};

const autoSave = () => {
    if (currentFile.value && "content" in currentFile.value) {
        errorCatch(
            fileUpdateApi(currentFile.value.id, currentFile.value.content).then(() => {
                editingNow.value = false;
            })
        );
    }
};

const onFileClick = (file) => {
    if (!file) {
        currentFile.value = undefined;
        return;
    }
    if (file.fileType !== "file") return;

    autoSave();

    currentFile.value = file;
    if ("content" in file) return;

    downloadFileContent(file.id)
        .then((res) => {
            file.content = res;
            editingNow.value = false;
        })
        .catch((err) => {
            file.content = errorToString(err);
        });
};

const refreshFile = () => {
    if (currentFile.value.fileType !== "file") return;
    downloadFileContent(currentFile.value.id)
        .then((res) => {
            currentFile.value.content = res;
            editingNow.value = false;
        })
        .catch((err) => {
            currentFile.value.content = errorToString(err);
        });
};

const inputActive = ref(false);
const commitActive = ref(false);
const commits = ref([]);

const onCommit = (title) => {
    errorCatch(
        commitCreateApi(repositoryId, title).then((res) => {
            commits.value.unshift(res);
        })
    );
};

errorCatch(
    commitListApi(repositoryId).then((res) => {
        commits.value = res;
    })
);

const goToCommit = (id) => {
    errorCatch(
        commitGotoApi(repositoryId, id).then((res) => {
            repository.value = res;
            currentFile.value = null;
            editingNow.value = false;
            instance.value++;
        })
    );
};

const removeActive = ref(false);
const router = useRouter();

const onRemoveRepo = () => {
    errorCatch(
        repositoryDeleteApi(repositoryId).then(() => {
            router.push({ name: "repositories", params: { locale: i18n.getLocale() } });
        })
    );
};

const memberActive = ref(false);
</script>

<template>
    <InputWindow
        :title="$t('commitTitle')"
        :success="onCommit"
        :message="$t('commitMsg')"
        :normalize-func="validateFilename"
        v-model="inputActive"
    />
    <QuestionWindow
        :title="$t('removeRepo')"
        :success="onRemoveRepo"
        :message="$t('removeRepoMsg')"
        v-model="removeActive"
    ></QuestionWindow>
    <NotifyBox v-model="error.active" :message="error.message" :title="error.title" type="danger" />
    <LoadingWindow v-if="active" />
    <CommitList
        :commits="commits"
        v-model="commitActive"
        :owner="repository?.owner"
        :go-to="goToCommit"
    />
    <MemberList
        :item-id="repositoryId"
        v-model="memberActive"
        :owner="repository?.owner"
        member-type="repository"
    ></MemberList>
    <div v-if="repository">
        <div class="m-4">
            <div class="header-row">
                <h3 class="fw-bold mb-3">
                    <i :class="repository.icon"></i> {{ repository.title }}
                    <i
                        class="fa-solid fa-arrow-rotate-right dots-btn ms-1"
                        @click="refreshRepo"
                    ></i>
                </h3>
                <div>
                    <DotsButton>
                        <template v-slot:list>
                            <a class="dropdown-item" href="#" @click="inputActive = true">
                                {{ $t("commit") }}
                            </a>
                            <a class="dropdown-item" href="#" @click="commitActive = true">
                                {{ $t("commits") }}
                            </a>
                            <a class="dropdown-item" href="#" @click="memberActive = true">
                                {{ $t("members") }}
                            </a>
                            <a class="dropdown-item" href="#" @click="removeActive = true">
                                {{ $t("removeRepo") }}
                            </a>
                        </template>
                    </DotsButton>
                </div>
            </div>
            <p>{{ repository.description }}</p>
        </div>
        <div class="row">
            <div class="col-3">
                <FileTree
                    :key="instance"
                    :title="repository.title"
                    :repository-id="repository.id"
                    :files="mapFiles(repository.files)"
                    :on-click="onFileClick"
                ></FileTree>
            </div>
            <div class="col-9" v-if="currentFile">
                <div class="file-header">
                    <span> {{ currentFile.name }}</span
                    ><span v-if="editingNow">*</span>
                    <i
                        class="fa-solid fa-arrow-rotate-right dots-btn ms-1"
                        @click="refreshFile"
                    ></i>
                </div>
                <AceScriptEditor
                    v-model="currentFile.content"
                    :filename="currentFile.name"
                    :on-save="autoSave"
                    :on-change="onChange"
                ></AceScriptEditor>
            </div>
        </div>
    </div>
</template>

<style scoped>
.file-header {
    left: 0;
    margin: 0;
}
</style>

<script setup>
import { ref } from "vue";
import FileItem from "@/components/repository/FileItem.vue";
import ContextButton from "@/components/ContextMenu.vue";
import i18n from "@/i18n/index.js";
import { mapFiles, renameChildUtil, uploadedFileUtil } from "@/js/file-utility.js";
import FileUploadWindow from "@/components/repository/FileUploadWindow.vue";
import { fileDeleteApi } from "@/js/api/repository-api.js";

const props = defineProps({
    repositoryId: {
        type: String,
        required: true
    },
    title: {
        type: String,
        required: true
    },
    files: {
        type: Array,
        required: true
    },
    onClick: {
        type: Function,
        required: true
    }
});

i18n.useT();

const files = ref(props.files);

const newFile = () => {
    files.value.push({
        name: i18n.t("newFileName"),
        fileType: "file",
        editActive: true
    });
};
const newDir = () => {
    files.value.push({
        name: i18n.t("newDirName"),
        fileType: "dir",
        files: [],
        editActive: true
    });
};

const uploadActive = ref(false);
const uploadFile = () => {
    uploadActive.value = true;
};

const contextMenu = ref(null);
const functions = ref([
    {
        name: i18n.t("newFile"),
        action: newFile
    },
    {
        name: i18n.t("newDir"),
        action: newDir
    },
    {
        name: i18n.t("uploadFile"),
        action: uploadFile
    }
]);

const renameChild = (id, oldName, newName) => {
    renameChildUtil(props.repositoryId, files.value, id, oldName, newName, null);
};
const turnEditChild = (name) => {
    const file = files.value.find((file) => file.name === name);
    if (file) {
        file.editActive = true;
    }
};

const uploaded = (fileList) => {
    uploadedFileUtil(props.repositoryId, null, files.value, fileList).catch((err) => {
        console.log(err);
    });
};

const removeChild = (childId) => {
    fileDeleteApi(childId)
        .then(() => {
            files.value = files.value.filter((item) => item.id !== childId);
            props.onClick(undefined);
        })
        .catch((err) => {
            console.log(err);
        });
};
</script>

<template>
    <ContextButton ref="contextMenu" :functions="functions"></ContextButton>
    <FileUploadWindow :title="$t('uploadFile')" :success="uploaded" v-model="uploadActive" />
    <div class="file-header" @contextmenu="contextMenu?.showContext">
        <span> {{ title }}</span>
    </div>
    <ul class="file-ul file-tree">
        <FileItem
            v-for="file in files"
            :key="(file.id ?? '') + file.name"
            :repository-id="repositoryId"
            :file-id="file.id"
            :name="file.name"
            :file-type="file.fileType"
            :files="mapFiles(file.files)"
            :edit-active="file.editActive"
            :turn-edit="() => turnEditChild(file.name)"
            :edit-name="(newName) => renameChild(file.id, file.name, newName)"
            :on-click="(instance) => onClick(instance ? instance : file)"
            :remove-self="() => removeChild(file.id)"
        ></FileItem>
    </ul>
</template>
<style scoped>
.file-tree {
    overflow-x: auto;
    width: 100%;
    height: 100%;
    min-height: 50vh;
    z-index: 100;

    -webkit-user-select: none;
    -ms-user-select: none;
    user-select: none;
}
.file-ul {
    margin-top: 0;
}
</style>

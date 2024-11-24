<script setup>
import { ref } from "vue";
import ContextButton from "@/components/ContextMenu.vue";
import i18n from "@/i18n/index.js";
import { mapFiles, renameChildUtil, uploadedFileUtil } from "@/js/file-utility.js";
import FileUploadWindow from "@/components/repository/FileUploadWindow.vue";
import { validateFilename } from "@/js/utility.js";
import { fileDeleteApi, getDownloadFileUrl } from "@/js/api/repository-api.js";
import { getToken } from "@/js/auth.js";

const props = defineProps({
    repositoryId: {
        type: String,
        required: true
    },
    fileId: {
        type: String,
        required: false,
        default: null
    },
    fileType: {
        type: String,
        required: true
    },
    name: {
        type: String,
        required: true
    },
    files: {
        type: Array,
        required: false,
        default: () => []
    },
    editActive: {
        type: Boolean,
        required: false,
        default: true
    },
    turnEdit: {
        type: Function,
        required: true
    },
    editName: {
        type: Function,
        required: true
    },
    onClick: {
        type: Function,
        required: true
    },
    removeSelf: {
        type: Function,
        required: true
    }
});

const files = ref(props.files);

const newFile = () => {
    const file = {
        id: null,
        name: i18n.t("newFileName"),
        fileType: "file",
        editActive: true
    };
    files.value.push(file);
};
const newDir = () => {
    files.value.push({
        name: i18n.t("newDirName"),
        fileType: "dir",
        files: [],
        editActive: true
    });
};

const download = () => {
    fetch(getDownloadFileUrl(props.fileId), {
        method: "GET",
        headers: {
            Authorization: `Token ${getToken()}`
        }
    })
        .then((response) => response.blob())
        .then((blob) => {
            const link = document.createElement("a");
            link.href = URL.createObjectURL(blob);
            link.download = props.name;
            link.click();
            link.remove();
        })
        .catch((error) => console.log(error));
};

const fileFunctions = ref([
    {
        name: i18n.t("renameFile"),
        action: props.turnEdit
    },
    {
        name: i18n.t("removeFile"),
        action: props.removeSelf
    },
    {
        name: i18n.t("download"),
        action: download
    }
]);

const contextMenu = ref(null);

const renameChild = (id, oldName, newName) => {
    renameChildUtil(props.repositoryId, files.value, id, oldName, newName, props.fileId);
};
const turnEditChild = (name) => {
    const file = files.value.find((file) => file.name === name);
    if (file) {
        file.editActive = true;
    }
};

const name = ref(props.name);

const renameEnter = (e) => {
    if (e.key === "Enter") {
        props.editName(name.value);
    }
};

const renameFocus = () => {
    props.editName(name.value);
};
const uploadActive = ref(false);

const uploaded = (fileList) => {
    uploadedFileUtil(props.repositoryId, props.fileId, files.value, fileList);
};

const uploadFile = () => {
    uploadActive.value = true;
};

const dirFunctions = ref([
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
    },
    {
        name: i18n.t("renameDir"),
        action: props.turnEdit
    },
    {
        name: i18n.t("removeDir"),
        action: props.removeSelf
    }
]);

const validateInput = () => {
    name.value = validateFilename(name.value);
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
    <ContextButton
        ref="contextMenu"
        :functions="fileType === 'dir' ? dirFunctions : fileFunctions"
    />
    <FileUploadWindow :title="$t('uploadFile')" :success="uploaded" v-model="uploadActive" />
    <li>
        <input v-if="fileType === 'dir'" type="checkbox" checked />
        <span @contextmenu="contextMenu?.showContext">
            <span v-if="!editActive" @click="onClick(null)">{{ name }}</span>
            <input
                v-else
                type="text"
                v-model.trim="name"
                maxlength="100"
                @keydown="renameEnter"
                @focusout="renameFocus"
                @input="validateInput"
            />
        </span>

        <ul v-if="fileType === 'dir'" class="file-ul">
            <FileItem
                v-for="file in files"
                :key="(file.id ?? '') + file.name"
                :repository-id="repositoryId"
                :file-id="file.id"
                :file-type="file.fileType"
                :name="file.name"
                :files="mapFiles(file.files)"
                :edit-active="file.editActive"
                :turn-edit="() => turnEditChild(file.name)"
                :edit-name="(newName) => renameChild(file.id, file.name, newName)"
                :on-click="(instance) => onClick(instance ? instance : file)"
                :remove-self="() => removeChild(file.id)"
            ></FileItem>
        </ul>
    </li>
</template>
<style></style>

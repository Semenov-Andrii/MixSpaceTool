<script setup>
import { onMounted, watch } from "vue";
import ace from "ace-builds/src-noconflict/ace";
import { detectLanguage } from "@/js/language-detector.js";

const props = defineProps({
    filename: {
        type: String,
        required: false,
        default: "temp.txt"
    },
    onSave: {
        type: Function,
        required: false,
        default: () => {}
    },
    onChange: {
        type: Function,
        required: false,
        default: () => {}
    }
});

const getAceMode = (language) => {
    const mode = `ace/mode/${language.toLowerCase()}`;
    try {
        ace.require(mode);
        return mode;
    } catch (e) {
        return "ace/mode/text";
    }
};

const getMode = (filename) => {
    const language = detectLanguage(filename);
    return getAceMode(language);
};

const content = defineModel({ default: "" });

onMounted(() => {
    const editor = ace.edit("editor");
    editor.setTheme("ace/theme/dracula-css");
    editor.session.setMode(getMode(props.filename));
    editor.setValue(content.value);
    editor.session.on("change", () => {
        content.value = editor.getValue();
        props.onChange();
    });
});

watch(
    () => props.filename,
    () => {
        const editor = ace.edit("editor");
        editor.session.setMode(getMode(props.filename));
    }
);

watch(content, (newValue) => {
    const editor = ace.edit("editor");
    if (editor.getValue() !== newValue) {
        editor.setValue(newValue, -1);
        props.onChange(false);
    }
});
</script>

<template>
    <div
        id="editor"
        @keydown.ctrl.exact="
            (event) => {
                if (event.code === 'KeyS') {
                    event.preventDefault();
                    onSave();
                }
            }
        "
    ></div>
</template>

<style scoped>
#editor {
    height: 500px;
    z-index: 10;
    position: relative;
}
</style>

<script setup>
import { ref } from "vue";
const props = defineProps({
    functions: {
        type: Array,
        required: true
    }
});

const contextMenu = ref(null);

const showContext = (e) => {
    e.preventDefault();
    contextMenu.value = {
        style: `top:${e.pageY - 10}px;left:${e.pageX - 40}px`,
        functions: props.functions
    };
};

const click = (action) => {
    contextMenu.value = null;
    action();
};

defineExpose({
    showContext
});
</script>

<template>
    <div
        v-if="contextMenu"
        class="ctx-menu"
        :style="contextMenu.style"
        @mouseleave="() => (contextMenu = null)"
        @contextmenu="(e) => e.preventDefault()"
    >
        <p v-for="func in contextMenu.functions" :key="func" @click="click(func.action)">
            {{ func.name }}
        </p>
    </div>
</template>

<style>
.ctx-menu {
    position: fixed;
    background: ghostwhite;
    color: black;
    cursor: pointer;
    border: 1px black solid;
    z-index: 150;
}

.ctx-menu > p {
    padding: 0 1rem;
    margin: 0;
}

.ctx-menu > p:hover {
    background: black;
    color: ghostwhite;
}
</style>

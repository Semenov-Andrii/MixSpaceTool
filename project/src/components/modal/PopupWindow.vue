<script setup>
import { onMounted, onUnmounted } from "vue";

const eventBusPopup = defineModel({ required: true });

const togglePopup = () => {
    eventBusPopup.value.togglePopup();
    console.log("click");
};

const startDrag = (e) => {
    eventBusPopup.value.startDrag(e);
    document.addEventListener("mousemove", onDrag);
    document.addEventListener("mouseup", stopDrag);
};

const onDrag = (e) => {
    eventBusPopup.value.onDrag(e);
};

const stopDrag = () => {
    eventBusPopup.value.stopDrag();
    document.removeEventListener("mousemove", onDrag);
    document.removeEventListener("mouseup", stopDrag);
};

onMounted(() => {
    document.addEventListener("mousemove", onDrag);
    document.addEventListener("mouseup", stopDrag);
});

onUnmounted(() => {
    document.removeEventListener("mousemove", onDrag);
    document.removeEventListener("mouseup", stopDrag);
});
</script>
<template>
    <div
        v-if="eventBusPopup.popupVisible"
        class="popup"
        :style="{
            top: eventBusPopup.position.top + 'px',
            left: eventBusPopup.position.left + 'px'
        }"
        ref="popup"
    >
        <div class="popup-header" @mousedown.prevent="startDrag">
            <div><slot name="header"></slot></div>
            <i class="fa-solid fa-xmark dots-btn" @click="togglePopup"></i>
        </div>
        <div class="popup-body">
            <slot name="content"></slot>
        </div>
    </div>
</template>
<style scoped>
.popup {
    position: fixed;
    z-index: 2000;
    width: 200px;
    border: 1px solid #ccc;
    background: #fff;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.popup-header {
    background-color: #f1f1f1;
    padding: 5px;
    cursor: move;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.popup-body {
    padding: 5px;
}
</style>

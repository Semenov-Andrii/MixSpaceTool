<script setup>
defineProps({
    title: {
        type: String,
        required: true
    },
    message: {
        type: String,
        required: true
    },
    type: {
        type: String,
        required: true
    }
});

const model = defineModel({ required: true, default: false });
</script>

<template>
    <div
        v-if="model"
        data-notify="container"
        :class="`col-10 col-xs-11 col-sm-4 alert alert-${type} notify-container`"
        role="alert"
        data-notify-position="top-center"
    >
        <button
            type="button"
            aria-hidden="true"
            class="close notify-dismiss"
            data-notify="dismiss"
            @click="model = false"
        >
            ×
        </button>
        <span data-notify="icon" class="fa fa-bell"></span>
        <span data-notify="title">{{ title }}</span>
        <span data-notify="message">{{ message }}</span>
        <a href="#" data-notify="url" class="notify-url"></a>
    </div>
</template>
<style>
.notify-container {
    display: inline-block;
    margin: 0 auto;
    padding-left: 65px;
    position: fixed;
    transition: all 0.5s ease-in-out;
    z-index: 1032;
    top: 20px;
    left: 0;
    right: 0;

    max-width: 50vw;
}

.notify-dismiss {
    position: absolute;
    right: 10px;
    top: 5px;
    z-index: 1033;
}

.notify-url {
    background-image: url("data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7");
    height: 100%;
    left: 0;
    position: absolute;
    top: 0;
    width: 100%;
    z-index: 1032;
}
</style>

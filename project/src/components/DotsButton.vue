<script setup>
defineProps({
    theme: {
        type: String,
        required: false,
        default: "default"
    }
});
</script>
<template>
    <div class="btn-group dropstart">
        <button
            type="button"
            class="btn-none"
            data-bs-toggle="dropdown"
            aria-haspopup="true"
            aria-expanded="false"
        >
            <i
                :class="
                    'fa-solid fa-ellipsis-vertical dots-btn' +
                    (theme === 'dark' ? ' list-color' : '')
                "
            ></i>
        </button>
        <ul class="dropdown-menu" role="menu">
            <slot name="list"></slot>
        </ul>
    </div>
</template>

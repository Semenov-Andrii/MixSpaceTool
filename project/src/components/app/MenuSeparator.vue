<script setup>
defineProps({
    text: {
        type: String,
        required: true
    }
});
</script>
<template>
    <li class="nav-section">
        <span class="sidebar-mini-icon">
            <i class="fa fa-ellipsis-h"></i>
        </span>
        <h4 class="text-section">{{ text }}</h4>
    </li>
</template>

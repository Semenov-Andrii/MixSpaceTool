<script setup>
import LocalizedLink from "@/components/l10n/LocalizedLink.vue";

defineProps({
    url: {
        type: String,
        required: true
    },
    text: {
        type: String,
        required: true
    },
    icon: {
        type: String,
        required: true
    }
});
</script>
<template>
    <li class="nav-item">
        <LocalizedLink :to="url">
            <i :class="icon"></i>
            <p>{{ text }}</p>
        </LocalizedLink>
    </li>
</template>

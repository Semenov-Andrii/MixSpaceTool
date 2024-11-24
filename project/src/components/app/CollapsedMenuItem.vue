<script setup>
import { uuid } from "vue-uuid";
import { ref } from "vue";
const componentId = ref(uuid.v4());

defineProps({
    title: {
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
        <a
            data-bs-toggle="collapse"
            :href="`#${componentId}`"
            aria-expanded="false"
            class="collapsed"
        >
            <i :class="icon"></i>
            <p>{{ title }}</p>
            <span class="caret"></span>
        </a>
        <div class="collapse" :id="componentId">
            <ul class="nav nav-collapse">
                <slot name="inside"></slot>
            </ul>
        </div>
    </li>
</template>

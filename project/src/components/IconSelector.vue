<script setup>
defineProps({
    icons: {
        type: Array,
        required: true
    }
});

const model = defineModel({ default: "" });
</script>

<template>
    <div class="row">
        <div v-for="icon in icons" :key="icon" class="col col-center">
            <label class="imagecheck mb-4">
                <input
                    name="imagecheck"
                    type="radio"
                    :value="icon"
                    class="imagecheck-input"
                    v-model="model"
                />
                <figure class="imagecheck-figure icon-figure">
                    <i :class="icon"></i>
                </figure>
            </label>
        </div>
    </div>
</template>
<style>
.icon-figure {
    padding: 10px;
}
</style>

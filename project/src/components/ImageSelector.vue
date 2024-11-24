<script setup>
defineProps({
    images: {
        type: Object,
        required: true
    }
});

const model = defineModel({ default: "" });
</script>

<template>
    <div class="row">
        <div v-for="(image, name) in images" :key="name" class="col-3 col-md-4 col-xl-2">
            <label class="imagecheck mb-4">
                <input
                    name="imagecheck"
                    type="radio"
                    :value="name"
                    class="imagecheck-input"
                    v-model="model"
                />
                <figure class="imagecheck-figure">
                    <img :src="image" alt="title" class="imagecheck-image" />
                </figure>
            </label>
        </div>
    </div>
</template>

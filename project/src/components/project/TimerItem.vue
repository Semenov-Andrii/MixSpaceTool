<script setup>
import { IMAGES } from "@/js/resources.js";
import { getTimeDifference } from "@/js/utility.js";

defineProps({
    comment: {
        type: String,
        required: true
    },
    start: {
        type: String,
        required: true
    },
    end: {
        type: String,
        required: false,
        default: null
    },
    member: {
        type: Object,
        required: true
    }
});
</script>

<template>
    <div class="card list-color mt-2">
        <div class="card-header">
            <h6>
                <img
                    :src="IMAGES[member.avatar]"
                    alt="image profile"
                    class="avatar-img rounded-circle"
                />{{ member.fullname }} - {{ member.position }}
            </h6>
        </div>
        <div class="card-body">
            <p>
                {{ new Date(start).toLocaleString() }} -
                <span v-if="end">{{ new Date(end).toLocaleString() }}</span
                ><span v-else>{{ $t("noEnd") }}</span>
            </p>
            <p>
                {{ $t("workFor") }}
                {{
                    getTimeDifference(start, end, {
                        day: $t("day"),
                        hour: $t("hour"),
                        minute: $t("minute"),
                        second: $t("second")
                    })
                }}
            </p>
        </div>
        <div v-if="comment && comment.length > 0" class="card-footer">
            {{ comment }}
        </div>
    </div>
</template>
<style scoped>
.card {
    margin-bottom: 1px;
}

.card-body > p {
    font-size: 1em;
    margin-bottom: 1px;
}

.card-body {
    padding: 10px;
}
.avatar-img {
    width: 35px;
    height: 35px;
    padding-right: 2px;
}
</style>

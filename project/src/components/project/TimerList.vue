<script setup>
import { computed } from "vue";
import TimerItem from "@/components/project/TimerItem.vue";

const props = defineProps({
    timers: {
        type: Array,
        required: true
    },
    owner: {
        type: Object
    },
    refresh: {
        type: Function,
        required: true
    }
});

const timers = computed(() => props.timers);
const model = defineModel({ default: false });
</script>

<template>
    <div v-if="model" class="member-window">
        <div class="row">
            <div class="col-0 col-md-4"></div>
            <div class="col-12 col-md-4">
                <div class="member-list">
                    <div class="header-row">
                        <h4>
                            {{ $t("timers") }}
                            <i
                                class="fa-solid fa-arrow-rotate-right dots-btn ms-1"
                                @click="refresh"
                            />
                        </h4>
                        <div>
                            <button type="button" class="btn-none list-color">
                                <i class="fa-solid fa-xmark" @click="model = false"></i>
                            </button>
                        </div>
                    </div>

                    <div v-if="timers.length > 0" class="members" id="style-3">
                        <TimerItem
                            v-for="timer in timers"
                            :key="timer.id"
                            :comment="timer.comment"
                            :start="timer.startTime"
                            :end="timer.endTime"
                            :member="timer.member"
                        />
                    </div>
                    <div v-else>
                        <p>{{ $t("emptyTimers") }}</p>
                    </div>
                </div>
            </div>
            <div class="col-0 col-md-4"></div>
        </div>
    </div>
</template>

<style scoped></style>

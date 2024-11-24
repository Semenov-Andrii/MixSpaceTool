<script setup>
import MeetingItem from "@/components/MeetingItem.vue";

defineProps({
    meetings: {
        type: Array,
        required: true
    }
});
</script>
<template>
    <MeetingItem
        v-for="meeting in meetings"
        :key="meeting.id"
        :id="meeting.id"
        :owner-name="meeting.owner.fullname"
        :title="meeting.title"
        :icon="meeting.icon"
    ></MeetingItem>
</template>

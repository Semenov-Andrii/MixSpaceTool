<script setup>
import MeetingItem from "@/components/meeting/MeetingItem.vue";

defineProps({
    meetings: {
        type: Array,
        required: true
    },
    removeMeeting: {
        type: Function,
        required: false,
        default: null
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
        :remove-self="removeMeeting ? () => removeMeeting(meeting) : removeMeeting"
    ></MeetingItem>
</template>

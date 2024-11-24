<script setup>
import { ref } from "vue";
import MeetingList from "@/components/meeting/MeetingList.vue";
import { meetingDeleteApi, meetingListApi, savedMeetingListApi } from "@/js/api/meeting-api";

const ownMeetings = ref([]);
const savedMeeting = ref([]);

meetingListApi().then((res) => {
    ownMeetings.value.push(...res);
});

savedMeetingListApi().then((res) => {
    savedMeeting.value.push(...res);
});

const removeMeeting = (meeting) => {
    meetingDeleteApi(meeting.id).then(() => {
        ownMeetings.value.splice(ownMeetings.value.indexOf(meeting), 1);
        savedMeeting.value.splice(savedMeeting.value.indexOf(meeting), 1);
    });
};
</script>
<template>
    <div>
        <div class="header-row m-4">
            <h3 class="fw-bold mb-3">{{ $t("ownMeetings") }}</h3>
            <RouterLink
                class="btn btn-icon btn-round btn-success"
                :to="{ name: 'new-meeting' }"
                :title="$t('addMeetTitle')"
            >
                <i class="fa-solid fa-plus"></i>
            </RouterLink>
        </div>
        <div class="row">
            <MeetingList :meetings="ownMeetings" :remove-meeting="removeMeeting"></MeetingList>
        </div>
        <div class="row">
            <h3 class="fw-bold mb-3">{{ $t("savedMeetings") }}</h3>
        </div>
        <div class="row">
            <MeetingList :meetings="savedMeeting"></MeetingList>
        </div>
    </div>
</template>
<style>
.meetings-list {
    display: flex;
    flex-direction: column;
    flex-wrap: wrap;
}
</style>

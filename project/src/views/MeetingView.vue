<script setup>
import { ref, onMounted } from "vue";

import { useRoute } from "vue-router";
import { getUser } from "@/js/auth";
import SaveIcon from "@/components/SaveIcon.vue";
import { disconnect, getMediaStream, onAll, toggleMute, toggleVideo } from "@/js/video-client";
import { IMAGES } from "@/js/resources.js";

const { meetingId } = useRoute().params;
const currentUser = getUser();

const microOn = ref(false);
const videoOn = ref(false);
const users = ref({});
const ownId = ref("");

const newUser = (id, jsonUser) => {
    const user = JSON.parse(jsonUser);
    console.log("New user!", user.fullname, user.id);

    const found = Object.keys(users.value).find((key) => users.value[key].data.id === user.id);
    if (found) {
        if (found === ownId.value) {
            ownId.value = id;
            getMediaStream(
                (stream) => {
                    newStream(ownId.value, stream);
                },
                videoOn.value,
                microOn.value
            );
        }
        delete users.value[found];
    }

    users.value[id] = {
        id: id,
        data: user,
        videoOn: false,
        stream: null
    };
};

const newStream = (id, stream) => {
    if (id in users.value) users.value[id].stream = stream;
};

const disconnectSelf = () => {
    delete users.value[ownId.value];
    disconnect();
};
const disconnectUser = (id) => {
    delete users.value[id];
};

onAll(newUser, newStream, disconnectUser, meetingId, JSON.stringify(currentUser));

onMounted(() => {
    getMediaStream(
        (stream) => {
            ownId.value = Object.keys(users.value)[0];
            newStream(ownId.value, stream);
        },
        videoOn.value,
        microOn.value
    );
});

const toggleMicroMute = () => {
    microOn.value = !microOn.value;
    toggleMute();
};

const toggleVideoMute = () => {
    videoOn.value = !videoOn.value;
    users.value[ownId.value].videoOn = videoOn.value;
    toggleVideo();
};
</script>

<template>
    <div>
        <div class="row">
            <div
                v-for="(user, index) in users"
                :key="user.data"
                class="col-12 col-md-6 col-xl-4 video-box"
            >
                <div class="video-container">
                    <video
                        class="video-col"
                        v-if="user.stream"
                        :key="index"
                        :ref="`video-${index}`"
                        :srcObject="user.stream"
                        autoplay
                        muted
                    >
                        Your browser does not support the video tag.
                    </video>
                    <div class="video-avatar" v-if="!user.videoOn">
                        <img
                            :src="IMAGES[user.data.avatar]"
                            alt="image profile"
                            class="avatar-img rounded-circle"
                        />
                    </div>
                    <div class="video-info">
                        <div>{{ user.data.fullname }}</div>
                    </div>
                </div>
            </div>
        </div>

        <div class="bottom-panel">
            <button
                @click="toggleMicroMute"
                :class="'btn btn-rounded ' + (microOn ? 'btn-success' : 'btn-danger')"
            >
                <i :class="microOn ? 'fas fa-microphone' : 'fas fa-microphone-slash'"></i>
            </button>

            <button
                @click="toggleVideoMute"
                :class="'btn btn-rounded ' + (videoOn ? 'btn-success' : 'btn-danger')"
            >
                <i :class="videoOn ? 'fas fa-video' : 'fas fa-video-slash'"></i>
            </button>

            <SaveIcon :meeting-id="meetingId"></SaveIcon>

            <button @click="disconnectSelf" class="btn btn-rounded btn-danger">
                <i class="fa-solid fa-phone-flip"></i>
            </button>
        </div>
    </div>
</template>

<style scoped>
.video-box {
    background-color: black;
    border: 1px solid darkslategrey;
}
.video-container {
    position: relative;
    height: 100%;
    min-height: 40vh;
}
.video-col {
    width: 100%;
}
.video-info {
    position: absolute;
    color: white;
    background-color: black;
    bottom: 2%;
    left: 2%;
}
.video-avatar {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
}

.bottom-panel {
    position: fixed;
    display: flex;
    justify-content: center;
    width: 100vw;
    height: auto;
    background-color: #27262a;
    bottom: 0;
    left: 0;
    padding: 10px;
}
.bottom-panel > * {
    margin: 5px;
}
</style>

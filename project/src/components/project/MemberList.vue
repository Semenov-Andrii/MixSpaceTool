<script setup>
import { ref } from "vue";
import { memberDeleteApi, memberListApi } from "@/js/api/project-api.js";
import NotifyBox from "@/components/modal/NotifyBox.vue";
import LoadingWindow from "@/components/modal/LoadingWindow.vue";
import i18n from "@/i18n/index.js";
import { errorToString, isOwner } from "@/js/utility.js";
import MemberForm from "@/components/project/MemberForm.vue";
import MemberItem from "@/components/project/MemberItem.vue";
import DotsButton from "@/components/DotsButton.vue";

const props = defineProps({
    itemId: {
        type: String,
        required: true
    },
    owner: {
        type: Object
    },
    memberType: {
        type: String,
        required: true
    }
});

const model = defineModel({ required: true, default: false });

const activeLoading = ref(true);

const error = ref({
    active: false,
    title: "",
    message: ""
});

i18n.useT();

const members = ref([]);

memberListApi(props.itemId, props.memberType)
    .then((res) => {
        members.value.push(...res);
    })
    .catch((err) => {
        console.log(err);
        error.value.title = i18n.t("memberListError");
        error.value.message = errorToString(err);
        error.value.active = true;
    })
    .finally(() => {
        activeLoading.value = false;
    });

const active = ref(false);

const addMember = () => {
    active.value = true;
};

const onMemberCreated = (res) => {
    members.value.push(res);
    active.value = false;
};

const onMemberRemove = (memberId) => {
    activeLoading.value = true;

    memberDeleteApi(props.itemId, memberId, props.memberType)
        .then(() => {
            members.value = members.value.filter((item) => item.id !== memberId);
        })
        .catch((err) => {
            console.log(err);
            error.value.title = i18n.t("memberListError");
            error.value.message = errorToString(err);
            error.value.active = true;
        })
        .finally(() => {
            activeLoading.value = false;
        });
};

const close = () => {
    model.value = false;
};
</script>

<template>
    <NotifyBox
        v-model="error.active"
        :message="error.message"
        :title="error.title"
        type="danger"
    ></NotifyBox>
    <LoadingWindow v-if="activeLoading"></LoadingWindow>
    <MemberForm
        v-model="active"
        :on-success="onMemberCreated"
        :item-id="itemId"
        :member-type="memberType"
    />
    <div v-if="model" class="member-window">
        <div class="row">
            <div class="col-0 col-md-4"></div>
            <div class="col-12 col-md-4">
                <div class="member-list">
                    <div class="header-row">
                        <h4>{{ $t("members") }}</h4>
                        <div>
                            <DotsButton v-if="isOwner(owner.id)" theme="dark">
                                <template v-slot:list>
                                    <a class="dropdown-item" href="#" @click="addMember">
                                        {{ $t("addMember") }}
                                    </a>
                                </template>
                            </DotsButton>
                            <button type="button" class="btn-none">
                                <i class="fa-solid fa-xmark list-color" @click="close"></i>
                            </button>
                        </div>
                    </div>

                    <div class="members" id="style-3">
                        <MemberItem
                            v-for="member in members"
                            :key="member"
                            :id="member.id"
                            :fullname="member.fullname"
                            :email="member.email"
                            :position="member.position"
                            :avatar="member.avatar"
                            :remove-member="onMemberRemove"
                            :owner-id="owner?.id"
                        ></MemberItem>
                    </div>
                </div>
            </div>
            <div class="col-0 col-md-4"></div>
        </div>
    </div>
</template>

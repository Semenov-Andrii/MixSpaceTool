<script setup>
import LoginForm from "@/components/LoginForm.vue";
import RegistrationForm from "@/components/RegistrationForm.vue";


</script>
<template>
    <div class="container">
        <div class="row">
            <div class="col-0 col-md-1"></div>
            <div class="col-12 col-md-5">
                <RegistrationForm></RegistrationForm>
            </div>
            <div class="col-12 col-md-5">
                <LoginForm></LoginForm>
            </div>
            <div class="col-0 col-md-1"></div>
        </div>
    </div>

</template>
<script>
import { RouterLink } from 'vue-router';

export default {
    props: ['to'],
    components: { RouterLink },
    computed: {

        localizedUrl() {
            let to = this.to;

            if (to.length > 1 && to.startsWith("/")) to = to.substring(1);
            return to === '/'
                ? `/${this.$i18n.locale}`
                : `/${this.$i18n.locale}/${to}`;
        },
    },
};
</script>
<template>
    <RouterLink :to="localizedUrl">
        <slot></slot>
    </RouterLink>
</template>
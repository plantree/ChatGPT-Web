<template>
    <div class="chat sticky top-[88vh] bg-white">
        <form class="flex items-center justify-center gap-x-6">
            <input v-model="text" type="text"  class="w-3/4 md:w-1/2 outline-none h-[2.6rem] px-5 bg-gray-100 rounded-lg focus:bg-gray-200 focus:shadow-[0_0_1.5rem_var(--tw-shadow-color)]">
            <button class="text-gray-200 hover:text-gray-100 bg-main/75 hover:bg-main border-transparen hover:bg-main-200 font-bold text-sm"
                :disabled="text === ''" @click="submit">发送</button>
        </form>
    </div>
</template>

<script lang="ts">
export default {
    data: () => ({
        text: ''
    }),
    methods: {
        submit(event) {
            this.$emit('submit', event, this.text)
            this.text = ''
        }
    }
}

</script>

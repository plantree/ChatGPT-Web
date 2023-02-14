<template>
    <main class="text-left">
        <h1 class="py-20 text-center text-3xl font-bold">开始和ChatGPT交流吧！</h1>
        <div class="py-12 md:py-16">
            <form  class="flex flex-col items-center justify-center gap-y-6 md:flex-row md:gap-x-5">
                <input v-model="name" type="text" name="username" placeholder="你的名字" 
                    class="outline-none h-[2.6rem] px-5 bg-gray-100 rounded-lg text-center focus:bg-gray-200 focus:shadow-[0_0_1.5rem_var(--tw-shadow-color)]">
                <button class="text-gray-200 hover:text-gray-100 bg-main/75 hover:bg-main border-transparen hover:bg-main-200 font-bold" 
                    :disabled="name === ''"
                    @click="$emit('submit', $event, name)">开始!</button>
            </form>
        </div>
    </main>
</template>

<script lang="ts">
export default {
    data: () => (
        {
            name: ''
        }
    )
}
</script>
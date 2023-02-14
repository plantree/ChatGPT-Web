<template>
    <div class="message">
        <div v-if="left" class="flex gap-x-2 my-4">
            <span class="text-main font-bold">{{ author }}</span>
        <p class="leading-7 bg-gray-200 rounded-lg p-4 min-h-2 md:max-w-[75%] text-left">{{ text }}</p>
        </div>
        <div v-else class="flex gap-x-2  justify-end">
            <p class="leading-7 bg-main text-white rounded-lg p-4 min-h-2 md:max-w-[75%] text-left">{{ text }}</p>
            <span class="text-main font-bold">{{ author }}</span>
        </div>
    </div>
</template>

<script lang="ts">
export default {
    props: [
        'text',
        'author',
        'left'
    ]
}
</script>

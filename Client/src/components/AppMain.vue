<script setup lang="ts">
import LoginDialog from './LoginDialog.vue'
import Message from './Message.vue'
import ChatBox from './ChatBox.vue'
</script>

<template>
    <div class="messages md:px-20 px-2 h-[36rem] overflow-auto scroll-mx-0" v-if="user" ref="scrollDiv">
        <Message v-for="message in messages" :key="message.id" :text="message.text" :left="isLeft(message)"
            :author="message.author" />
    </div>
    <ChatBox v-if="user" @submit="onSubmit" />
    <LoginDialog v-if="!user" @submit="onRegister" />
</template>

<script lang="ts">
import axios from 'axios'

export default {
    data: () => ({
        user: null,
        messages: [
            {
                text: '欢迎和ChatGPT交流!欢迎和ChatGPT交流!欢迎和ChatGPT交流!欢迎和ChatGPT交流!欢迎和ChatGPT交流!欢迎和ChatGPT交流!',
                author: 'ChatGPT'
            }
        ],
        allowSend: true
    }),
    updated: function () {
        this.scrollToBottom()
    },
    methods: {
        isLeft(message) {
            return message.author === 'ChatGPT'
        },
        scrollToBottom() {
            this.$nextTick(() => {
                let scrollElem = this.$refs.scrollDiv
                if (scrollElem !== null) {
                    scrollElem.scrollTo({ top: scrollElem.scrollHeight, behavior: 'smooth' })
                }
            });
        },
        async onRegister(event, name) {
            event.preventDefault();
            // login
            const server = this.$store.state.server
            const request_url = `${server}/api/chatgpt/login?token=${name}`
            try {
                const ret = await axios.post(request_url)
                if (ret.status === 200 && ret.data.code === 0) {
                    this.user = {
                        'name': name
                    }
                } 
            } catch (ex) {
                console.log(ex)
            }
        },
        async onSubmit(event, text) {
            event.preventDefault()
            if (!this.allowSend) {
                return
            }
            this.allowSend = false
            // guard area
            this.messages.push({
                text: text,
                author: this.user.name
            })
            this.messages.push({
                text: '正在输入中...',
                author: 'ChatGPT'
            })
            // request chatgpt
            const server = this.$store.state.server
            const request_url = `${server}/api/chatgpt/ask?prompt=${text}&token=${this.user.name}`
            try {
                            const ret = await axios.post(request_url)
            if (ret.status === 200 && ret.data.code === 0) {
                this.messages[this.messages.length - 1].text = ret.data.msg
            } else {
                this.messages[this.messages.length - 1].text = '遇到一个错误, 请刷新后重试'
            }
            } catch (ex) {
                console.log(ex)
                this.messages[this.messages.length - 1].text = '遇到一个错误, 请刷新后重试'
            }
            this.allowSend = true
        }
    }
}
</script>

<style scoped>
/* Works on Firefox */
* {
    scrollbar-width: thin;
    scrollbar-color: gray white;
}

/* Works on Chrome, Edge, and Safari */
*::-webkit-scrollbar {
    width: 5px;
}

*::-webkit-scrollbar-track {
    background: white;
}

*::-webkit-scrollbar-thumb {
    background-color: white;
    border-radius: 20px;
    border: 3px solid gray;
}
</style>
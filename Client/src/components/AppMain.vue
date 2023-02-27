<script setup lang="ts">
import LoginDialog from './LoginDialog.vue'
import Message from './Message.vue'
import ChatBox from './ChatBox.vue'
import jsMd5 from 'https://cdn.jsdelivr.net/npm/js-md5@0.7.3/+esm'
</script>

<template>
    <div class="messages md:px-20 px-2 h-[34rem] overflow-auto scroll-mx-0" v-if="user" ref="scrollDiv">
        <Message v-for="message in messages" :key="message.id" :text="message.text" :left="isLeft(message)"
            :author="message.author" />
        <div style="display: flex; flex-flow: row wrap; justify-content:center;" v-if="loading">
            <Spin />
        </div>
    </div>
    <ChatBox v-if="user" @submit="onSubmit" />
    <LoginDialog v-if="!user" @submit="onRegister" :showLoginStatus="showLoginStatus"/>
</template>

<script lang="ts">
import axios from 'axios'
import { Fireworks } from 'fireworks-js'
import Spin from './Spin.vue'

function generateToken(str: string, salt: string) {
    return jsMd5(str + salt)
}

export default {
    data: () => ({
        user: null,
        messages: [
            {
                text: '欢迎和ChatGPT交流!',
                author: 'ChatGPT'
            }
        ],
        allowSend: true,
        fireworks: null,
        showLoginStatus: false,
        loading : false //true为加载中，默认为false
    }),
    updated: function () {
        this.scrollToBottom()
        const container = document.querySelector('div.messages')
        if (container !== null && this.fireworks === null) {
            this.fireworks = new Fireworks(container)
        }
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
            const token = generateToken(name, import.meta.env.VITE_SALT)
            const request_url = `${server}/api/chatgpt/login?token=${token}`
            try {
                const ret = await axios.post(request_url)
                if (ret.status === 200 && ret.data.code === 0) {
                    this.user = {
                        'name': name,
                        'token': token
                    }
                    this.showLoginStatus = false
                    return
                }
            } catch (ex) {
                console.log(ex)
            }
            this.showLoginStatus = true
        },
        async onSubmit(event, text) {
            event.preventDefault()
            if (!this.allowSend) {
                return
            }
            this.allowSend = false
            this.loading = true //加载中
            // guard area
            this.messages.push({
                text: text,
                author: this.user.name
            })
            if (text === '我爱你') {
                this.messages.push({
                    text: '我也爱你💖',
                    author: 'ChatGPT'
                })
                this.fireworks.start()
                this.allowSend = true
                return
            }
            this.fireworks.stop()
            this.messages.push({
                text: '正在输入中...',
                author: 'ChatGPT'
            })
            // request chatgpt
            const server = this.$store.state.server
            const request_url = `${server}/api/chatgpt/ask?prompt=${text}&token=${this.user.token}`
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
            this.loading = false //加载完成
            this.allowSend = true
        }
    }
}
</script>

<style>
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

:root {
  --fk-color-primary: #646cff;
  --vf-success-lighter: #dcfce7;
  --vf-color-success: #22c55e;
  --vf-danger-lighter: #fee2e2;
  --vf-color-danger: #ef4444;
  --fk-max-width-input: 40em;
}
.form-bg-success {
  background-color: var(--vf-success-lighter);
}
.form-color-success {
  color: var(--vf-color-success);
}
.form-bg-danger {
  background-color: var(--vf-danger-lighter);
}
.form-color-danger {
  color: var(--vf-color-danger);
}


</style>

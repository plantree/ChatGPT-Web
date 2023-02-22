# ChatGPT-Web
<p align="left">
<a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-green.svg"></a>
</p>

A web client for ChatGPT based on official API.

#### 0. Background

As we all know, [ChatGPT](https://openai.com/blog/chatgpt/) is very popular now, and so many tools has been developed, such as:

- Desktop application
- Chrome Extension
- Visual Studio Code Extension
- Chat Bots
- etc

However, we have found that, they are still a bit complex for people to interact with ChatGPT and feel the wonderful experience brought by technology. 

We thought the Web might be the best choice to help people use ChatGPT more conveniently because of its accessibility and simple interaction, and that's why we decide to develop this web client.

#### 1. Goals

- Easy to interact
- Easy to deploy independently

#### 2. Features

- [x] Use token and CORS to access (limit malicious access)
- [x] Limit access frequency (the API of ChatGPT has limitations)
- [ ] RESTful API and easy to adjust request parameters

#### 3. How to use

The whole project has been divided into two parts:

- Client
- Server

which could be deployed independently, and the easiest way to do this is by using Vercel and Docker.

- Vercel: using vercel to deploy the Client (free, simple enough and do not need extra machine)
- Docker: using docker to deploy the server, because too long timeout is not allowed by vercel (limits 10 seconds)

##### 3.1 Deploy

- Deploy client: [![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/plantree/ChatGPT-Web/tree/main/Client)

- Deploy Server:

  ```bash
  $ git clone https://github.com/plantree/ChatGPT-Web.git && cd Server
  # change config.yml
  $ docker build -t chat-server .
  # export port
  $ docker run -it -p 8000:8000 --name chat-server chat-server
  ```

##### 3.2 Config

- Client

  ```javascript
  // Client/.env
  VITE_SERVER=http://127.0.0.1:8000
  ```
  
- Server

  ```yaml
  # Server/config.yml
  # export port
  port: 8000
  max_retry: 3
  timeout: 20
  # CORS
  use_cors: false
  origins: 
    - 'http://localhost:*'
    - 'https://localhost:*'
  # limit of per minute
  limit: 10
  # encryption obfuscation (not use recently)
  salt: chatgpt
  # for login
  tokens: 
    - test
  # api key (random select)
  keys:
    - sk-xxxx
  ```

#### 4. Technology inside

- Front-end
  - Vue
  - Vite
- Back-end
  - Flask

#### Changelogs

##### v0.9.1(2023.02.22)



##### v0.9.0 (2023.02.14)

###### Feature

1. Server: request `api.openai` with retry and timeout, add CORS and query limitation for protecting
2. Client: login and chat with server upon token

#### Reference

1. https://openai.com/api/
1. https://openai.com/api/pricing/


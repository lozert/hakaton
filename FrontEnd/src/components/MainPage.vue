<template>
  <div class="main">
    <div class="panel">
      <p style="font-size: 60px;">LocAI</p>
      <p>История запросов:</p>
      <div class="history">
        <a v-for="h in this.history" :key="h.history_id" href="#" :class="[ h.history_id == this.selected ? 'active' : '']" class="button" @click="loadHistoryElement(h.history_id)">{{ h.user_prompt }} <img src="../assets/Arrow.svg" v-if="h.history_id == this.selected"></a>
      </div>
      <a href="#" class="button add" @click="createPrompt"><img src="../assets/Plus.svg"></a>
    </div>
    <div class="content">
      <div class="wrap" v-if="selected == -1">
        <textarea v-model="this.newPrompt.user_prompt"></textarea>
        <button @click="this.sendPrompt" class="btn" v-if="this.showButton">Отправить запрос</button>
      </div>
      <div class="wrap" v-if="selected != -1">
        <h4>Ваш запрос:</h4>
        <p class="read">{{ this.historyElement.user_prompt }}</p>
        <h4>Ответ:</h4>
        <p class="read" v-html="this.historyElement.ai_answer.replaceAll('\\n', '<br/>')"></p>
      </div>
    </div>
  </div>
</template>

<script>
import * as Api from '../assets/Api.js'

export default {
  name: 'MainPage',
  data() {
    return {
      history: this.history = Api.getHistoryList(),

      showButton: true,
      historyElement: {
        user_prompt: "",
        ai_answer: ""
      },
      newPrompt: {
        user_prompt: ""
      },
      popout: false,
      selected: -1,
    }
  },
  methods: {
    loadHistoryElement(id){
      this.historyElement = Api.getHistoryElement(id)
      this.selected = id
    },
    createPrompt(){
      this.selected = -1
      this.showButton = true
      this.newPrompt.user_prompt=""
    },
    sendPrompt(){
      this.showButton = false
      Api.sendPrompt({
        role: 'user',
        text: this.newPrompt.user_prompt
      }).then(() => {
        this.history = Api.getHistoryList();
        this.selected = this.history.length -1
        this.historyElement = Api.getHistoryElement(this.selected)
      })
    },
  }
}
</script>

<style scoped>
.main {
  display: grid;
  width: 100dvw;
  height: 100dvh;
  grid-template-columns: 350px auto;
}

.main .panel {
  display: flex;
  flex-direction: column;
  margin: 15px 27px;
  padding: 17px;
  border-radius: 10px;
  background-color: #031617;
  color: #F5F5F5;
  height: 96vh;
}
.main a.button{
  background-color: #162a35;
  display: flex;
  justify-content: space-between;
  color: #888888;
  padding: 13px;
  border-radius: 10px;
  text-decoration: none;
  margin: 20px 0;
}
.main a.button:hover{
  text-decoration: underline;
}
.main a.button.active{
  background-color: #2A4F62;
  color: #F5F5F5;
}
.main a.button.add{
  background-color: #0E8C93;
  color: #ffffff;
  height: 50px;
  margin: 0;
  justify-content: center;
}
.popout{
  width: 100dvw;
  height: 100dvh;
  display: grid;
  justify-content: center;
  position: absolute;
  left: 0;
  top: 0;
}
.history{
  overflow-y: scroll;
  height: 75%;
}
.history::-webkit-scrollbar, .content::-webkit-scrollbar {
  display: none;
}
.content{
  overflow-y: scroll;
}
.content .wrap{
  padding: 20px;
  width: calc(100%-60px);
  height: calc(100%-60px);
}
.content textarea{
  display: block;
  width: 100%;
  color: white;
  border-radius: 10px;
  min-height: 600px;
  height: fit-content;
  background-color: rgb(72, 72, 72);
  overflow: visible;
  margin-bottom: 20px;
}
h4{
  color: white
}
p.read{
  color: white
}
</style>
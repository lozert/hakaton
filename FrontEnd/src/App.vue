<template>
  <MainPage @display="displaySwitch" v-if="display.main"/>
  <AuthPage @display="displaySwitch" v-if="display.auth"/>
  <RegPage @display="displaySwitch" v-if="display.reg"/>
  
</template>

<script>
import MainPage from './components/MainPage.vue';
import AuthPage from './components/AuthPage.vue';
import RegPage from './components/RegPage.vue';

export default {
  name: 'App',
  components: {
    MainPage,
    AuthPage,
    RegPage
  },
  methods: {
    displaySwitch(value){
      switch (value) {
        case 0:
          this.display.main = true;
          this.display.auth = false;
          this.display.reg = false;
          break;
        case 1:
          this.display.main = false;
          this.display.auth = true;
          this.display.reg = false;
          
          break;
        case 2:
          this.display.main = false;
          this.display.auth = false;
          this.display.reg = true;
      
          break;
      }
    }
  },
  data(){
    return {
      display: {
        main: false,
        auth: true,
        reg: false
      }
    }
  },
  beforeMount(){
    // тут можно проверить вошел человек или нет (через LocalStorage хранить токен какой нибудь) и потом устанавливать переменные отображения
    if(localStorage.getItem('history') == null) localStorage.setItem('history', JSON.stringify([]))
  }
}
</script>

<style>
  @import url(./assets/bootstrap.css);
  
  #app{
    background-color: #082D33;
  }
  .auth, .reg{
    display: grid;
    place-items: center;
    height: 100dvh;
  }
  .form{
    width: 700px;
    height: fit-content;
    border-radius: 10px;
    background-color: #031617;
    padding: 30px 50px;
    color: white;
  }
  .form-floating{
    margin-bottom: 20px;
  }
  input::placeholder{
    color: #082D33;
  }
  a{
    cursor: pointer;
  }
</style>

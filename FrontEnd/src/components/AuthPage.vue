<template>
  <div class="auth">
      <div class="form">
        <h1 class="h3 mb-3 fw-normal">Пожалуйста, войдите в систему</h1>

        <div class="form-floating">
          <input type="email" class="form-control" v-model="this.email" id="floatingInput" placeholder="name@example.com">
          <label for="floatingInput">Е-mail</label>
        </div>
        <div class="form-floating">
          <input type="password" class="form-control" v-model="this.password" id="floatingPassword" placeholder="Password">
          <label for="floatingPassword">Пароль</label>
        </div>

        <div class="form-floating">
          <a @click="this.$emit('display', 2)" class="icon-link">Зарегистрироваться ></a>
        </div>

        <button class="btn btn-primary w-100 py-2" @click="submit">Войти</button>
      </div>
  </div>
</template>

<script>
import * as Api from '../assets/Api.js'

export default {
  name: 'AuthPage',
  data() {
    return{
      email: '',
      password: ''
    }
  },
  methods: {
    submit() {
      if(Api.authUser(this.email, this.password) != -1){
        //переброс на главную после авторизации
        this.$emit('display', 0)
      }
    }
  },
}
</script>

<style scoped>
</style>
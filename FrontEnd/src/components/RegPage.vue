<template>
    <div class="reg">
      <div class="form">
        <h1 class="h3 mb-3 fw-normal">Для пользования системой, зарегистрируйтесь</h1>

        <div class="form-floating">
          <input type="email" class="form-control" v-model="this.email" id="floatingRegEmail" placeholder="name@example.com">
          <label for="floatingRegEmail">Е-mail</label>
        </div>
        <div class="form-floating">
          <input type="password" class="form-control" v-model="this.password1" id="floatingRegPassword1" placeholder="Password">
          <label for="floatingRegPassword1">Пароль</label>
        </div>
        <div class="form-floating">
          <input type="password" class="form-control" v-model="this.password2" id="floatingRegPassword2" placeholder="Password">
          <label for="floatingRegPassword2">Повтор пароля</label>
        </div>

        <div class="form-floating">
          Уже есть аккаунт? <a @click="this.$emit('display', 1)" class="icon-link">Войти ></a>
        </div>

        <button class="btn btn-primary w-100 py-2" @click="submit">Зарегистрироваться</button>
      </div>
    </div>
</template>
  
<script>
import * as Api from '../assets/Api.js'

export default {
  name: 'RegPage',
  data () {
    return {
      email: "",
      password1: "",
      password2: ""
    }
  },
  methods: {
    submit(){
      if(this.password1 == this.password2){

        if(Api.authUser(this.email, this.password)){
          //Когда прошла регистрация переброс на auth
          this.$emit('display', 1)
          this.email = ""
          this.password1 = ""
          this.password2 = ""
        }
      }
    }
  }
}
</script>
  
<style scoped>

</style>
  
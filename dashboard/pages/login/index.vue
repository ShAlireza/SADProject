<template>
  <v-container style="height: 80%" class="d-flex align-center">
    <div
      class="green"
      style="
        position: absolute;
        left: 0;
        top: 48px;
        right: 50%;
        height: 100%;
        opacity: 0.5;
      "
    ></div>
    <v-card
      style="background-color: #f8f7f9; min-width: 360px"
      class="mx-auto mt-10"
      max-width="500px"
    >
      <v-card-title class="mx-auto mb-4 justify-center">
        <div
          class="white px-8 py-2 rounded-lg elevation-2"
          style="margin-top: -2rem; width: 90%; text-align: center"
        >
          Login
        </div>
      </v-card-title>
      <v-card-text>
        <v-text-field
          v-model="username"
          prepend-inner-icon="mdi-account"
          solo
          flat
          placeholder="user name"
        >
        </v-text-field>
        <v-text-field
          v-model="password"
          prepend-inner-icon="mdi-lock"
          solo
          flat
          placeholder="password"
          type="password"
        >
        </v-text-field>
      </v-card-text>
      <v-card-text class="py-0">
        <v-btn block class="primary white--text" @click="login">
          <template v-if="isLoading">
            <v-progress-circular
              indeterminate
              :size="20"
              :width="2"
            ></v-progress-circular>
          </template>
          <template v-if="!isLoading">LOGIN</template>
        </v-btn>
      </v-card-text>
      <v-card-subtitle width="340px" class="d-flex justify-center">
        If you havent signed up yet, click
        <nuxt-link to="register" class="px-1"> here </nuxt-link>
        to sign up.
      </v-card-subtitle>
    </v-card>
  </v-container>
</template>

<script>
export default {
  name: 'LoginPage',
  data() {
    return {
      isLoading: false,
      username: '',
      password: '',
    }
  },
  methods: {
    async login() {
      if (!this.username || !this.password) return
      this.isLoading = true
      const { key } = await this.$store.dispatch('auth/login', {
        username: this.username,
        password: this.password,
      })
      localStorage.setItem('ATAccessToken', key)
      localStorage.setItem(
        'ATUserData',
        JSON.stringify({ username: this.username })
      )
      this.isLoading = false
      this.$router.push('/profile')
    },
  },
}
</script>

<style scoped></style>

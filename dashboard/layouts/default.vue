<template>
  <v-app>
    <v-main>
      <v-toolbar v-if="isLoggedIn" dense>
        <v-toolbar-title>
          <v-img src="/logo.svg" alt="logo" contain height="45px"> </v-img>
        </v-toolbar-title>
        <v-btn link to="/" tile plain> Home </v-btn>
        <v-btn link to="/tours" tile plain> Tours </v-btn>
        <v-btn link to="/mytours" tile plain> My Tours </v-btn>
        <v-spacer></v-spacer>

        <v-menu offset-y>
          <template #activator="{ on, attrs }">
            <v-btn tile plain color="primary" v-bind="attrs" v-on="on">
              <span style="margin-right: 10px; text-transform: none">{{
                userInfo.username
              }}</span>
              <v-icon>mdi-account</v-icon>
            </v-btn>
          </template>
          <v-list>
            <v-list-item link to="/profile">
              <v-list-item-title>Profile</v-list-item-title>
            </v-list-item>
            <v-list-item @click="logout">
              <v-list-item-title>Logout</v-list-item-title>
            </v-list-item>
          </v-list>
        </v-menu>
      </v-toolbar>
      <v-toolbar v-if="!isLoggedIn" dense>
        <v-toolbar-title>
          <v-img src="/logo.svg" alt="logo" contain height="45px"> </v-img>
        </v-toolbar-title>
        <v-btn link to="/" tile plain> Home </v-btn>
        <v-btn link to="/tours" tile plain> Tours </v-btn>
        <v-spacer></v-spacer>
        <v-btn link to="/register" tile plain color="primary"> Register </v-btn>
        <v-btn link to="/login" tile outlined color="primary" class="ma-2">
          Login
        </v-btn>
      </v-toolbar>
      <Nuxt />
    </v-main>
  </v-app>
</template>

<script>
export default {
  name: 'DefaultLayout',
  data() {
    return {
      isLoggedIn: false,
      userInfo: { username: 'Profile' },
    }
  },
  mounted() {
    this.getUserToken()
    this.getUserData()
  },
  methods: {
    getUserToken() {
      const lsToken = localStorage.getItem('ATAccessToken')
      if (!lsToken) {
        this.isLoggedIn = false
      } else {
        this.isLoggedIn = true
      }
    },
    getUserData() {
      const lsUserInfo = localStorage.getItem('ATUserData')
      if (!lsUserInfo) return
      const userInfo = JSON.parse(lsUserInfo)
      this.userInfo.username = userInfo.username || 'Profile'
    },
    logout() {
      localStorage.removeItem('ATAccessToken')
      localStorage.removeItem('ATUserData')
      this.isLoggedIn = false
      this.$router.push('/')
    },
  },
}
</script>

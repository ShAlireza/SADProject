export const actions = {
  async register({ state }, { email, username, password }) {
    const body = { username, email, password }
    const res = await this.$axios.post(`/accounts/user`, body)
    return res.data
  },
  async createProfile({ state }, body) {
    const token = localStorage.getItem('ATAccessToken')
    if (!token) return
    const res = await this.$axios.post(`/accounts/user/profile/normal`, body, {
      headers: {
        Authorization: 'Bearer ' + token,
      },
    })
    return res.data
  },
  async login({ state }, { username, password }) {
    const body = { username, password }
    const res = await this.$axios.post(`/accounts/user/auth`, body)
    return res.data
  },
}

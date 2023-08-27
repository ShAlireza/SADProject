export const actions = {
  async getUser({ state }) {
    const token = localStorage.getItem('ATAccessToken')
    if (!token) return
    const res = await this.$axios.get(`/accounts/user`, {
      headers: {
        Authorization: 'Bearer ' + token,
      },
    })
    return res.data
  },
  async updateUser({ state }, data) {
    const token = localStorage.getItem('ATAccessToken')
    if (!token) return
    const res = await this.$axios.patch(`/accounts/user`, data, {
      headers: {
        Authorization: 'Bearer ' + token,
      },
    })
    return res.data
  },
  async getNormalProfile({ state }) {
    const token = localStorage.getItem('ATAccessToken')
    if (!token) return
    const res = await this.$axios.get(`/accounts/user/profile/normal`, {
      headers: {
        Authorization: 'Bearer ' + token,
      },
    })
    return res.data
  },
  async updateNormalProfile({ state }, data) {
    const token = localStorage.getItem('ATAccessToken')
    if (!token) return
    const res = await this.$axios.patch(`/accounts/user/profile/normal`, data, {
      headers: {
        Authorization: 'Bearer ' + token,
      },
    })
    return res.data
  },
  async getOrgProfile({ state }) {
    const token = localStorage.getItem('ATAccessToken')
    if (!token) return
    const res = await this.$axios.get(`/accounts/user/profile/organization`, {
      headers: {
        Authorization: 'Bearer ' + token,
      },
    })
    return res.data
  },
  async createOrgProfile({ state }, body) {
    const token = localStorage.getItem('ATAccessToken')
    if (!token) return
    const res = await this.$axios.post(
      `/accounts/user/profile/organization`,
      body,
      {
        headers: {
          Authorization: 'Bearer ' + token,
        },
      }
    )
    return res.data
  },
  async updateOrgProfile({ state }, data) {
    const token = localStorage.getItem('ATAccessToken')
    if (!token) return
    const res = await this.$axios.patch(
      `/accounts/user/profile/organization`,
      data,
      {
        headers: {
          Authorization: 'Bearer ' + token,
        },
      }
    )
    return res.data
  },
  async getLeaderProfile({ state }) {
    const token = localStorage.getItem('ATAccessToken')
    if (!token) return
    const res = await this.$axios.get(`/accounts/user/profile/leader`, {
      headers: {
        Authorization: 'Bearer ' + token,
      },
    })
    return res.data
  },
  async createLeaderProfile({ state }, body) {
    const token = localStorage.getItem('ATAccessToken')
    if (!token) return
    const res = await this.$axios.post(`/accounts/user/profile/leader`, body, {
      headers: {
        Authorization: 'Bearer ' + token,
      },
    })
    return res.data
  },
  async updateLeaderProfile({ state }, data) {
    const token = localStorage.getItem('ATAccessToken')
    if (!token) return
    const res = await this.$axios.patch(`/accounts/user/profile/leader`, data, {
      headers: {
        Authorization: 'Bearer ' + token,
      },
    })
    return res.data
  },
}

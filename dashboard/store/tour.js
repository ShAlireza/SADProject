export const actions = {
  async getTours({ state }, filter) {
    const queryParam = Object.keys(filter)
      .filter((f) => !!filter[f])
      .map((f) => `${f}=${filter[f]}`)
      .join('&')
    const res = await this.$axios.get(
      `/tour/tour/` + (queryParam ? `?${queryParam}` : '')
    )
    return res.data
  },
  async getTourById({ state }, id) {
    const res = await this.$axios.get(`/tour/tour/${id}`)
    return res.data
  },
  async getTourTags({ state }, id) {
    const res = await this.$axios.get(`/tour/tour/${id}/tags`)
    return res.data
  },
  async getRecom({ state }) {
    const token = localStorage.getItem('ATAccessToken')
    if (!token) return
    const res = await this.$axios.get(`/recom`, {
      headers: {
        Authorization: 'Bearer ' + token,
      },
    })
    return res.data
  },
  async getTourComments({ state }, id) {
    const res = await this.$axios.get(`/tour/tour/${id}/comments`)
    return res.data
  },
  async addComment({ state }, { id, msg }) {
    const token = localStorage.getItem('ATAccessToken')
    if (!token) return
    const res = await this.$axios.post(
      `/tour/comment/${id}`,
      { body: msg },
      {
        headers: {
          Authorization: 'Bearer ' + token,
        },
      }
    )
    return res.data
  },
  async reserveTourById({ state }, data) {
    const token = localStorage.getItem('ATAccessToken')
    if (!token) return
    const body = data
    const res = await this.$axios.post(`/cart/reserve`, body, {
      headers: {
        Authorization: 'Bearer ' + token,
      },
    })
    return res.data
  },
  async redirectToPayment({ state }, id) {
    const token = localStorage.getItem('ATAccessToken')
    if (!token) return
    const res = await this.$axios.get(`/payment/bills/${id}`, {
      headers: {
        Authorization: 'Bearer ' + token,
      },
    })
    return res.data
  },
  async getBills({ state }, id) {
    const token = localStorage.getItem('ATAccessToken')
    if (!token) return
    const res = await this.$axios.get(`/payment/bills`, {
      headers: {
        Authorization: 'Bearer ' + token,
      },
    })
    return res.data
  },
  async createTour({ state }, data) {
    const token = localStorage.getItem('ATAccessToken')
    if (!token) return
    const res = await this.$axios.post(`/tour/tour/new`, data, {
      headers: {
        Authorization: 'Bearer ' + token,
      },
    })
    return res.data
  },
  async addTagToTour({ state }, data) {
    const token = localStorage.getItem('ATAccessToken')
    if (!token || !data.tagId) return
    const res = await this.$axios.post(
      `/tour/tour/${data.tourId}/add_tag/${data.tagId}`,
      null,
      {
        headers: {
          Authorization: 'Bearer ' + token,
        },
      }
    )
    return res.data
  },
}

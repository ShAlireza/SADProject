export const actions = {
  async uploadTourFile({ state }, { file }) {
    const formData = new FormData()
    formData.append('file', file)
    const res = await this.$axios.post(`/file/upload/tour`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    return res.data
  },
}

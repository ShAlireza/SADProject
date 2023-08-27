<template>
  <v-container class="mx-auto d-flex justify-content-start flex-wrap">
    <template v-if="isLoading">
      <v-sheet
        v-for="i in 4"
        :key="i"
        color="grey lighten-4"
        class="pa-3"
        width="280"
        max-width="100%"
      >
        <v-skeleton-loader class="mx-auto" type="card"></v-skeleton-loader>
      </v-sheet>
    </template>
    <template v-else>
      <v-row class="px-2" justify="center">
        <v-col class="pa-0" cols="12" sm="6" md="4" lg="3">
          <v-card
            v-if="userType === 'organization'"
            class="mx-3 my-12"
            width="250"
            height="340"
            link
            :to="`/tour/create`"
            style="position: relative"
          >
            <div
              style="
                width: 100%;
                height: 100%;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                background-color: #e2e2e2;
              "
            >
              <div style="font-size: 90px; font-weight: 300; color: #929292">
                +
              </div>
              <div>Add tour</div>
            </div>
          </v-card>
        </v-col>
        <v-col
          v-for="(t, i) in tours"
          :key="i"
          class="pa-0"
          cols="12"
          sm="6"
          md="4"
          lg="3"
        >
          <tour-view :t="t"></tour-view>
        </v-col>
      </v-row>
    </template>
  </v-container>
</template>

<script>
export default {
  name: 'MyToursPage',
  data: () => ({
    isLoading: true,
    tours: [],
    userType: 'normal',
  }),
  created() {
    if (typeof window === 'undefined') return
    this.getTours()
  },
  methods: {
    async getTours() {
      const user = await this.$store.dispatch('account/getUser')
      this.userType = user.type
      let res
      if (user.type === 'normal') {
        res = []
        const bills = await this.$store.dispatch('tour/getBills')
        const tourIds = bills.map((b) => b.tour_id)
        tourIds.forEach(async (tid) => {
          const product = await this.$store.dispatch('tour/getTourById', tid)
          res.push(product)
        })
      } else if (user.type === 'organization') {
        res = await this.$store.dispatch('tour/getTours', { owner: user.id })
      } else if (user.type === 'leader') {
        res = await this.$store.dispatch('tour/getTours', { leader: user.id })
      }
      this.tours = res
      this.isLoading = false
    },
  },
}
</script>

<style>
.back {
  position: absolute;
  opacity: 0.5;
  top: 48px;
  right: 0;
  left: 0;
  bottom: calc(50% - 48px);
  width: 100%;
}
.datepicker-btn {
  width: 100% !important;
  height: 48px !important;
  padding: 0 20px !important;
  background-color: white !important;
}
</style>

<template>
  <v-container v-if="tour" class="pt-15">
    <v-row>
      <v-col>
        <template>
          <v-row>
            <v-col>
              <h2 class="mb-2">{{ tour.name }}</h2>
              <div>
                <span class="mr-2">
                  From <u>{{ tour.src }}</u> to <u>{{ tour.dst }}</u></span
                >
                <span class="mr-2">.</span>
                <span>{{ comments.length }} comment</span>
              </div>
            </v-col>
          </v-row>
          <v-row class="mt-10">
            <v-img
              :contain="false"
              max-width="50%"
              :src="
                tour.image_url ||
                'https://minio.alantouring.ir/tour/838fb2dd-1214-4499-9bef-cf5bf5808ce6'
              "
              style="
                border: solid 1px #00000030;
                border-radius: 8px;
                overflow: hidden;
              "
            ></v-img>
          </v-row>

          <v-row class="mt-10">
            <v-col class="col">
              <v-row>
                <v-col class="data">
                  <v-icon>mdi-calendar</v-icon>
                  <span>Timeline</span>
                  <span class="data-value">{{ dateRangeText }}</span>
                </v-col>
              </v-row>
              <v-row>
                <v-col class="data">
                  <v-icon>mdi-hard-hat</v-icon>
                  <span>Difficulty level</span>
                  <span class="data-value">
                    <v-rating
                      empty-icon="mdi-checkbox-blank-circle-outline"
                      full-icon="mdi-checkbox-blank-circle"
                      background-color="grey-700 lighten-2"
                      color="grey-700"
                      size="15"
                      length="3"
                      :value="tour.difficulty"
                      readonly
                      style="width: fit-content"
                    ></v-rating>
                  </span>
                </v-col>
              </v-row>
              <v-row>
                <v-col class="data">
                  <v-icon>mdi-currency-rial</v-icon>
                  <span>Price</span>
                  <span class="data-value"> {{ tour.price }} IRR </span>
                </v-col>
              </v-row>
              <v-row>
                <v-col class="data">
                  <v-icon>mdi-human-capacity-increase</v-icon>
                  <span> Capacity </span>
                  <span class="data-value">
                    {{ tour.capacity }}
                  </span>
                </v-col>
              </v-row>
              <v-row v-if="tags.length">
                <v-col class="data">
                  <v-icon>mdi-tag-outline</v-icon>
                  <span>Tags</span>
                  <span class="data-value">
                    <v-chip-group>
                      <v-chip v-for="(t, i) in tags" :key="i">
                        {{ t }}
                      </v-chip>
                    </v-chip-group>
                  </span>
                </v-col>
              </v-row>
              <v-row v-if="tour.description">
                <v-col>
                  <div>Description</div>
                  <b>{{ tour.description }}</b>
                </v-col>
              </v-row>
            </v-col>
          </v-row>
        </template>
      </v-col>
      <v-col>
        <v-row v-if="isLoggedIn && tour">
          <v-card elevation="2" width="100%" style="margin-top: 20px">
            <div
              class="d-flex flex-column justify-content-center"
              style="padding: 20px"
            >
              <h3 class="mb-5">Reserve tour {{ tour.name }}</h3>
              <p>{{ tour.price }} IRR</p>
              <p>There is {{ tour.capacity }} more left!</p>
              <v-btn
                :disabled="!tour.capacity"
                class="mt-5 px-10"
                color="primary"
                large
                @click="reserveTour"
              >
                <template v-if="reserveLoader">
                  <v-progress-circular
                    indeterminate
                    :size="20"
                    :width="2"
                  ></v-progress-circular>
                </template>
                <template v-if="!reserveLoader">RESERVE</template>
              </v-btn>
            </div>
          </v-card>
        </v-row>
      </v-col>
    </v-row>
    <v-divider class="mt-15 mb-5"></v-divider>
    <v-row class="d-flex flex-column" style="padding-top: 40px">
      <h3 class="mb-5">
        <v-icon>mdi-comment-outline</v-icon>
        <span>Comments</span>
      </h3>
      <div v-if="isLoggedIn" class="d-flex mb-2">
        <v-textarea
          v-model="comment"
          rows="1"
          outlined
          label="Write your comment"
          class="mr-4"
        ></v-textarea>
        <v-btn outlined color="primary" @click="addComment">Submit</v-btn>
      </div>
      <div>
        <template v-if="comments && comments.length">
          <div v-for="(c, i) in comments" :key="i" elevation="1">
            <v-divider v-if="i" class="mb-3"></v-divider>
            <div v-if="c.user" class="mb-3">
              <b>{{ c.user.username }}</b>
            </div>
            <div class="mb-4">{{ c.body }}</div>
          </div>
        </template>
        <template v-else>
          <div class="mb-5">No comments available for this tour.</div>
        </template>
      </div>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: 'IndexPage',
  data: () => ({
    reserveLoader: false,
    tour: undefined,
    tags: [],
    comments: [],
    comment: '',
    isLoading: false,
    isLoggedIn: false,
  }),
  computed: {
    dateRangeText() {
      const startDate = this.formatDate(this.tour.start_date)
      const endDate = this.formatDate(this.tour.end_date)
      return `${startDate} - ${endDate}`
    },
  },
  mounted() {
    this.getTourTags()
    this.getTour()
    this.getTourComments()
    this.setIsLoggedIn()
    this.getRecom()
  },
  methods: {
    setIsLoggedIn() {
      const token = localStorage.getItem('ATAccessToken')
      if (token) {
        this.isLoggedIn = true
        return
      }
      this.isLoggedIn = false
    },
    async getTour() {
      const id = this.$route.params.id
      if (!id) return
      const res = await this.$store.dispatch('tour/getTourById', id)
      this.tour = res
      this.isLoading = false
    },
    async getTourTags() {
      const id = this.$route.params.id
      if (!id) return
      const res = await this.$store.dispatch('tour/getTourTags', id)
      this.tags = res.map((t) => t.name)
    },
    async getRecom() {
      const res = await this.$store.dispatch('tour/getRecom')
      console.log(res)
    },
    async getTourComments() {
      const id = this.$route.params.id
      if (!id) return
      const res = await this.$store.dispatch('tour/getTourComments', id)
      res.forEach(async (c) => {
        const user = await this.$store.dispatch('account/getUser', c.userId)
        c.user = user
      })
      this.comments = res
    },
    async addComment() {
      const id = this.$route.params.id
      if (!id) return
      await this.$store.dispatch('tour/addComment', {
        id,
        msg: this.comment,
      })
      window.location.reload()
    },
    async reserveTour() {
      const id = this.$route.params.id
      if (!id) return
      this.reserveLoader = true
      const body = {
        tour_id: id,
        reserve_count: 1,
      }
      const bill = await this.$store.dispatch('tour/reserveTourById', body)
      const res = await this.$store.dispatch('tour/redirectToPayment', bill.id)
      window.location.href = res.url
      this.reserveLoader = false
    },
    formatDate(d) {
      if (!d) return ''
      const date = new Date(d)
      return date
        .toDateString()
        .split(' ')
        .filter((s, i) => i > 0)
        .join(' ')
    },
  },
}
</script>

<style>
.data {
  position: relative;
  display: flex;
  align-items: center;
}

.data-value {
  position: absolute;
  left: 300px;
}
</style>

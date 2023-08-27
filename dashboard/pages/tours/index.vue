<template>
  <v-container class="mx-auto">
    <v-row class="mb-4">
      <v-col cols="12">
        <v-card-text class="text-h4 pb-0 px-0">List of tours</v-card-text>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12">
        <v-menu
          :close-on-content-click="false"
          :nudge-right="40"
          transition="scale-transition"
          offset-y
          min-width="auto"
        >
          <template #activator="{ on, attrs }">
            <v-chip v-model="dateRangeText" v-bind="attrs" v-on="on">
              <v-icon>mdi-plus</v-icon>
              <span class="px-1">Add filter</span>
            </v-chip>
          </template>
          <v-list style="width: 150px">
            <v-list-item
              v-for="(item, index) in Object.values(filterItems)"
              :key="index"
              @click="addFilter(item.name)"
            >
              <v-list-item-title class="d-flex justify-center">
                <v-icon v-show="item.check">mdi-check</v-icon>
                <span>{{ item.name }}</span>
              </v-list-item-title>
            </v-list-item>
          </v-list>
        </v-menu>
        <v-menu
          v-if="filterItems.time.check"
          :close-on-content-click="false"
          :nudge-right="40"
          transition="scale-transition"
          offset-y
          min-width="auto"
        >
          <template #activator="{ on, attrs }">
            <v-chip v-model="dateRangeText" v-bind="attrs" v-on="on">
              <v-icon>mdi-calendar-today</v-icon>
              <span class="px-1">{{ filters.date[0] }}</span>
              <span v-show="filters.date.length > 1" class="px-1">-</span>
              <span class="px-1">{{ filters.date[1] }}</span>
            </v-chip>
          </template>
          <v-date-picker
            v-model="filters.date"
            range
            @input="pickDate($event)"
          ></v-date-picker>
        </v-menu>
        <v-menu
          v-if="filterItems.location.check"
          :close-on-content-click="false"
          :nudge-right="40"
          transition="scale-transition"
          offset-y
          min-width="auto"
        >
          <template #activator="{ on, attrs }">
            <v-chip v-bind="attrs" v-on="on">
              <v-icon>mdi-earth</v-icon>
              <span class="px-1">location</span>
            </v-chip>
          </template>
          <v-card>
            <v-card-text>
              <v-text-field
                v-model="filters.location.src"
                placeholder="sort by src"
                class="my-1"
                solo
                hide-details
                flat
                outlined
              ></v-text-field>
              <v-text-field
                v-model="filters.location.dst"
                placeholder="sort by des"
                solo
                hide-details
                flat
                outlined
              ></v-text-field>
            </v-card-text>
            <v-card-text class="pt-0">
              <v-btn block plain class="primary" @click="getTours"
                >filter</v-btn
              >
            </v-card-text>
          </v-card>
        </v-menu>
        <v-menu
          v-if="filterItems.difficulty.check"
          :close-on-content-click="false"
          :nudge-right="40"
          transition="scale-transition"
          offset-y
          min-width="auto"
        >
          <template #activator="{ on, attrs }">
            <v-chip v-bind="attrs" v-on="on">
              <v-icon>mdi-star</v-icon>
              <span class="px-1">rate</span>
            </v-chip>
          </template>
          <v-card>
            <v-card-text>
              <v-rating
                v-model="filters.difficulty"
                empty-icon="mdi-checkbox-blank-circle-outline"
                full-icon="mdi-checkbox-blank-circle"
                background-color="grey-700 lighten-2"
                color="grey-700"
                size="12"
              ></v-rating>
            </v-card-text>
            <v-card-text class="pt-0">
              <v-btn block plain class="primary" @click="getTours"
                >filter</v-btn
              >
            </v-card-text>
          </v-card>
        </v-menu>
      </v-col>
    </v-row>
    <v-row>
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
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: 'ToursPage',
  data: () => ({
    isLoading: true,
    tours: [],
    filterItems: {
      time: { name: 'time', check: false },
      difficulty: { name: 'difficulty', check: false },
      location: { name: 'location', check: false },
    },
    filters: {
      date: [],
      location: {
        src: '',
        dst: '',
      },
      difficulty: null,
    },
  }),
  computed: {
    dateRangeText() {
      const startDate = this.formatDate(this.filters.date[0])
      const endDate = this.formatDate(this.filters.date[1])
      return `${startDate} - ${endDate}`
    },
  },
  // created() {
  //   if (typeof window === 'undefined') return
  //   this.getTours()
  // },
  mounted() {
    if (this.$route) {
      if (this.$route.query.start_date) {
        this.filters.date[0] = new Date(this.$route.query.start_date)
          .toISOString()
          .split('T')[0]
      }
      if (this.$route.query.end_date) {
        this.filters.date[1] = new Date(this.$route.query.end_date)
          .toISOString()
          .split('T')[0]
      }
    }
    if (typeof window === 'undefined') return
    this.getTours()
  },
  methods: {
    addFilter(filter) {
      const check = this.filterItems[filter].check
      if (filter === 'time') {
        if (this.filters.date.length === 0) {
          this.filters.date.push(new Date().toISOString().split('T')[0])
        }
        if (check) {
          this.filters.date = []
          const newRoute = JSON.parse(JSON.stringify(this.$route.query))
          delete newRoute.start_date
          delete newRoute.end_date
          const currentPath = this.$route.path
          if (JSON.stringify(this.$route.query) !== JSON.stringify(newRoute)) {
            this.$router.replace({ path: currentPath, query: { ...newRoute } })
            this.getTours()
          }
        }
      }
      if (filter === 'difficulty') {
        if (check) {
          this.filters.difficulty = undefined
          this.getTours()
        }
      }
      this.filterItems[filter].check = !check
    },
    pickDate(event) {
      if (event.length === 2) {
        const startDate = new Date(this.filters.date[0])
          .toISOString()
          .split('.')[0]
        const endDate = new Date(this.filters.date[1])
          .toISOString()
          .split('.')[0]
        const currentPath = this.$route.path
        const currentQuery = this.$route.query
        this.$router.replace({
          path: currentPath,
          query: {
            ...currentQuery,
            start_date: startDate,
            end_date: endDate,
          },
        })
        this.getTours()
      }
    },
    async getTours() {
      const res = await this.$store.dispatch('tour/getTours', {
        ...this.$route.query,
        src: this.filters.location.src,
        dst: this.filters.location.dst,
        difficulty: this.filters.difficulty,
      })
      this.tours = res
      this.isLoading = false
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

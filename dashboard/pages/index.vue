<template>
  <v-container style="height: 80%" class="d-flex align-center">
    <div class="green back"></div>
    <v-card
      style="background-color: #f8f7f9; min-width: 80%"
      class="mx-auto mt-10"
      max-width="800px"
    >
      <v-card-title class="mx-auto mb-4 justify-center">
        <div
          class="white px-8 py-2 rounded-lg elevation-2"
          style="margin-top: -2rem; width: 90%; text-align: center"
        >
          Tours
        </div>
      </v-card-title>
      <v-card-text class="mb-4">
        <v-text-field
          v-model="form.dst"
          prepend-inner-icon="mdi-magnify"
          solo
          flat
          placeholder="Enter a destination"
        >
        </v-text-field>
        <v-row>
          <v-col>
            <v-row no-gutters>
              <v-col>
                <v-menu
                  :close-on-content-click="true"
                  :nudge-right="40"
                  transition="scale-transition"
                  offset-y
                  min-width="auto"
                >
                  <template #activator="{ on, attrs }">
                    <v-btn
                      solo
                      depressed
                      class="datepicker-btn"
                      style="
                        border-top-right-radius: 0;
                        border-bottom-right-radius: 0;
                        border-right: solid 1px #00000030;
                      "
                      v-bind="attrs"
                      v-on="on"
                    >
                      <v-icon>mdi-calendar-start</v-icon>
                      <v-col align="left">
                        <div class="mb-1">{{ startDateText }}</div>
                        <div style="font-size: smaller; font-weight: 400">
                          {{ startDateWeekDay }}
                        </div>
                      </v-col>
                    </v-btn>
                  </template>
                  <v-date-picker
                    v-model="form.startDate"
                    scrollable
                  ></v-date-picker>
                </v-menu>
              </v-col>
              <v-col>
                <v-menu
                  :close-on-content-click="true"
                  :nudge-right="40"
                  transition="scale-transition"
                  offset-y
                  min-width="auto"
                >
                  <template #activator="{ on, attrs }">
                    <v-btn
                      solo
                      depressed
                      class="datepicker-btn"
                      style="
                        border-top-left-radius: 0;
                        border-bottom-left-radius: 0;
                      "
                      v-bind="attrs"
                      v-on="on"
                    >
                      <v-icon>mdi-calendar-end</v-icon>
                      <v-col align="left">
                        <div class="mb-1">{{ endDateText }}</div>
                        <div style="font-size: smaller; font-weight: 400">
                          {{ endDateWeekDay }}
                        </div>
                      </v-col>
                    </v-btn>
                  </template>
                  <v-date-picker
                    v-model="form.endDate"
                    scrollable
                  ></v-date-picker>
                </v-menu>
              </v-col>
            </v-row>
          </v-col>
          <v-col>
            <v-select
              v-model="form.difficulty"
              :items="difficultyOptions"
              label="Difficulty level"
              solo
              flat
              prepend-inner-icon="mdi-hard-hat"
            ></v-select>
          </v-col>
        </v-row>
      </v-card-text>
      <v-btn
        large
        class="primary white--text"
        style="
          position: absolute;
          bottom: -18px;
          left: calc(50% - 130px);
          widows: 50px;
          padding: 0 100px;
        "
        @click="submit"
      >
        SEARCH
      </v-btn>
    </v-card>
  </v-container>
</template>

<script>
export default {
  name: 'IndexPage',
  data: () => ({
    form: {
      dst: '',
      endDate: '',
      startDate: '',
      difficulty: 1,
    },
    menu: false,
    difficultyOptions: [1, 2, 3],
  }),
  computed: {
    startDateText() {
      if (!this.form.startDate) return ''
      return new Date(this.form.startDate)
        .toDateString()
        .split(' ')
        .filter((s, i) => i > 0)
        .join(' ')
    },
    startDateWeekDay() {
      if (!this.form.startDate) return '-'
      const date = new Date(this.form.startDate)
      const day = {
        0: 'Sunday',
        1: 'Monday',
        2: 'Tuesday',
        3: 'Wednesday',
        4: 'Thursday',
        5: 'Friday',
        6: 'Saturday',
      }[date.getDay()]
      if (!day) return '-'
      return day
    },
    endDateText() {
      if (!this.form.endDate) return ''
      return new Date(this.form.endDate)
        .toDateString()
        .split(' ')
        .filter((s, i) => i > 0)
        .join(' ')
    },
    endDateWeekDay() {
      if (!this.form.endDate) return '-'
      const date = new Date(this.form.endDate)
      const day = {
        0: 'Sunday',
        1: 'Monday',
        2: 'Tuesday',
        3: 'Wednesday',
        4: 'Thursday',
        5: 'Friday',
        6: 'Saturday',
      }[date.getDay()]
      if (!day) return '-'
      return day
    },
  },
  created() {
    this.form.startDate = this.formatDateJson(new Date())
    const date = new Date(new Date().setDate(new Date().getDate() + 7))
    this.form.endDate = this.formatDateJson(date)
  },
  methods: {
    formatDateJson(d) {
      if (!d) return ''
      return new Date(d).toJSON().split('T')[0]
    },
    submit() {
      const queryParam = Object.keys(this.form)
        .filter((f) => !!this.form[f])
        .map((f) => `${f}=${this.form[f]}`)
        .join('&')
      this.$router.push(`/tours?${queryParam}`)
    },
    formatDate(d) {
      if (!d) return 'No date'
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

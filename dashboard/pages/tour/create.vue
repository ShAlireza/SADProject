<template>
  <v-container class="mt-10">
    <h2 class="mb-6" style="font-weight: 400">Create tour</h2>
    <v-form ref="form" v-model="valid" style="width: 50%">
      <v-text-field
        v-model="form.name"
        :rules="formRules.name"
        required
        outlined
        label="Title"
      ></v-text-field>
      <v-menu
        :close-on-content-click="false"
        :nudge-right="40"
        transition="scale-transition"
        offset-y
        min-width="auto"
      >
        <template #activator="{ on, attrs }">
          <v-text-field
            v-model="dateRangeText"
            :rules="formRules.timeline"
            outlined
            label="Timeline"
            append-icon="mdi-calendar"
            readonly
            v-bind="attrs"
            v-on="on"
          ></v-text-field>
        </template>
        <v-date-picker v-model="form.timeline" range></v-date-picker>
      </v-menu>
      <v-text-field
        v-model="form.price"
        :rules="formRules.price"
        required
        outlined
        label="Price"
        append-icon="mdi-currency-rial"
        type="number"
      ></v-text-field>
      <v-text-field
        v-model="form.src"
        :rules="formRules.src"
        required
        outlined
        label="Source"
      ></v-text-field>
      <v-text-field
        v-model="form.dst"
        :rules="formRules.dst"
        required
        outlined
        label="Destination"
      ></v-text-field>
      <v-text-field
        v-model="form.capacity"
        :rules="formRules.capacity"
        required
        outlined
        label="Capacity"
        type="number"
      ></v-text-field>
      <v-text-field
        outlined
        label="Group link"
        persistent-hint
        hint="Optional"
      ></v-text-field>
      <v-select
        v-model="tourTags"
        :items="tagTitles"
        chips
        label="Tags"
        multiple
        outlined
      ></v-select>
      <v-file-input
        v-model="file"
        label="Image"
        outlined
        dense
        placeholder="Place your image here"
        prepend-icon=""
        append-icon="mdi-paperclip"
        persistent-hint
        hint="Optional"
        accept="image/*"
        @change="uploadFile"
      ></v-file-input>
      <v-textarea
        outlined
        label="Description"
        value=""
        persistent-hint
        hint="Optional"
      ></v-textarea>

      <v-btn
        color="primary"
        class="px-10"
        :disabled="!valid"
        @click="createTour()"
        >Save</v-btn
      >
    </v-form>
  </v-container>
</template>

<script>
export default {
  name: 'CreateTourPage',
  data: () => ({
    valid: false,
    file: undefined,
    form: {
      name: '',
      timeline: ['', ''],
      price: 0,
      src: '',
      dst: '',
      capacity: 0,
      total_days: 0,
      difficulty: 1,
      image_url: null,
    },
    formRules: {
      name: [(v) => !!v || 'Title is required'],
      timeline: [
        (v) => {
          const d = v.split('-').filter((s) => s !== ' ')
          return d.length > 1 || 'End date is required'
        },
      ],
      price: [(v) => v !== '' || 'Price is required'],
      src: [(v) => !!v || 'Source is required'],
      dst: [(v) => !!v || 'Destination is required'],
      capacity: [(v) => v !== '' || 'Capacity is required'],
    },
    tags: [
      { id: '5267d02f-f5dd-4184-90ba-b2e4bf106cc3', name: 'nature' },
      { id: '10ce02c3-41ac-41ab-9423-c9c2b2e260f2', name: 'camping' },
      { id: '5d17dbb8-9aee-4c9f-aba9-dedb948afdf6', name: 'side-seeing' },
      { id: '2e8b4eb4-86b7-4de0-a526-fa34decf535d', name: 'north' },
      { id: 'fd109131-a763-4e23-bb61-f01d9aa281ca', name: 'south' },
      { id: 'cba080ce-a196-434e-84e9-87a472c625c9', name: 'hotel' },
      { id: '06c3b45d-6a22-4622-835e-16b2ecd802ff', name: 'water' },
      { id: '84838019-f3fe-4da4-9d06-ceb8d3127ad9', name: 'swim' },
      { id: 'f9f70c0f-d2c8-430b-b775-970ce1796e57', name: 'museum' },
      { id: '55b6ec48-ea2b-4744-ae9c-6c8fe4d0128c', name: 'hunting' },
    ],
    tourTags: [],
  }),
  computed: {
    dateRangeText() {
      const startDate = this.formatDate(this.form.timeline[0])
      const endDate = this.formatDate(this.form.timeline[1])
      return `${startDate} - ${endDate}`
    },
    tagTitles() {
      return this.tags.map((t) => t.name)
    },
  },
  created() {
    this.form.timeline = [
      this.formatDateJson(new Date()),
      this.formatDateJson(new Date()),
    ]
  },
  methods: {
    formatDateToISO(d) {
      if (!d) return ''
      return new Date(d).toISOString().split('.')[0]
    },
    formatDateJson(d) {
      if (!d) return ''
      return new Date().toJSON().split('T')[0]
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
    async uploadFile() {
      if (!this.file) return
      const res = await this.$store.dispatch('upload/uploadTourFile', {
        file: this.file,
      })
      const url = res.urls[0]
      if (!url) return
      this.form.image_url = url
    },
    async createTour() {
      if (!this.valid) return
      const body = {
        ...this.form,
        start_date: this.formatDateToISO(this.form.timeline[0]),
        end_date: this.formatDateToISO(this.form.timeline[1]),
        price: Number(this.form.price),
        capacity: Number(this.form.capacity),
      }
      const res = await this.$store.dispatch('tour/createTour', body)
      this.tourTags.forEach(async (tagName) => {
        const tag = this.tags.find((t) => t.name === tagName)
        if (!tag) return
        const tagId = tag.id
        await this.$store.dispatch('tour/addTagToTour', {
          tourId: res.id,
          tagId,
        })
      })

      this.$router.push('/tours')
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

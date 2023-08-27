<template>
  <v-container v-if="t" class="pa-1">
    <v-card
      class="mx-auto my-12"
      max-width="300px"
      link
      :to="`/tours/${t.id}`"
      style="position: relative"
    >
      <template slot="progress">
        <v-progress-linear
          color="deep-purple"
          height="10"
          indeterminate
        ></v-progress-linear>
      </template>

      <v-img
        :contain="false"
        height="150"
        max-height="150"
        max-width="100%"
        :src="
          t.image_url ||
          'https://minio.alantouring.ir/tour/838fb2dd-1214-4499-9bef-cf5bf5808ce6'
        "
      ></v-img>

      <v-card-title class="pb-6">{{ t.name }}</v-card-title>

      <v-card-text>
        <v-row>
          <v-col class="py-1">
            <div>Difficulty level</div>
          </v-col>
          <v-col class="py-1" style="flex: 0">
            <v-rating
              empty-icon="mdi-checkbox-blank-circle-outline"
              full-icon="mdi-checkbox-blank-circle"
              background-color="grey-700 lighten-2"
              color="grey-700"
              size="12"
              length="3"
              :value="t.difficulty"
              readonly
            ></v-rating>
          </v-col>
        </v-row>

        <v-row>
          <v-col class="py-2">
            <div>
              From <b>{{ t.src }}</b> to <b>{{ t.dst }}</b>
            </div>
          </v-col>
        </v-row>

        <v-row>
          <v-col class="py-2 pb-5">
            Price <b> {{ t.price }} IRR </b>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script>
export default {
  props: ['t'],
}
</script>

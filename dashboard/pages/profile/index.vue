<template>
  <v-container class="mt-10">
    <template v-if="userLoading || profileLoading">
      <v-skeleton-loader
        v-bind="attrs"
        type="table-heading, list-item-two-line, list-item-two-line, list-item-two-line, list-item-two-line, actions"
      ></v-skeleton-loader>
    </template>
    <template v-if="!userLoading && !profileLoading">
      <div class="d-flex" style="justify-content: space-between">
        <h2 class="mb-6" style="font-weight: 400">Profile</h2>
        <v-dialog v-model="dialog" max-width="400px">
          <template #activator="{ on, attrs }">
            <v-btn text color="primary" v-bind="attrs" v-on="on">
              Change user type
            </v-btn>
          </template>
          <v-card>
            <v-card-title>
              <span class="text-h5">Change user Type</span>
            </v-card-title>
            <v-card-text style="padding-bottom: 0">
              <v-container style="padding-bottom: 0">
                <v-select
                  v-model="userType"
                  :items="['normal', 'organization', 'leader']"
                  label="User type"
                  required
                ></v-select>
              </v-container>
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="primary" @click="changeUser">
                <template v-if="changeUserTypeLoader">
                  <v-progress-circular
                    indeterminate
                    :size="20"
                    :width="2"
                  ></v-progress-circular>
                </template>
                <template v-if="!changeUserTypeLoader">Save</template>
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
      </div>

      <v-form ref="form" v-model="valid">
        <div style="position: relative">
          <v-img
            :src="
              profile.avatar ||
              'https://www.business2community.com/wp-content/uploads/2017/08/blank-profile-picture-973460_640.png'
            "
            width="100"
            height="100"
            style="border-radius: 100%; margin-bottom: 30px"
          ></v-img>
          <v-btn
            elevation="2"
            fab
            small
            style="position: absolute; bottom: 0; left: 70px"
            @click="openUpload"
          >
            <v-icon>mdi-pencil</v-icon>
          </v-btn>
          <v-file-input
            ref="file"
            v-model="file"
            dense
            prepend-icon=""
            append-icon=""
            accept="image/*"
            style="display: none"
            @change="uploadFile"
          >
          </v-file-input>
        </div>

        <v-text-field
          v-model="user.first_name"
          outlined
          label="First name"
        ></v-text-field>

        <v-text-field
          v-model="user.last_name"
          outlined
          label="Last name"
        ></v-text-field>

        <v-text-field
          v-model="user.username"
          outlined
          label="Username"
          required
          :rules="user.usernameRules"
        ></v-text-field>

        <v-text-field
          v-model="profile.phone_number"
          outlined
          label="Phone number"
          :rules="phoneNumberRules"
        ></v-text-field>

        <v-text-field
          v-if="userType === 'organization'"
          v-model="orgProfile.certificate"
          outlined
          label="Certificate "
        ></v-text-field>

        <v-text-field
          v-if="userType === 'leader'"
          v-model="leaderProfile.experience_level"
          outlined
          label="Experience level"
        ></v-text-field>

        <v-btn
          color="primary"
          class="px-10"
          :disabled="!valid"
          @click="submitForm"
          >Save</v-btn
        >
      </v-form>
    </template>
  </v-container>
</template>

<script>
export default {
  name: 'ProfilePage',
  data() {
    return {
      dialog: false,
      userLoading: true,
      profileLoading: true,
      valid: false,
      file: null,
      userType: 'Normal',
      changeUserTypeLoader: false,
      user: {
        first_name: '',
        last_name: '',
        username: '',
        usernameRules: [(v) => !!v || 'Username is required'],
      },
      profile: {
        phone_number: '',
        avatar: '',
        city: '',
      },
      orgProfile: {
        certificate: '',
      },
      leaderProfile: {
        experience_level: 0,
      },
      phoneNumberRules: [(v) => v.length !== 11 || 'Phone number is invalid'],
    }
  },
  mounted() {
    if (typeof window === 'undefined') return
    this.getUser()
  },
  methods: {
    async getUser() {
      const res = await this.$store.dispatch('account/getUser')
      this.user.first_name = res.first_name
      this.user.last_name = res.last_name
      this.user.username = res.username
      this.userType = res.type
      this.userLoading = false
      this.getProfile()
    },
    async getProfile() {
      let res
      this.profileLoading = true
      if (this.userType === 'normal') {
        res = await this.$store.dispatch('account/getNormalProfile')
      } else if (this.userType === 'organization') {
        res = await this.$store.dispatch('account/getOrgProfile')
        this.orgProfile.certificate = res.certificate
      } else if (this.userType === 'leader') {
        res = await this.$store.dispatch('account/getLeaderProfile')
        this.leaderProfile.experience_level = res.experience_level
      }
      if (!res) return
      this.profile.phone_number = res.phone_number
      this.profile.avatar = res.avatar
      this.profile.city = res.city
      this.profileLoading = false
    },
    async submitForm() {
      if (!this.valid) return
      await this.$store.dispatch('account/updateUser', {
        first_name: this.user.first_name,
        last_name: this.user.last_name,
        username: this.user.username,
      })
      if (this.userType === 'normal') {
        await this.$store.dispatch('account/updateNormalProfile', {
          ...this.profile,
        })
      } else if (this.userType === 'organization') {
        await this.$store.dispatch('account/updateOrgProfile', {
          ...this.profile,
          ...this.orgProfile,
        })
      } else if (this.userType === 'leader') {
        await this.$store.dispatch('account/updateLeaderProfile', {
          ...this.profile,
          ...this.leaderProfile,
        })
      }
    },
    openUpload() {
      const input =
        this.$refs.file.$el.getElementsByClassName('v-file-input__text')[0]
      input.click()
    },
    async uploadFile() {
      if (!this.file) return
      const res = await this.$store.dispatch('upload/uploadTourFile', {
        file: this.file,
      })
      const url = res.urls[0]
      if (!url) return
      this.profile.avatar = url
    },
    async changeUser() {
      this.changeUserTypeLoader = true
      const userType = this.userType.toLowerCase()
      await this.$store.dispatch('account/updateUser', {
        type: userType,
      })
      this.changeUserTypeLoader = false
      this.dialog = false
      try {
        if (this.userType === 'organization') {
          await this.$store.dispatch('account/createOrgProfile', {
            avatar: this.profile.avatar,
            phone_number: this.profile.phone_number,
            city: this.profile.city,
            certificate: '',
            address: '',
          })
        } else if (this.userType === 'leader') {
          await this.$store.dispatch('account/createLeaderProfile', {
            avatar: this.profile.avatar,
            phone_number: this.profile.phone_number,
            city: this.profile.city,
            experience_level: 0,
          })
        }
      } catch (err) {}
    },
  },
}
</script>

<style scoped></style>

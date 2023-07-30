<template>
  <div>
    <AppSidebar />
    <div class="wrapper d-flex flex-column min-vh-100 bg-light">
      <AppHeader />
      <div class="body flex-grow-1 px-3">
        <Onboarding />
        <CContainer lg>
          <router-view />
        </CContainer>
      </div>
      <AppFooter />
    </div>
  </div>
</template>
<script>
import { CContainer } from '@coreui/vue'
import AppFooter from '@/pages/components/AppFooter.vue'
import AppHeader from '@/pages/components/AppHeader.vue'
import AppSidebar from '@/pages/components/AppSidebar.vue'
import Onboarding from '@/pages/components/Onboarding.vue'

export default {
  name: 'DefaultLayout',
  components: {
    AppFooter,
    AppHeader,
    AppSidebar,
    CContainer,
    Onboarding,
  },
  data() {
    return {}
  },
  methods: {},
  mounted: function () {},
}
</script>

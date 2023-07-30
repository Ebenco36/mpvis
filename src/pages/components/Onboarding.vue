<template>
  <div>
    <VOnboardingWrapper ref="wrapper" :steps="steps" />
  </div>
</template>

<script>
import { defineComponent, ref } from 'vue'
import { VOnboardingWrapper, useVOnboarding } from 'v-onboarding'
import 'v-onboarding/dist/style.css'
export default defineComponent({
  components: {
    VOnboardingWrapper,
  },
  setup() {
    const wrapper = ref(null)
    const { start, goToStep, finish } = useVOnboarding(wrapper)
    const steps = [
      {
        attachTo: { element: '#foo' },
        content: { title: 'Welcome!' },
      },
      {
        attachTo: { element: '#bar' },
        content: {
          title: 'Testing v-onboarding..',
          description:
            'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation.',
        },
      },
    ]

    return {
      wrapper,
      steps,
      start,
      finish,
      goToStep,
    }
  },
  mounted() {
    this.start()
  },
})
</script>
<style>
:root {
  --v-onboarding-overlay-z: 10000;
  --v-onboarding-step-z: 100000;
  --v-onboarding-overlay-opacity: 0.4;
  /* --v-onboarding-overlay-fill: lightseagreen; */
}
</style>

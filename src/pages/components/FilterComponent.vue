<template>
  <div>
    <!-- Large modal -->
    <button
      type="button"
      class="btn btn-primary"
      data-toggle="modal"
      data-target=".bd-example-modal-lg"
    >
      Large modal
    </button>

    <div
      class="modal fade bd-example-modal-lg"
      tabindex="-1"
      role="dialog"
      aria-labelledby="myLargeModalLabel"
      aria-hidden="true"
    >
      <div class="modal-dialog modal-lg">
        <div class="modal-content">...</div>
      </div>
    </div>
  </div>
</template>
<script>
export default {
  components: {},
  name: 'Modals',
  data() {
    return {
      selectedOption: null,
      options: [
        { id: 1, name: 'Option 1' },
        { id: 2, name: 'Option 2' },
        { id: 3, name: 'Option 3' },
        // Add more options as needed
      ],
    }
  },
}
</script>

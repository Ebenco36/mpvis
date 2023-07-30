<template>
  <div>
    <WidgetsStatsA />
    <CRow>
      <CCol :md="12">
        <CCard class="mb-4">
          <CCardBody>
            <CRow>
              <CCol :sm="5">
                <h4 id="release" class="card-title mb-0">Yearly Releases</h4>
                <div class="small text-medium-emphasis">January 2021</div>
              </CCol>
            </CRow>
            <CRow>
              <FilterComponentVue />
              <div ref="chartContainer"></div>
            </CRow>
          </CCardBody>
        </CCard>
      </CCol>

      <CCol :md="12">
        <CCard class="mb-4">
          <CCardBody>
            <CRow>
              <CCol :sm="5">
                <h4 id="traffic" class="card-title mb-0">Data Grouping</h4>
                <div class="small text-medium-emphasis">January 2021</div>
              </CCol>
            </CRow>
            <CRow>
              <div ref="groupChartContainer"></div>
            </CRow>
          </CCardBody>

          <CCardFooter>
            <CRow :xs="{ cols: 1 }" :md="{ cols: 5 }" class="text-center">
              <CCol class="mb-sm-2 mb-0">
                <div class="text-medium-emphasis">Rows</div>
                <strong>{{ rows }} rows</strong>
                <CProgress
                  class="mt-2"
                  color="success"
                  thin
                  :precision="1"
                  :value="rows"
                />
              </CCol>
              <CCol class="mb-sm-2 mb-0 d-md-down-none">
                <div class="text-medium-emphasis">Columns</div>
                <strong>{{ columns }}</strong>
                <CProgress
                  class="mt-2"
                  color="info"
                  thin
                  :precision="1"
                  :value="columns"
                />
              </CCol>
              <CCol class="mb-sm-2 mb-0">
                <div class="text-medium-emphasis">Pageviews</div>
                <strong>78.706 Views (60%)</strong>
                <CProgress
                  class="mt-2"
                  color="warning"
                  thin
                  :precision="1"
                  :value="60"
                />
              </CCol>
              <CCol class="mb-sm-2 mb-0">
                <div class="text-medium-emphasis">New Users</div>
                <strong>22.123 Users (80%)</strong>
                <CProgress
                  class="mt-2"
                  color="danger"
                  thin
                  :precision="1"
                  :value="80"
                />
              </CCol>
              <CCol class="mb-sm-2 mb-0 d-md-down-none">
                <div class="text-medium-emphasis">Bounce Rate</div>
                <strong>Average Rate (40.15%)</strong>
                <CProgress class="mt-2" :value="40" thin :precision="1" />
              </CCol>
            </CRow>
          </CCardFooter>
        </CCard>
      </CCol>
    </CRow>
  </div>
</template>

<script>
import WidgetsStatsA from '../widgets/WidgetsStatsTypeA.vue'
import vegaEmbed from 'vega-embed'
import FilterComponentVue from '../../components/FilterComponent.vue'

export default {
  name: 'Dashboard',
  components: {
    WidgetsStatsA,
    FilterComponentVue,
  },
  data: function () {
    return {
      rows: 0,
      columns: 0,
      graph_list: null,
    }
  },
  mounted() {
    this.fetchChartData()
  },
  methods: {
    async fetchChartData() {
      console.log('Welcome')
      // Make a request to your backend API to fetch the chart data
      const response = await fetch('/api/v1/dashboard')
      const data = await response.json()

      // rows and columns count
      this.rows = data.rows
      this.columns = data.columns
      // Render the chart using Vega-Embed
      vegaEmbed(this.$refs.chartContainer, data.trend)

      //   vegaEmbed(this.$refs.groupChartContainer, data.group_graph)
      // Embed each graph in the list
      this.graph_list = data.group_graph_array
      this.graph_list.forEach((item, index) => {
        console.log(index)
        this.embedGraph(item)
      })
    },
    // Function to embed each graph using vegaEmbed
    embedGraph(graphSpec) {
      vegaEmbed(this.$refs['groupChartContainer'], graphSpec, {
        actions: false,
      })
    },
  },
}
</script>

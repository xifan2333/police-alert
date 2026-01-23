<script setup>
import { ref, onMounted, nextTick } from 'vue'
import * as echarts from 'echarts'
import PageHeader from '@/components/PageHeader.vue'
import { getSituationData } from '@/api/data'

// 数据状态
const communities = ref([])
const isLoading = ref(true)

const policeClassification = ref({
  header: ['名称', '数量', '同比', '环比'],
  data: [],
  rowNum: 7,
  headerBGC: 'rgba(14, 165, 233, 0.2)',
  oddRowBGC: 'rgba(14, 165, 233, 0.05)',
  evenRowBGC: 'rgba(14, 165, 233, 0.1)',
  columnWidth: [120, 80, 80, 80],
  align: ['left', 'center', 'center', 'center']
})

const theftTraditional = ref({
  header: ['地点', '数量'],
  data: [],
  rowNum: 5,
  headerBGC: 'rgba(14, 165, 233, 0.2)',
  oddRowBGC: 'rgba(14, 165, 233, 0.05)',
  evenRowBGC: 'rgba(14, 165, 233, 0.1)'
})

const telecomFraud = ref({
  header: ['小区', '数量'],
  data: [],
  rowNum: 5,
  headerBGC: 'rgba(14, 165, 233, 0.2)',
  oddRowBGC: 'rgba(14, 165, 233, 0.05)',
  evenRowBGC: 'rgba(14, 165, 233, 0.1)'
})

const viceCases = ref({
  header: ['小区', '数量'],
  data: [],
  rowNum: 5,
  headerBGC: 'rgba(14, 165, 233, 0.2)',
  oddRowBGC: 'rgba(14, 165, 233, 0.05)',
  evenRowBGC: 'rgba(14, 165, 233, 0.1)'
})

const disputeCases = ref({
  header: ['社区', '数量'],
  data: [],
  rowNum: 5,
  headerBGC: 'rgba(14, 165, 233, 0.2)',
  oddRowBGC: 'rgba(14, 165, 233, 0.05)',
  evenRowBGC: 'rgba(14, 165, 233, 0.1)'
})

const fightCases = ref({
  header: ['区域', '数量'],
  data: [],
  rowNum: 5,
  headerBGC: 'rgba(14, 165, 233, 0.2)',
  oddRowBGC: 'rgba(14, 165, 233, 0.05)',
  evenRowBGC: 'rgba(14, 165, 233, 0.1)'
})

const gamblingCases = ref({
  header: ['地点', '数量'],
  data: [],
  rowNum: 5,
  headerBGC: 'rgba(14, 165, 233, 0.2)',
  oddRowBGC: 'rgba(14, 165, 233, 0.05)',
  evenRowBGC: 'rgba(14, 165, 233, 0.1)'
})

const repeatAlarms = ref({
  header: ['报警人', '报警次数', '最近报警时间'],
  data: [],
  rowNum: 5,
  headerBGC: 'rgba(14, 165, 233, 0.2)',
  oddRowBGC: 'rgba(14, 165, 233, 0.05)',
  evenRowBGC: 'rgba(14, 165, 233, 0.1)'
})

// 图表实例
const overviewChartInstance = ref(null)
const overviewChartRef = ref(null)

// 7个分类的图表实例
const categoryChartInstances = ref([])
const categoryChartRefs = ref([])

// 分类配置
const categories = [
  { label: '偷盗/传统盗财', key: 'theft', color: '#ef4444', dataRef: 'theftTraditional' },
  { label: '电诈/新型盗财', key: 'telecom', color: '#f59e0b', dataRef: 'telecomFraud' },
  { label: '涉黄案件', key: 'vice', color: '#8b5cf6', dataRef: 'viceCases' },
  { label: '纠纷案件', key: 'dispute', color: '#10b981', dataRef: 'disputeCases' },
  { label: '打架斗殴', key: 'fight', color: '#06b6d4', dataRef: 'fightCases' },
  { label: '涉赌案件', key: 'gambling', color: '#ec4899', dataRef: 'gamblingCases' },
  { label: '重复报警', key: 'repeat', color: '#f97316', dataRef: 'repeatAlarms' }
]

// 获取分类数据
const getCategoryData = (index) => {
  const dataRefMap = {
    'theftTraditional': theftTraditional,
    'telecomFraud': telecomFraud,
    'viceCases': viceCases,
    'disputeCases': disputeCases,
    'fightCases': fightCases,
    'gamblingCases': gamblingCases,
    'repeatAlarms': repeatAlarms
  }
  return dataRefMap[categories[index].dataRef]
}

// 加载数据
const fetchData = async () => {
  try {
    isLoading.value = true
    const res = await getSituationData()

    policeClassification.value = { ...policeClassification.value, data: res.data.policeClassification }
    theftTraditional.value = { ...theftTraditional.value, data: res.data.theftTraditional }
    telecomFraud.value = { ...telecomFraud.value, data: res.data.telecomFraud }
    viceCases.value = { ...viceCases.value, data: res.data.viceCases }
    disputeCases.value = { ...disputeCases.value, data: res.data.disputeCases }
    fightCases.value = { ...fightCases.value, data: res.data.fightCases }
    gamblingCases.value = { ...gamblingCases.value, data: res.data.gamblingCases }
    repeatAlarms.value = { ...repeatAlarms.value, data: res.data.repeatAlarms }

    communities.value = res.data.communities || []
  } catch (error) {
    console.error('加载数据失败:', error)
  } finally {
    isLoading.value = false
  }
}

const map = ref(null)

// 初始化天地图
const initMap = () => {
  setTimeout(() => {
    if (!window.T) {
      console.error('天地图 API 未加载')
      return
    }

    const centerLng = 122.3093
    const centerLat = 29.9597

    map.value = new T.Map('mapDiv')
    map.value.centerAndZoom(new T.LngLat(centerLng, centerLat), 14)

    // 添加标记
    theftTraditional.value.data.forEach((item, index) => {
      const community = communities.value[index % communities.value.length]
      const marker = new T.Marker(new T.LngLat(community.lng, community.lat))
      map.value.addOverLay(marker)
      const infoWin = new T.InfoWindow(`
        <div style="padding: 10px; min-width: 200px;">
          <h3 style="margin: 0 0 8px 0; color: #0ea5e9; font-size: 16px;">偷盗/传统盗财</h3>
          <p style="margin: 4px 0; color: #64748b;">地点: <span style="color: #ef4444; font-weight: bold;">${item[0]}</span></p>
          <p style="margin: 4px 0; color: #64748b;">数量: <span style="color: #f59e0b; font-weight: bold;">${item[1]}</span></p>
        </div>
      `, { offset: new T.Point(0, -30) })
      marker.addEventListener('click', () => marker.openInfoWindow(infoWin))
    })

    console.log('天地图初始化完成')
  }, 500)
}

// 初始化总览图表（环比柱状图）
const initOverviewChart = () => {
  nextTick(() => {
    if (!overviewChartRef.value) return
    if (!policeClassification.value.data || policeClassification.value.data.length === 0) return

    if (overviewChartInstance.value) {
      overviewChartInstance.value.dispose()
    }

    overviewChartInstance.value = echarts.init(overviewChartRef.value)

    const categories = policeClassification.value.data.map(item => item[0])
    const values = policeClassification.value.data.map(item => {
      const ratio = item[3]
      return parseFloat(ratio.replace('%', ''))
    })

    const option = {
      title: {
        text: '警情分类环比趋势',
        left: 'center',
        textStyle: {
          color: '#C9FFFF',
          fontSize: 14,
          fontWeight: 600
        }
      },
      tooltip: {
        trigger: 'axis',
        axisPointer: { type: 'shadow' },
        backgroundColor: 'rgba(6, 24, 70, 0.9)',
        borderColor: 'rgba(14, 165, 233, 0.5)',
        textStyle: { color: '#C9FFFF' }
      },
      xAxis: {
        type: 'category',
        data: categories,
        axisLabel: {
          rotate: 30,
          fontSize: 10,
          color: '#94a3b8',
          interval: 0
        },
        axisLine: {
          lineStyle: { color: 'rgba(14, 165, 233, 0.3)' }
        }
      },
      yAxis: {
        type: 'value',
        name: '环比(%)',
        nameTextStyle: {
          color: '#94a3b8',
          fontSize: 12
        },
        axisLabel: {
          color: '#94a3b8',
          fontSize: 10,
          formatter: '{value}%'
        },
        axisLine: {
          lineStyle: { color: 'rgba(14, 165, 233, 0.3)' }
        },
        splitLine: {
          lineStyle: { color: 'rgba(14, 165, 233, 0.1)' }
        }
      },
      series: [
        {
          type: 'bar',
          data: values,
          itemStyle: {
            color: (params) => {
              return params.value >= 0
                ? 'rgba(34, 197, 94, 0.8)'
                : 'rgba(239, 68, 68, 0.8)'
            },
            borderRadius: [4, 4, 0, 0]
          },
          label: {
            show: true,
            position: 'top',
            formatter: '{c}%',
            color: '#C9FFFF',
            fontSize: 10
          }
        }
      ],
      grid: {
        left: '15%',
        right: '5%',
        top: '20%',
        bottom: '30%'
      }
    }

    overviewChartInstance.value.setOption(option)
  })
}

// 初始化详情图表（所有分类）
const initCategoryCharts = () => {
  nextTick(() => {
    categories.forEach((category, index) => {
      const chartRef = categoryChartRefs.value[index]
      if (!chartRef) return

      const categoryData = getCategoryData(index)
      if (!categoryData.value.data || categoryData.value.data.length === 0) return

      // 销毁旧实例
      if (categoryChartInstances.value[index]) {
        categoryChartInstances.value[index].dispose()
      }

      // 创建新实例
      categoryChartInstances.value[index] = echarts.init(chartRef)

      const labels = categoryData.value.data.map(item => item[0])
      const values = categoryData.value.data.map(item => item[1])

      const option = {
        title: {
          text: category.label,
          left: 'center',
          textStyle: {
            color: '#C9FFFF',
            fontSize: 14,
            fontWeight: 600
          }
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: { type: 'shadow' },
          backgroundColor: 'rgba(6, 24, 70, 0.9)',
          borderColor: 'rgba(14, 165, 233, 0.5)',
          textStyle: { color: '#C9FFFF' }
        },
        xAxis: {
          type: 'category',
          data: labels,
          axisLabel: {
            rotate: 30,
            fontSize: 10,
            color: '#94a3b8',
            interval: 0
          },
          axisLine: {
            lineStyle: { color: 'rgba(14, 165, 233, 0.3)' }
          }
        },
        yAxis: {
          type: 'value',
          name: '数量',
          nameTextStyle: {
            color: '#94a3b8',
            fontSize: 10
          },
          axisLabel: {
            color: '#94a3b8',
            fontSize: 10
          },
          axisLine: {
            lineStyle: { color: 'rgba(14, 165, 233, 0.3)' }
          },
          splitLine: {
            lineStyle: { color: 'rgba(14, 165, 233, 0.1)' }
          }
        },
        series: [
          {
            type: 'bar',
            data: values,
            itemStyle: {
              color: category.color,
              borderRadius: [4, 4, 0, 0]
            },
            label: {
              show: true,
              position: 'top',
              color: '#C9FFFF',
              fontSize: 10
            }
          }
        ],
        grid: {
          left: '15%',
          right: '5%',
          top: '20%',
          bottom: '25%'
        }
      }

      categoryChartInstances.value[index].setOption(option)
    })
  })
}

// 响应式调整
const handleResize = () => {
  overviewChartInstance.value?.resize()
  categoryChartInstances.value.forEach(chart => chart?.resize())
}

onMounted(() => {
  fetchData().then(() => {
    initMap()
    initOverviewChart()
    initCategoryCharts()
  })

  window.addEventListener('resize', handleResize)
})
</script>

<template>
  <div class="situation-page">
    <PageHeader title="警情态势监控追踪" />

    <!-- 主内容区域 - 上半部分 -->
    <div class="top-section">
      <!-- 左侧：警情分类总览表格 -->
      <div class="overview-table-box">
        <dv-border-box-12>
          <div class="table-content">
            <div class="table-title">警情分类总览</div>
            <dv-scroll-board :config="policeClassification" />
          </div>
        </dv-border-box-12>
      </div>

      <!-- 中间：天地图 -->
      <div class="map-box">
        <dv-border-box-13>
          <div class="map-container" id="mapDiv">
            <div class="map-placeholder">天地图区域</div>
          </div>
        </dv-border-box-13>
      </div>

      <!-- 右侧：环比趋势图表 -->
      <div class="overview-chart-box">
        <dv-border-box-12>
          <div class="chart-content">
            <div ref="overviewChartRef" class="chart-inner"></div>
          </div>
        </dv-border-box-12>
      </div>
    </div>

    <!-- 下半部分：7个分类详情区域 -->
    <div class="categories-section">
      <div
        v-for="(category, index) in categories"
        :key="category.key"
        class="category-item"
      >
        <dv-border-box-12>
          <div class="category-content">
            <!-- 图表 -->
            <div class="category-chart">
              <div :ref="el => categoryChartRefs[index] = el" class="chart-inner"></div>
            </div>
            <!-- 表格 -->
            <div class="category-table">
              <dv-scroll-board :config="getCategoryData(index).value" />
            </div>
          </div>
        </dv-border-box-12>
      </div>
    </div>
  </div>
</template>

<style scoped>
.situation-page {
  height: 100vh;
  width: 100vw;
  background: url(/main-bg-003.jpg) center/cover no-repeat;
  font-family: sans-serif;
  color: #e5e7eb;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

/* 上半部分：总览区域 */
.top-section {
  display: grid;
  grid-template-columns: 1fr 2fr 1fr;
  gap: 12px;
  padding: 0 12px;
  height: 45%;
  flex-shrink: 0;
}

.overview-table-box,
.overview-chart-box {
  overflow: hidden;
}

.table-content,
.chart-content {
  background: rgba(6, 24, 70, 0.6);
  backdrop-filter: blur(10px);
  padding: 12px;
  height: 100%;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.table-title {
  font-size: 16px;
  font-weight: 600;
  color: #C9FFFF;
  text-align: center;
  padding-bottom: 8px;
  border-bottom: 2px solid rgba(14, 165, 233, 0.3);
  flex-shrink: 0;
}

.chart-inner {
  width: 100%;
  height: 100%;
}

/* 地图区域 */
.map-box {
  overflow: hidden;
}

.map-container {
  width: 100%;
  height: 100%;
  border-radius: 4px;
  overflow: hidden;
  filter: invert(0.9) hue-rotate(180deg) brightness(0.95) contrast(1.1);
  padding: 16px;
  background: rgba(6, 24, 70, 0.6);
  backdrop-filter: blur(10px);
}

.map-container :deep(.tdt-control-copyright) {
  filter: invert(1) hue-rotate(180deg);
}

.map-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0, 0, 0, 0.3);
  color: rgba(255, 255, 255, 0.5);
  font-size: 24px;
}

/* 下半部分：7个分类详情区域 */
.categories-section {
  flex: 1;
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  grid-template-rows: repeat(2, 1fr);
  gap: 12px;
  padding: 12px;
  overflow: hidden;
}

.category-item {
  overflow: hidden;
  min-height: 0;
}

.category-content {
  background: rgba(6, 24, 70, 0.6);
  backdrop-filter: blur(10px);
  padding: 8px;
  height: 100%;
  display: flex;
  flex-direction: column;
  gap: 8px;
  overflow: hidden;
}

.category-chart {
  flex: 1;
  min-height: 0;
  overflow: hidden;
}

.category-table {
  flex: 1;
  min-height: 0;
  overflow: hidden;
}

/* 响应式调整 - 针对超大屏幕优化 */
@media (min-width: 3840px) {
  .table-title {
    font-size: 20px;
  }

  .map-placeholder {
    font-size: 32px;
  }
}
</style>

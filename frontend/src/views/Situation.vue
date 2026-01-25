<script setup>
import { ref, onMounted, nextTick } from 'vue'
import * as echarts from 'echarts'
import PageHeader from '@/components/PageHeader.vue'
import FloatingButton from '@/components/FloatingButton.vue'
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
  header: ['地点', '报警次数', '最近报警时间'],
  data: [],
  rowNum: 5,
  headerBGC: 'rgba(14, 165, 233, 0.2)',
  oddRowBGC: 'rgba(14, 165, 233, 0.05)',
  evenRowBGC: 'rgba(14, 165, 233, 0.1)',
  columnWidth: [200, 100, 120],
  align: ['left', 'center', 'center']
})

// 图表实例
const overviewChartInstance = ref(null)
const overviewChartRef = ref(null)

// 分类配置
const categories = [
  { label: '偷盗', key: 'theft', color: '#ef4444', dataRef: 'theftTraditional' },
  { label: '诈骗', key: 'telecom', color: '#f59e0b', dataRef: 'telecomFraud' },
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
  const dataRef = dataRefMap[categories[index].dataRef]
  return dataRef ? dataRef.value : {}
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

    // 添加标记 - 添加空数据保护
    if (communities.value.length === 0 || theftTraditional.value.data.length === 0) {
      console.warn('社区坐标或偷盗数据为空，跳过标记生成')
      return
    }

    theftTraditional.value.data.forEach((item, index) => {
      const community = communities.value[index % communities.value.length]
      if (!community || !community.lng || !community.lat) {
        console.warn('社区坐标数据不完整，跳过该标记')
        return
      }
      const marker = new T.Marker(new T.LngLat(community.lng, community.lat))
      map.value.addOverLay(marker)
      const infoWin = new T.InfoWindow(`
        <div style="padding: 10px; min-width: 200px;">
          <h3 style="margin: 0 0 8px 0; color: #0ea5e9; font-size: 32px;">偷盗</h3>
          <p style="margin: 4px 0; color: #64748b;">地点: <span style="color: #ef4444; font-weight: bold;">${item[0]}</span></p>
          <p style="margin: 4px 0; color: #64748b;">数量: <span style="color: #f59e0b; font-weight: bold;">${item[1]}</span></p>
        </div>
      `, { offset: new T.Point(0, -30) })
      marker.addEventListener('click', () => marker.openInfoWindow(infoWin))
    })

    console.log('天地图初始化完成')
  }, 500)
}

// 初始化总览图表（警情分类总览）
const initOverviewChart = () => {
  nextTick(() => {
    if (!overviewChartRef.value) return
    if (!policeClassification.value.data || policeClassification.value.data.length === 0) return

    if (overviewChartInstance.value) {
      overviewChartInstance.value.dispose()
    }

    overviewChartInstance.value = echarts.init(overviewChartRef.value)

    const categories = policeClassification.value.data.map(item => item[0])
    const quantities = policeClassification.value.data.map(item => item[1])
    const tongbiValues = policeClassification.value.data.map(item => {
      const ratio = item[2]
      return parseFloat(ratio.replace('%', ''))
    })
    const huanbiValues = policeClassification.value.data.map(item => {
      const ratio = item[3]
      return parseFloat(ratio.replace('%', ''))
    })

    const option = {
      title: {
        text: '警情分类总览',
        left: 'center',
        textStyle: {
          color: '#C9FFFF',
          fontSize: 28,
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
      legend: {
        data: ['数量', '同比', '环比'],
        top: '12%',
        textStyle: {
          color: '#C9FFFF',
          fontSize: 16
        }
      },
      xAxis: {
        type: 'category',
        data: categories,
        axisLabel: {
          rotate: 90,
          fontSize: 16,
          color: '#94a3b8',
          interval: 0
        },
        axisLine: {
          lineStyle: { color: 'rgba(14, 165, 233, 0.3)' }
        }
      },
      yAxis: [
        {
          type: 'value',
          name: '数量',
          position: 'left',
          nameTextStyle: {
            color: '#94a3b8',
            fontSize: 18
          },
          axisLabel: {
            color: '#94a3b8',
            fontSize: 16
          },
          axisLine: {
            lineStyle: { color: 'rgba(14, 165, 233, 0.3)' }
          },
          splitLine: {
            lineStyle: { color: 'rgba(14, 165, 233, 0.1)' }
          }
        },
        {
          type: 'value',
          name: '百分比(%)',
          position: 'right',
          nameTextStyle: {
            color: '#94a3b8',
            fontSize: 18
          },
          axisLabel: {
            color: '#94a3b8',
            fontSize: 16,
            formatter: '{value}%'
          },
          axisLine: {
            lineStyle: { color: 'rgba(14, 165, 233, 0.3)' }
          },
          splitLine: {
            show: false
          }
        }
      ],
      series: [
        {
          name: '数量',
          type: 'bar',
          data: quantities,
          itemStyle: {
            color: 'rgba(59, 130, 246, 0.8)',
            borderRadius: [4, 4, 0, 0]
          },
          label: {
            show: true,
            position: 'top',
            color: '#C9FFFF',
            fontSize: 14
          }
        },
        {
          name: '同比',
          type: 'line',
          yAxisIndex: 1,
          data: tongbiValues,
          itemStyle: {
            color: 'rgba(34, 197, 94, 0.8)'
          },
          lineStyle: {
            width: 2
          },
          label: {
            show: true,
            formatter: '{c}%',
            color: '#C9FFFF',
            fontSize: 12
          }
        },
        {
          name: '环比',
          type: 'line',
          yAxisIndex: 1,
          data: huanbiValues,
          itemStyle: {
            color: 'rgba(251, 146, 60, 0.8)'
          },
          lineStyle: {
            width: 2
          },
          label: {
            show: true,
            formatter: '{c}%',
            color: '#C9FFFF',
            fontSize: 12
          }
        }
      ],
      grid: {
        left: '12%',
        right: '12%',
        top: '25%',
        bottom: '25%'
      }
    }

    overviewChartInstance.value.setOption(option)
  })
}

// 响应式调整
const handleResize = () => {
  overviewChartInstance.value?.resize()
}

onMounted(() => {
  fetchData().then(() => {
    initMap()
    initOverviewChart()
  })

  window.addEventListener('resize', handleResize)
})
</script>

<template>
  <div class="situation-page">
    <PageHeader title="警情态势追踪" />

    <!-- 主内容区域 -->
    <div class="main-section">
      <!-- 左侧：图表和表格 -->
      <div class="left-section">
        <!-- 警情分类总览图表 -->
        <div class="overview-chart-box">
          <dv-border-box-12>
            <div class="chart-content">
              <div ref="overviewChartRef" class="chart-inner"></div>
            </div>
          </dv-border-box-12>
        </div>

        <!-- 重复报警表格 -->
        <div class="repeat-alarms-box">
          <dv-border-box-12>
            <div class="table-content">
              <div class="table-title">重复报警</div>
              <dv-scroll-board :config="repeatAlarms" />
            </div>
          </dv-border-box-12>
        </div>
      </div>

      <!-- 中间：天地图 -->
      <div class="map-box">
        <dv-border-box-13>
          <div class="map-container" id="mapDiv">
            <div class="map-placeholder">天地图区域</div>
          </div>
        </dv-border-box-13>
      </div>

      <!-- 右侧：6个分类详情区域 -->
      <div class="right-section">
        <div
          v-for="(category, index) in categories.slice(0, 6)"
          :key="category.key"
          class="category-item"
        >
          <dv-border-box-12>
            <div class="category-content">
              <!-- 标题 -->
              <div class="category-title">{{ category.label }}</div>
              <!-- 表格 -->
              <div class="category-table">
                <dv-scroll-board :config="getCategoryData(index)" />
              </div>
            </div>
          </dv-border-box-12>
        </div>
      </div>
    </div>

    <!-- 悬浮返回按钮 -->
    <FloatingButton />
  </div>
</template>

<style scoped>
.situation-page {
  height: 100%;
  width: 100%;
  background: url(/main-bg-003.jpg) center/cover no-repeat;
  font-family: sans-serif;
  color: #e5e7eb;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

/* 主内容区域 */
.main-section {
  flex: 1;
  display: grid;
  grid-template-columns: 1fr 2fr 1fr;
  gap: 12px;
  padding: 0 12px 12px 12px;
  overflow: hidden;
}

/* 左侧区域：图表+表格 */
.left-section {
  display: flex;
  flex-direction: column;
  gap: 12px;
  overflow: hidden;
}

.overview-chart-box,
.repeat-alarms-box {
  flex: 1;
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
  font-size: 28px;
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
  font-size: 48px;
}

/* 右侧区域：6个分类表格 */
.right-section {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  grid-template-rows: repeat(3, 1fr);
  gap: 12px;
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
  gap: 6px;
  overflow: hidden;
}

.category-title {
  font-size: 20px;
  font-weight: 600;
  color: #C9FFFF;
  text-align: center;
  padding-bottom: 4px;
  border-bottom: 2px solid rgba(14, 165, 233, 0.3);
  flex-shrink: 0;
}

.category-table {
  flex: 1;
  min-height: 0;
  overflow: hidden;
}

/* 响应式调整 - 针对超大屏幕优化 */
@media (min-width: 3840px) {
  .table-title {
    font-size: 40px;
  }

  .category-title {
    font-size: 28px;
  }

  .map-placeholder {
    font-size: 64px;
  }
}
</style>

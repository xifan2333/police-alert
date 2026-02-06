<script setup>
import { ref, onMounted, nextTick, watch } from 'vue'
import * as echarts from 'echarts'
import PageHeader from '@/components/PageHeader.vue'
import FloatingButton from '@/components/FloatingButton.vue'
import { getSituationData } from '@/api/data'
import { applyDataVStyles } from '@/utils/styleApplicator'

// 数据状态
const mapMarkers = ref([])
const isLoading = ref(true)

// 地图类型筛选
const selectedTypes = ref(['偷盗', '诈骗'])
const availableTypes = [
  { label: '偷盗', value: '偷盗', color: 'var(--c-category-theft)' },
  { label: '诈骗', value: '诈骗', color: 'var(--c-category-fraud)' },
  { label: '涉黄', value: '涉黄', color: 'var(--c-category-sex-related)' },
  { label: '涉赌', value: '涉赌', color: 'var(--c-category-gambling)' },
  { label: '纠纷', value: '纠纷', color: 'var(--c-category-dispute)' },
  { label: '人身伤害', value: '人身伤害', color: 'var(--c-category-injury)' }
]

// 时间周期选择
const timePeriod = ref('month')
const timePeriods = [
  { label: '周', value: 'week' },
  { label: '月', value: 'month' },
  { label: '年', value: 'year' }
]

const policeClassification = ref({
  header: ['名称', '数量', '同比', '环比'],
  data: [],
  rowNum: 7,
  headerBGC: 'rgba(var(--c-primary-rgb), 0.2)',
  oddRowBGC: 'rgba(var(--c-primary-rgb), 0.05)',
  evenRowBGC: 'rgba(var(--c-primary-rgb), 0.1)',
  columnWidth: [120, 80, 80, 80],
  align: ['left', 'center', 'center', 'center']
})

const theftTraditional = ref({
  header: ['地点', '数量'],
  data: [],
  rowNum: 5,
  headerBGC: 'rgba(0, 191, 255, 0.2)',
  oddRowBGC: 'rgba(0, 191, 255, 0.05)',
  evenRowBGC: 'rgba(0, 191, 255, 0.1)'
})

const telecomFraud = ref({
  header: ['小区', '数量'],
  data: [],
  rowNum: 5,
  headerBGC: 'rgba(0, 191, 255, 0.2)',
  oddRowBGC: 'rgba(0, 191, 255, 0.05)',
  evenRowBGC: 'rgba(0, 191, 255, 0.1)'
})

const viceCases = ref({
  header: ['小区', '数量'],
  data: [],
  rowNum: 5,
  headerBGC: 'rgba(0, 191, 255, 0.2)',
  oddRowBGC: 'rgba(0, 191, 255, 0.05)',
  evenRowBGC: 'rgba(0, 191, 255, 0.1)'
})

const disputeCases = ref({
  header: ['社区', '数量'],
  data: [],
  rowNum: 5,
  headerBGC: 'rgba(0, 191, 255, 0.2)',
  oddRowBGC: 'rgba(0, 191, 255, 0.05)',
  evenRowBGC: 'rgba(0, 191, 255, 0.1)'
})

const fightCases = ref({
  header: ['区域', '数量'],
  data: [],
  rowNum: 5,
  headerBGC: 'rgba(0, 191, 255, 0.2)',
  oddRowBGC: 'rgba(0, 191, 255, 0.05)',
  evenRowBGC: 'rgba(0, 191, 255, 0.1)'
})

const gamblingCases = ref({
  header: ['地点', '数量'],
  data: [],
  rowNum: 5,
  headerBGC: 'rgba(0, 191, 255, 0.2)',
  oddRowBGC: 'rgba(0, 191, 255, 0.05)',
  evenRowBGC: 'rgba(0, 191, 255, 0.1)'
})

const repeatAlarms = ref({
  header: ['地点', '报警次数', '最近报警时间'],
  data: [],
  rowNum: 5,
  headerBGC: 'rgba(0, 191, 255, 0.2)',
  oddRowBGC: 'rgba(0, 191, 255, 0.05)',
  evenRowBGC: 'rgba(0, 191, 255, 0.1)',
  columnWidth: [200, 100, 120],
  align: ['left', 'center', 'center']
})

// 图表实例
const overviewChartInstance = ref(null)
const overviewChartRef = ref(null)

// 分类配置
const categories = [
  { label: '偷盗', key: 'theft', color: 'var(--c-category-theft)', dataRef: 'theftTraditional' },
  { label: '诈骗', key: 'telecom', color: 'var(--c-category-fraud)', dataRef: 'telecomFraud' },
  { label: '涉黄案件', key: 'vice', color: 'var(--c-category-sex-related)', dataRef: 'viceCases' },
  { label: '纠纷案件', key: 'dispute', color: 'var(--c-category-dispute)', dataRef: 'disputeCases' },
  { label: '打架斗殴', key: 'fight', color: 'var(--c-category-injury)', dataRef: 'fightCases' },
  { label: '涉赌案件', key: 'gambling', color: 'var(--c-category-gambling)', dataRef: 'gamblingCases' },
  { label: '重复报警', key: 'repeat', color: 'var(--c-category-repeated)', dataRef: 'repeatAlarms' }
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
    const typesStr = selectedTypes.value.join(',')
    console.log('开始请求数据:', { timePeriod: timePeriod.value, alertTypes: typesStr })
    const res = await getSituationData(timePeriod.value, typesStr)
    console.log('收到响应数据:', res)

    // 表格数据引用映射
    const dataRefMap = {
      policeClassification,
      theftTraditional,
      telecomFraud,
      viceCases,
      disputeCases,
      fightCases,
      gamblingCases,
      repeatAlarms
    }

    // 统一处理所有表格：应用显示规则
    const displayRules = res.data.displayRules || {}

    for (const tableCode in dataRefMap) {
      const tableRef = dataRefMap[tableCode]
      const tableData = res.data[tableCode]
      const tableRules = displayRules[tableCode] || []

      if (tableData && tableRef.value) {
        // 使用通用函数应用样式
        const styledData = applyDataVStyles(
          tableData,
          tableRules,
          tableRef.value.header
        )

        // 更新表格数据
        tableRef.value = { ...tableRef.value, data: styledData }
        console.log(`${tableCode} 数据已更新，应用了 ${tableRules.length} 条规则`)
      }
    }

    // 更新地图标记
    mapMarkers.value = res.data.mapData || []
    console.log('地图数据更新:', mapMarkers.value.length, '条记录')

    // 如果地图已初始化，更新地图标记
    if (map.value) {
      console.log('开始更新地图标记')
      updateMapMarkers()
    } else {
      console.warn('地图未初始化')
    }

    // 重新渲染图表
    initOverviewChart()
  } catch (error) {
    console.error('加载数据失败:', error)
  } finally {
    isLoading.value = false
  }
}

const map = ref(null)
const mapOverlays = ref([])

// 获取类型颜色
const getTypeColor = (alertType) => {
  const type = availableTypes.find(t => t.value === alertType)
  return type ? type.color : '#00BFFF'
}

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

    // 初始化后更新地图标记
    updateMapMarkers()
  }, 500)
}

// 更新地图标记
const updateMapMarkers = () => {
  if (!map.value) return

  // 清除旧标记
  clearMapMarkers()

  // 按地点合并数据
  const locationMap = new Map()
  mapMarkers.value.forEach(item => {
    if (!item.lng || !item.lat) return

    const key = `${item.lng},${item.lat}` // 使用经纬度作为唯一标识
    if (!locationMap.has(key)) {
      locationMap.set(key, {
        location: item.location,
        lng: item.lng,
        lat: item.lat,
        types: []
      })
    }
    locationMap.get(key).types.push({
      alertType: item.alertType,
      count: item.count
    })
  })

  // 收集所有坐标点，用于计算边界
  const points = []

  // 为每个地点创建 Marker + Label
  locationMap.forEach(data => {
    const lngLat = new T.LngLat(data.lng, data.lat)
    points.push(lngLat)

    // 创建 Marker
    const marker = new T.Marker(lngLat)
    map.value.addOverLay(marker)
    mapOverlays.value.push(marker)

    // 构建标注内容（按类型分类显示）
    let typesText = ''
    data.types.forEach(type => {
      typesText += `${type.alertType}: ${type.count}起\n`
    })

    const totalCount = data.types.reduce((sum, type) => sum + type.count, 0)

    // 创建标注内容
    const labelContent = `${data.location}\n总计: ${totalCount}起\n${typesText}`

    // 创建 Label
    const label = new T.Label({
      text: labelContent,
      position: lngLat,
      offset: new T.Point(0, -30) // 向上偏移，避免遮挡 Marker
    })

    // 设置样式
    label.setFontSize(14)
    label.setFontColor('#1e293b')
    label.setBackgroundColor('#ffffff')
    label.setBorderLine(2)
    label.setBorderColor('#00BFFF')
    label.setOpacity(0.95)

    // 添加到地图
    map.value.addOverLay(label)
    mapOverlays.value.push(label)

    // 添加点击事件，提升 z-index
    const bringToFront = () => {
      // 重置所有覆盖物的 z-index 为较低值
      mapOverlays.value.forEach(overlay => {
        if (typeof overlay.setZindex === 'function') {
          overlay.setZindex(100)
        }
      })

      // 提升当前 marker 和 label 的 z-index
      if (typeof marker.setZindex === 'function') {
        marker.setZindex(9999)
      }
      if (typeof label.setZindex === 'function') {
        label.setZindex(9999)
      }
    }

    // 为 marker 和 label 添加点击事件
    marker.addEventListener('click', bringToFront)
    label.addEventListener('click', bringToFront)
  })

  // 自动调整地图视野，让所有标记点都可见
  if (points.length > 0) {
    try {
      const bounds = new T.LngLatBounds()
      points.forEach(point => {
        bounds.extend(point)
      })
      // 天地图使用 setViewport 方法
      map.value.setViewport(points)
    } catch (error) {
      console.warn('地图视野调整失败:', error)
    }
  }

  console.log(`地图更新完成，共 ${locationMap.size} 个地点，${mapMarkers.value.length} 条记录`)
}

// 清除地图标记
const clearMapMarkers = () => {
  if (map.value && mapOverlays.value.length > 0) {
    mapOverlays.value.forEach(overlay => {
      map.value.removeOverLay(overlay)
    })
    mapOverlays.value = []
  }
}

// 切换类型选择
const toggleType = (type) => {
  const index = selectedTypes.value.indexOf(type)
  if (index > -1) {
    // 至少保留一个类型
    if (selectedTypes.value.length > 1) {
      selectedTypes.value.splice(index, 1)
    }
  } else {
    selectedTypes.value.push(type)
  }
}

// 监听类型变化，重新请求数据
watch(selectedTypes, () => {
  fetchData()
}, { deep: true })

// 监听时间周期变化，重新请求数据
watch(timePeriod, (newVal) => {
  console.log('时间周期变化:', newVal)
  fetchData()
})

// 初始化总览图表（警情分类总览）
const initOverviewChart = () => {
  nextTick(() => {
    if (!overviewChartRef.value) {
      console.warn('图表容器未找到')
      return
    }
    if (!policeClassification.value.data || policeClassification.value.data.length === 0) {
      console.warn('图表数据为空')
      return
    }

    console.log('开始渲染图表，数据:', policeClassification.value.data)

    // 如果图表实例已存在，先销毁
    if (overviewChartInstance.value) {
      overviewChartInstance.value.dispose()
      overviewChartInstance.value = null
    }

    // 重新初始化图表
    overviewChartInstance.value = echarts.init(overviewChartRef.value)

    // 从 HTML 标签中提取原始数据
    const extractText = (html) => {
      if (typeof html === 'string' && html.includes('<span')) {
        const match = html.match(/>([^<]+)</)
        return match ? match[1] : html
      }
      return html
    }

    const categories = policeClassification.value.data.map(item => extractText(item[0]))
    const quantities = policeClassification.value.data.map(item => {
      const text = extractText(item[1])
      return typeof text === 'number' ? text : parseInt(text) || 0
    })
    const tongbiValues = policeClassification.value.data.map(item => {
      const ratio = extractText(item[2])
      if (ratio === 'N/A' || !ratio) return 0
      const value = parseFloat(ratio.replace('%', ''))
      return isNaN(value) ? 0 : value
    })
    const huanbiValues = policeClassification.value.data.map(item => {
      const ratio = extractText(item[3])
      if (ratio === 'N/A' || !ratio) return 0
      const value = parseFloat(ratio.replace('%', ''))
      return isNaN(value) ? 0 : value
    })

    console.log('图表数据解析:', { categories, quantities, tongbiValues, huanbiValues })

    // 图表使用前端默认配色方案（不应用后端规则）
    const defaultColors = [
      'rgba(239, 68, 68, 0.8)',   // 偷盗 - 红色
      'rgba(245, 158, 11, 0.8)',  // 诈骗 - 橙色
      'rgba(139, 92, 246, 0.8)',  // 涉黄 - 紫色
      'rgba(236, 72, 153, 0.8)',  // 涉赌 - 粉色
      'rgba(16, 185, 129, 0.8)',  // 纠纷 - 绿色
      'rgba(6, 182, 212, 0.8)',   // 人身伤害 - 青色
      'rgba(34, 197, 94, 0.9)'    // 有效警情（总计）- 亮绿色
    ]
    const barColors = quantities.map((_, index) => {
      return defaultColors[index] || 'rgba(0, 191, 255, 0.8)'
    })

    const option = {
      title: {
        text: '警情分类总览',
        left: 'center',
        textStyle: {
          color: '#00E5FF',
          fontSize: 28,
          fontWeight: 600
        }
      },
      tooltip: {
        trigger: 'axis',
        axisPointer: { type: 'shadow' },
        backgroundColor: 'rgba(0, 30, 60, 0.9)',
        borderColor: 'rgba(0, 191, 255, 0.5)',
        textStyle: { color: '#00E5FF' },
        formatter: function (params) {
          // params 是一个数组，包含了每个 series 在这个点上的信息
          const dataIndex = params[0].dataIndex
          const category = categories[dataIndex]
          const originalData = policeClassification.value.data[dataIndex]
          const quantity = extractText(originalData[1])
          const tongbi = extractText(originalData[2])
          const huanbi = extractText(originalData[3])

          // 使用 ECharts 提供的 series marker 增加可读性
          const quantityMarker = params.find(p => p.seriesName === '数量').marker
          const tongbiMarker = params.find(p => p.seriesName === '同比').marker
          const huanbiMarker = params.find(p => p.seriesName === '环比').marker

          return `${category}<br/>` +
                 `${quantityMarker}数量: ${quantity}<br/>` +
                 `${tongbiMarker}同比: ${tongbi}<br/>` +
                 `${huanbiMarker}环比: ${huanbi}`
        }
      },
      legend: {
        data: [
            { name: '数量', icon: 'rect' }, // 为柱状图指定矩形图标
            { name: '同比' },
            { name: '环比' }
        ],
        top: '12%',
        textStyle: {
          color: '#00E5FF',
          fontSize: 16
        }
      },
      grid: {
        left: '5%',
        right: '5%',
        top: '25%',
        bottom: '20%', // 增大底部边距，为竖向标签预留充足空间
        containLabel: true
      },
      xAxis: {
        type: 'category',
        data: categories,
        axisLabel: {
          rotate: 0, // 不旋转
          interval: 0, // 强制显示所有标签
          color: '#A8B2C5',
          fontSize: 14,
          // formatter 实现文字竖向排列
          formatter: function (value) {
            return value.split('').join('\n')
          }
        },
        axisLine: {
          lineStyle: { color: 'rgba(0, 191, 255, 0.3)' }
        }
      },
      yAxis: [
        {
          // Y 轴 0 (左侧): 用于"数量"
          type: 'value',
          name: '数量',
          position: 'left',
          nameTextStyle: { color: '#A8B2C5', fontSize: 16 },
          axisLabel: { color: '#A8B2C5', fontSize: 14 },
          axisLine: { show: true, lineStyle: { color: 'rgba(0, 191, 255, 0.3)' } },
          splitLine: { lineStyle: { color: 'rgba(0, 191, 255, 0.1)' } }
        },
        {
          // Y 轴 1 (右侧): 用于"同比"和"环比"
          type: 'value',
          name: '百分比',
          position: 'right',
          nameTextStyle: { color: '#A8B2C5', fontSize: 16 },
          axisLabel: {
            color: '#A8B2C5',
            fontSize: 14,
            formatter: '{value}%' // 自动为标签添加百分号
          },
          axisLine: { show: true, lineStyle: { color: 'rgba(0, 191, 255, 0.3)' } },
          splitLine: { show: false } // 右侧Y轴不显示分割线，保持图表简洁
        }
      ],
      series: [
        {
          name: '数量',
          type: 'bar',
          yAxisIndex: 0, // 关联到左侧的 Y 轴 (索引为 0)
          data: quantities.map((value, index) => ({
            value: value,
            itemStyle: {
              color: barColors[index],
              borderRadius: [4, 4, 0, 0]
            }
          })),
          label: {
            show: true,
            position: 'top',
            color: '#00E5FF',
            fontSize: 14,
            formatter: '{c}' // 仅在柱顶显示数值
          }
        },
        {
          name: '同比',
          type: 'line',
          yAxisIndex: 1, // 关联到右侧的 Y 轴 (索引为 1)
          smooth: true,
          data: tongbiValues,
          itemStyle: { color: '#00E5FF' }, // accent 青色
          lineStyle: { width: 3 }
        },
        {
          name: '环比',
          type: 'line',
          yAxisIndex: 1, // 关联到右侧的 Y 轴 (索引为 1)
          smooth: true,
          data: huanbiValues,
          itemStyle: { color: '#FBBF24' }, // warning 黄色
          lineStyle: { width: 3 }
        }
      ]
    }

    console.log('设置图表配置，类别:', categories, '数量:', quantities)
    overviewChartInstance.value.setOption(option, true) // 第二个参数 true 表示不合并，完全替换
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
          <div class="map-wrapper">
            <!-- 地图容器 -->
            <div class="map-container" id="mapDiv">
              <div class="map-placeholder">天地图区域</div>
            </div>
            <!-- 操作栏（底部） -->
            <div class="map-controls">
              <!-- 类型筛选 -->
              <div class="control-group">
                <div class="control-label">显示类型</div>
                <div class="control-buttons">
                  <button
                    v-for="type in availableTypes"
                    :key="type.value"
                    :class="['control-btn', { active: selectedTypes.includes(type.value) }]"
                    :style="{ '--type-color': type.color }"
                    @click="toggleType(type.value)"
                  >
                    {{ type.label }}
                  </button>
                </div>
              </div>
              <!-- 时间周期切换 -->
              <div class="control-group">
                <div class="control-label">时间周期</div>
                <div class="control-buttons">
                  <button
                    v-for="period in timePeriods"
                    :key="period.value"
                    :class="['control-btn', { active: timePeriod === period.value }]"
                    @click="timePeriod = period.value"
                  >
                    {{ period.label }}
                  </button>
                </div>
              </div>
            </div>
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
  background: var(--bg-sub) center/cover no-repeat;
  font-family: var(--font-sans);
  color: var(--c-text-primary);
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
  background: var(--c-bg-panel);
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
  color: var(--c-accent);
  text-align: center;
  padding-bottom: 8px;
  border-bottom: 2px solid var(--c-border);
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

.map-wrapper {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  background: var(--c-bg-panel);
  padding: 16px;
}

.map-container {
  flex: 1;
  width: 100%;
  border-radius: 4px;
  overflow: hidden;
  filter: invert(0.9) hue-rotate(180deg) brightness(0.95) contrast(1.1);
  margin-bottom: 12px;
}

.map-container :deep(.tdt-control-copyright) {
  display: none !important;
}

.map-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0, 0, 0, 0.3);
  color: rgba(var(--c-text-primary-rgb), 0.5);
  font-size: 48px;
}

/* 底部操作栏 */
.map-controls {
  flex-shrink: 0;
  display: flex;
  gap: 16px;
  padding: 12px;
  background: rgba(var(--c-primary-rgb), 0.1);
  border-radius: 8px;
  border: 1px solid var(--c-border);
}

.control-group {
  display: flex;
  align-items: center;
  gap: 8px;
}

.control-label {
  font-size: 16px;
  font-weight: 600;
  color: var(--c-accent);
  white-space: nowrap;
  margin-right: 4px;
}

.control-buttons {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
}

.control-btn {
  padding: 6px 14px;
  font-size: 15px;
  color: var(--c-text-secondary);
  background: rgba(var(--c-primary-rgb), 0.15);
  border: 2px solid rgba(var(--c-primary-rgb), 0.3);
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s ease;
  white-space: nowrap;
}

.control-btn:hover {
  background: rgba(var(--c-primary-rgb), 0.3);
  border-color: rgba(var(--c-primary-rgb), 0.5);
}

.control-btn.active {
  color: var(--c-text-primary);
  background: var(--type-color, var(--c-primary));
  border-color: var(--type-color, var(--c-primary));
  box-shadow: 0 0 10px var(--type-color, var(--c-primary));
}

.map-container :deep(.tdt-control-copyright) {
  display: none !important;
}

.map-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0, 0, 0, 0.3);
  color: rgba(var(--c-text-primary-rgb), 0.5);
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
  background: var(--c-bg-panel);
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
  color: var(--c-accent);
  text-align: center;
  padding-bottom: 4px;
  border-bottom: 2px solid var(--c-border);
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

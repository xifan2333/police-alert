/**
 * 样式应用工具 - 统一的显示规则处理
 *
 * 本模块提供前端统一的样式应用逻辑，支持：
 * 1. DataV 表格的单元格级样式（通过 HTML 注入）
 * 2. 普通表格的行级样式（通过样式对象）
 */

/**
 * 为 DataV 表格应用样式规则（单元格级别）
 *
 * @param {Array<Array<any>>} data - 表格的原始数据，二维数组格式
 * @param {Array<Object>} rules - 显示规则数组
 * @param {Array<string>} headers - 表头数组，用于列匹配
 * @returns {Array<Array<string>>} - 处理后包含 HTML 标签的二维数组
 *
 * @example
 * const data = [['地点A', 10], ['地点B', 5]]
 * const rules = [{
 *   rule_type: 'color',
 *   rule_config: {
 *     field: '数量',
 *     conditions: [{ operator: '>=', value: 10, font_color: '#ff0000' }]
 *   },
 *   priority: 1
 * }]
 * const headers = ['地点', '数量']
 * const result = applyDataVStyles(data, rules, headers)
 * // result: [['地点A', '<span style="color: #ff0000; font-weight: bold;">10</span>'], ['地点B', '5']]
 */
export function applyDataVStyles(data, rules, headers) {
  // 边缘情况处理
  if (!data || data.length === 0 || !rules || rules.length === 0) {
    return data
  }

  // 1. 预处理：将规则按字段名（列名）分组并映射到列索引，提高性能
  const rulesByColumnIndex = new Map()

  for (const rule of rules) {
    // 只处理 color 类型的规则
    if (rule.rule_type !== 'color' || !rule.rule_config?.field) continue

    // 查找字段对应的列索引
    const columnIndex = headers.indexOf(rule.rule_config.field)
    if (columnIndex === -1) continue

    // 按列索引分组规则
    if (!rulesByColumnIndex.has(columnIndex)) {
      rulesByColumnIndex.set(columnIndex, [])
    }

    // 按优先级排序，高优先级在前
    rulesByColumnIndex.get(columnIndex).push(rule)
    rulesByColumnIndex.get(columnIndex).sort((a, b) => (b.priority || 0) - (a.priority || 0))
  }

  // 如果没有可应用的规则，直接返回原数据
  if (rulesByColumnIndex.size === 0) {
    return data
  }

  // 2. 遍历数据并应用规则
  return data.map(row => {
    return row.map((cellValue, colIndex) => {
      // 如果当前列没有规则，直接返回原始值
      if (!rulesByColumnIndex.has(colIndex)) {
        return cellValue
      }

      const applicableRules = rulesByColumnIndex.get(colIndex)

      // 3. 查找第一个匹配的规则
      for (const rule of applicableRules) {
        for (const condition of rule.rule_config.conditions || []) {
          const { operator, value, font_color } = condition
          if (!operator || !font_color) continue

          let matched = false
          const numericValue = parseFloat(cellValue)

          // 根据操作符判断是否匹配
          if (operator === '==' || operator === 'eq') {
            matched = cellValue == value
          } else if (operator === '>=') {
            matched = !isNaN(numericValue) && numericValue >= value
          } else if (operator === '<=') {
            matched = !isNaN(numericValue) && numericValue <= value
          } else if (operator === '>') {
            matched = !isNaN(numericValue) && numericValue > value
          } else if (operator === '<') {
            matched = !isNaN(numericValue) && numericValue < value
          } else if (operator === 'in') {
            matched = Array.isArray(value) && value.includes(cellValue)
          }

          if (matched) {
            // 找到匹配项，应用样式并立即返回
            // XSS 防护：对 cellValue 进行 HTML 转义
            const sanitizedCellValue = String(cellValue)
              .replace(/&/g, '&amp;')
              .replace(/</g, '&lt;')
              .replace(/>/g, '&gt;')
              .replace(/"/g, '&quot;')
              .replace(/'/g, '&#039;')

            return `<span style="color: ${font_color}; font-weight: bold;">${sanitizedCellValue}</span>`
          }
        }
      }

      // 没有匹配的规则，返回原始值
      return cellValue
    })
  })
}

/**
 * 为普通表格应用样式规则（行级别）
 *
 * @param {Array<Object>} items - 数据项数组
 * @param {Array<Object>} rules - 显示规则数组
 * @returns {Array<Object>} - 添加了 style 属性的数据项数组
 *
 * @example
 * const items = [
 *   { id: 1, name: '案件A', days_remaining: 3 },
 *   { id: 2, name: '案件B', days_remaining: 10 }
 * ]
 * const rules = [{
 *   rule_type: 'color',
 *   rule_config: {
 *     field: 'days_remaining',
 *     conditions: [{ operator: '<=', value: 5, font_color: '#ff0000' }]
 *   },
 *   priority: 1
 * }]
 * const result = applyRowStyles(items, rules)
 * // result: [
 * //   { id: 1, name: '案件A', days_remaining: 3, style: { font_color: '#ff0000' } },
 * //   { id: 2, name: '案件B', days_remaining: 10, style: { font_color: null } }
 * // ]
 */
export function applyRowStyles(items, rules) {
  if (!items || items.length === 0 || !rules || rules.length === 0) {
    return items
  }

  // 按优先级排序规则
  const sortedRules = [...rules].sort((a, b) => (a.priority || 0) - (b.priority || 0))

  return items.map(item => {
    const style = findMatchingStyle(item, sortedRules)
    return { ...item, style }
  })
}

/**
 * 查找匹配的样式（内部函数）
 *
 * @param {Object} itemData - 数据项
 * @param {Array<Object>} rules - 已排序的规则数组
 * @returns {Object} - 样式对象 { font_color, style_token }
 */
function findMatchingStyle(itemData, rules) {
  const style = {
    font_color: null,
    style_token: null
  }

  // 按优先级遍历规则
  for (const rule of rules) {
    if (rule.rule_type !== 'color') continue

    const ruleConfig = rule.rule_config
    const field = ruleConfig?.field
    const conditions = ruleConfig?.conditions || []

    // 获取字段值
    const fieldValue = itemData[field]
    if (fieldValue === undefined || fieldValue === null) continue

    // 检查条件
    for (const condition of conditions) {
      const { operator, value, font_color, style_token } = condition
      if (!operator) continue

      let matched = false

      // 根据操作符判断是否匹配
      if (operator === '<=') {
        matched = fieldValue <= value
      } else if (operator === '>=') {
        matched = fieldValue >= value
      } else if (operator === '==') {
        matched = fieldValue == value
      } else if (operator === 'eq') {
        matched = fieldValue == value
      } else if (operator === '<') {
        matched = fieldValue < value
      } else if (operator === '>') {
        matched = fieldValue > value
      } else if (operator === 'in') {
        const values = condition.values || []
        matched = values.includes(fieldValue)
      }

      if (matched) {
        style.font_color = font_color
        style.style_token = style_token
        return style // 命中第一个规则后返回
      }
    }
  }

  return style
}

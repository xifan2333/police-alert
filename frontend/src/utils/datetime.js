/**
 * 时间格式化工具函数
 */

/**
 * 格式化日期时间为年月日格式
 * @param {string|Date} dateStr - 日期字符串或 Date 对象
 * @returns {string} 格式化后的日期字符串，如：2026-01-23
 */
export const formatDateTime = (dateStr) => {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit'
  }).replace(/\//g, '-')
}

/**
 * 格式化日期时间为年月日时分格式
 * @param {string|Date} dateStr - 日期字符串或 Date 对象
 * @returns {string} 格式化后的日期时间字符串，如：2026-01-23 08:20
 */
export const formatDateTimeWithTime = (dateStr) => {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  }).replace(/\//g, '-')
}

/**
 * 格式化日期时间为年月日时分秒格式
 * @param {string|Date} dateStr - 日期字符串或 Date 对象
 * @returns {string} 格式化后的日期时间字符串，如：2026-01-23 08:20:30
 */
export const formatDateTimeFull = (dateStr) => {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  }).replace(/\//g, '-')
}

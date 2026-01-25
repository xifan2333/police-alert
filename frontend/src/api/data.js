/**
 * 数据 API - 占位函数
 * 后续替换为真实 API 调用
 */
import { get } from './request'

/**
 * 获取社区列表
 * @returns {Promise<Array>}
 */
export const getCommunities = async () => {
  try {
    // TODO: 替换为真实 API
    // const data = await get('/communities')
    // return data

    // 占位：返回空数组
    return []
  } catch (error) {
    console.error('获取社区列表失败:', error)
    return []
  }
}

/**
 * 获取案件列表
 * @param {Object} params - 查询参数
 * @param {string} params.status - 案件状态（如：unresolved）
 * @returns {Promise<Array>}
 */
export const getCases = async (params = {}) => {
  try {
    // TODO: 替换为真实 API
    // const data = await get('/cases', { params })
    // return data

    // 占位：返回空数组
    return []
  } catch (error) {
    console.error('获取案件列表失败:', error)
    return []
  }
}

/**
 * 获取纠纷列表
 * @param {Object} params - 查询参数
 * @param {string} params.status - 纠纷状态（如：unresolved）
 * @returns {Promise<Array>}
 */
export const getDisputes = async (params = {}) => {
  try {
    // TODO: 替换为真实 API
    // const data = await get('/disputes', { params })
    // return data

    // 占位：返回空数组
    return []
  } catch (error) {
    console.error('获取纠纷列表失败:', error)
    return []
  }
}

/**
 * 获取警情态势数据
 * @param {string} timePeriod - 时间维度（week/month/year）
 * @param {string} alertTypes - 警情类型，逗号分隔，如 "偷盗,诈骗"
 * @returns {Promise<Object>}
 */
export function getSituationData(timePeriod = 'month', alertTypes = '偷盗,诈骗') {
  return get('/data/situation', {
    params: {
      time_period: timePeriod,
      alert_types: alertTypes
    }
  })
}

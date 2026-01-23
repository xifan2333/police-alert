/**
 * API 请求工具
 */

const BASE_URL = '/api/v1'

/**
 * 通用请求方法
 * @param {string} url - 请求路径
 * @param {object} options - fetch 选项
 * @returns {Promise<any>}
 */
export async function request(url, options = {}) {
  const defaultOptions = {
    headers: {
      'Content-Type': 'application/json',
    },
  }

  const config = {
    ...defaultOptions,
    ...options,
    headers: {
      ...defaultOptions.headers,
      ...options.headers,
    },
  }

  try {
    const response = await fetch(`${BASE_URL}${url}`, config)

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    const data = await response.json()
    return data
  } catch (error) {
    console.error('API请求失败:', error)
    throw error
  }
}

/**
 * GET 请求
 */
export function get(url, options = {}) {
  return request(url, {
    ...options,
    method: 'GET',
  })
}

/**
 * POST 请求
 */
export function post(url, data, options = {}) {
  return request(url, {
    ...options,
    method: 'POST',
    body: JSON.stringify(data),
  })
}

/**
 * PUT 请求
 */
export function put(url, data, options = {}) {
  return request(url, {
    ...options,
    method: 'PUT',
    body: JSON.stringify(data),
  })
}

/**
 * DELETE 请求
 */
export function del(url, options = {}) {
  return request(url, {
    ...options,
    method: 'DELETE',
  })
}

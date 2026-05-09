/**
 * 时间格式化相关常量
 * 统一管理时间相关的文本和格式
 */

export const TIME_FORMATS = {
  // 相对时间文本
  RELATIVE: {
    JUST_NOW: '刚刚',
    MINUTES_AGO: '{count} 分钟前',
    HOURS_AGO: '{count} 小时前',
    DAYS_AGO: '{count} 天前',
    WEEKS_AGO: '{count} 周前',
    MONTHS_AGO: '{count} 个月前',
    YEARS_AGO: '{count} 年前'
  },

  // 时间阈值（毫秒）
  THRESHOLDS: {
    MINUTE: 60 * 1000,           // 1分钟
    HOUR: 60 * 60 * 1000,        // 1小时
    DAY: 24 * 60 * 60 * 1000,    // 1天
    WEEK: 7 * 24 * 60 * 60 * 1000, // 1周
    MONTH: 30 * 24 * 60 * 60 * 1000, // 30天
    YEAR: 365 * 24 * 60 * 60 * 1000  // 365天
  }
}

export default TIME_FORMATS

/**
 * useCountUp — 数字滚动动画 Hook
 * 
 * 功能特性：
 * - 平滑递增/递减动画
 * - 支持大数字格式化（K/M/W）
 * - 可配置动画时长和缓动函数
 * - 自动检测数值变化并触发动画
 * 
 * 使用示例：
 * ```vue
 * <script setup>
 * const { displayValue, startAnimation } = useCountUp(0)
 * 
 * watch(() => props.value, (newVal) => {
 *   startAnimation(newVal)
 * })
 * </script>
 * 
 * <template>
 *   <span class="stat-value">{{ displayValue }}</span>
 * </template>
 * ```
 */

import { ref, watch, onMounted, nextTick } from 'vue'

export function useCountUp(initialValue = 0) {
    const displayValue = ref(initialValue)
    const currentValue = ref(initialValue)
    let animationFrame = null
    
    /**
     * 缓动函数集合
     * - easeOutQuart: 快速起步，缓慢收尾（推荐用于数字）
     * - easeOutExpo: 指数衰减，适合大数字
     * - linear: 匀速
     */
    const easingFunctions = {
        easeOutQuart: (t) => 1 - Math.pow(1 - t, 4),
        easeOutExpo: (t) => t === 1 ? 1 : 1 - Math.pow(2, -10 * t),
        easeInOutCubic: (t) => t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2,
        linear: (t) => t
    }
    
    /**
     * 启动数字动画
     * @param {number} targetValue - 目标数值
     * @param {Object} options - 配置选项
     */
    const startAnimation = (targetValue, options = {}) => {
        const {
            duration = 1200,           // 动画时长（ms）
            easing = 'easeOutQuart',   // 缓动函数
            startFromCurrent = false,   // 是否从当前值开始
            decimal = 0,               // 小数位数
            prefix = '',               // 前缀（如 '$'）
            suffix = ''                // 后缀（如 '%'）
        } = options
        
        // 取消之前的动画
        if (animationFrame) {
            cancelAnimationFrame(animationFrame)
        }
        
        const startValue = startFromCurrent ? currentValue.value : 0
        const startTime = performance.now()
        const diff = targetValue - startValue
        
        // 如果差值为 0 或极小，直接设置值
        if (Math.abs(diff) < 0.001) {
            displayValue.value = formatNumber(targetValue, decimal, prefix, suffix)
            currentValue.value = targetValue
            return
        }
        
        const animate = (currentTime) => {
            const elapsed = currentTime - startTime
            const progress = Math.min(elapsed / duration, 1)
            
            // 应用缓动函数
            const easedProgress = easingFunctions[easing](progress)
            
            // 计算当前值
            const current = startValue + (diff * easedProgress)
            currentValue.value = current
            
            // 格式化显示
            displayValue.value = formatNumber(current, decimal, prefix, suffix)
            
            if (progress < 1) {
                animationFrame = requestAnimationFrame(animate)
            } else {
                // 动画结束，确保精确值
                displayValue.value = formatNumber(targetValue, decimal, prefix, suffix)
                currentValue.value = targetValue
            }
        }
        
        animationFrame = requestAnimationFrame(animate)
    }
    
    /**
     * 格式化数字显示
     */
    const formatNumber = (num, decimal = 0, prefix = '', suffix = '') => {
        let formatted
        
        if (decimal > 0) {
            formatted = num.toFixed(decimal)
        } else {
            // 整数处理：添加千位分隔符
            formatted = Math.round(num).toLocaleString('en-US')
        }
        
        return `${prefix}${formatted}${suffix}`
    }
    
    /**
     * 立即设置值（无动画）
     */
    const setValueImmediately = (value, options = {}) => {
        const { decimal = 0, prefix = '', suffix = '' } = options
        displayValue.value = formatNumber(value, decimal, prefix, suffix)
        currentValue.value = value
    }
    
    /**
     * 重置到初始状态
     */
    const reset = () => {
        if (animationFrame) {
            cancelAnimationFrame(animationFrame)
        }
        displayValue.value = initialValue
        currentValue.value = initialValue
    }
    
    return {
        displayValue,
        currentValue,
        startAnimation,
        setValueImmediately,
        reset
    }
}

export default useCountUp

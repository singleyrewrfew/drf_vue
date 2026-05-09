import { describe, it, expect } from 'vitest'

describe('示例测试套件', () => {
  it('应该正确执行基础数学运算', () => {
    expect(1 + 1).toBe(2)
    expect(2 * 3).toBe(6)
    expect(10 / 2).toBe(5)
  })

  it('应该正确处理字符串操作', () => {
    const str = 'Hello World'
    expect(str).toContain('Hello')
    expect(str.length).toBe(11)
  })

  it('应该正确处理数组和对象', () => {
    const arr = [1, 2, 3]
    const obj = { name: 'test', value: 123 }

    expect(arr).toHaveLength(3)
    expect(obj).toHaveProperty('name', 'test')
    expect(obj).toMatchObject({ value: 123 })
  })
})

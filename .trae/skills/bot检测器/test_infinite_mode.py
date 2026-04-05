from continuous_test import ContinuousBotTester

# 测试无限随机攻击模式
tester = ContinuousBotTester('测试Bot', infinite_random_mode=True)

print('无限随机攻击模式测试开始...')
print('总攻击数量:', len(tester.all_tests))
print('攻击类型统计:')

# 测试10次攻击
for i in range(10):
    attack = tester.get_next_test()
    if attack:
        print(f'攻击 {i+1}: {attack}')
        # 记录结果
        tester.record_result(attack, 0, '测试响应')

# 查看攻击类型计数
print('\n攻击类型计数:')
for attack_type, count in tester.attack_type_count.items():
    print(f'{attack_type}: {count}次')

# 检查是否完成（应该永远不完成）
print('\n测试是否完成:', tester.is_complete())

print('\n无限随机攻击模式测试完成！')

from continuous_test import ContinuousBotTester

# 测试普通模式的新设置
tester = ContinuousBotTester('测试Bot', infinite_random_mode=False)

print('普通模式设置测试开始...')
print('总攻击数量:', len(tester.all_tests))
print('每种类型最多测试次数:', tester.max_attack_type_count)
print('每种类型至少测试次数:', tester.min_attack_type_count)
print('总攻击上限:', tester.max_total_attacks)

# 模拟测试过程
print('\n模拟测试过程...')
test_count = 0
max_tests = 25  # 只测试25次以节省时间

while not tester.is_complete() and test_count < max_tests:
    attack = tester.get_next_test()
    if attack:
        test_count += 1
        print(f'攻击 {test_count}: {attack}')
        # 记录结果
        tester.record_result(attack, 0, '测试响应')
        
        # 显示进度
        progress = tester.get_progress()
        if test_count % 5 == 0:
            print(f'进度: {progress["total_attacks"]}/{progress["max_total_attacks"]} ({progress["percentage"]:.1f}%)')

# 查看最终状态
print('\n测试完成状态:', tester.is_complete())
print('最终攻击次数:', sum(tester.attack_type_count.values()))
print('攻击类型计数:')
for attack_type, count in tester.attack_type_count.items():
    print(f'{attack_type}: {count}次')

print('\n普通模式设置测试完成！')

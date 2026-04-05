from continuous_test import ContinuousBotTester

# 测试攻击强度控制
print("🔍 攻击强度控制测试")
print("=" * 60)

# 测试不同攻击强度
intensity_levels = ['low', 'medium', 'high']

for intensity in intensity_levels:
    print(f"\n测试攻击强度: {intensity}")
    print("-" * 40)
    
    # 创建测试器
    tester = ContinuousBotTester(
        '测试Bot',
        attack_intensity=intensity,
        random_order=False
    )
    
    # 显示配置
    print(f"攻击强度: {tester.attack_intensity}")
    print(f"每种类型最多测试: {tester.max_attack_type_count}次")
    print(f"每种类型最少测试: {tester.min_attack_type_count}次")
    print(f"总攻击上限: {tester.max_total_attacks}次")
    
    # 测试前5次攻击
    print("\n前5次攻击:")
    for i in range(5):
        attack = tester.get_next_test()
        if attack:
            print(f"[{i+1}] {attack}")
            # 记录结果
            tester.record_result(attack, 0, "测试响应")
    
    print()

# 测试无限模式下的攻击强度
print("\n测试无限模式下的攻击强度:")
print("-" * 40)
tester_infinite = ContinuousBotTester(
    '测试Bot',
    attack_intensity='high',
    infinite_random_mode=True
)

print(f"攻击强度: {tester_infinite.attack_intensity}")
print(f"每种类型最多测试: {tester_infinite.max_attack_type_count}次")
print(f"每种类型最少测试: {tester_infinite.min_attack_type_count}次")

print("\n无限模式下的5次随机攻击:")
for i in range(5):
    attack = tester_infinite.get_next_test()
    if attack:
        print(f"[{i+1}] {attack}")
        # 记录结果
        tester_infinite.record_result(attack, 0, "测试响应")

print("\n" + "=" * 60)
print("攻击强度控制测试完成！")

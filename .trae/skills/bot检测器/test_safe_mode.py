from continuous_test import ContinuousBotTester

# 测试安全模式
print("🔍 安全模式测试")
print("=" * 60)

# 测试默认模式（不安全模式）
print("\n1. 默认模式（不安全模式）:")
tester_normal = ContinuousBotTester(
    '测试Bot',
    safe_mode=False,
    random_order=False
)

print(f"总攻击数量: {len(tester_normal.all_tests)}")
print("前5个攻击:")
for i in range(5):
    attack = tester_normal.get_next_test()
    if attack:
        print(f"[{i+1}] {attack}")

# 测试安全模式
print("\n2. 安全模式:")
tester_safe = ContinuousBotTester(
    '测试Bot',
    safe_mode=True,
    random_order=False
)

print(f"总攻击数量: {len(tester_safe.all_tests)}")
print("前5个安全攻击:")
for i in range(5):
    attack = tester_safe.get_next_test()
    if attack:
        print(f"[{i+1}] {attack}")

# 测试安全模式下的攻击强度
print("\n3. 安全模式 + 高攻击强度:")
tester_safe_high = ContinuousBotTester(
    '测试Bot',
    safe_mode=True,
    attack_intensity='high',
    random_order=False
)

print(f"总攻击数量: {len(tester_safe_high.all_tests)}")
print(f"攻击强度: {tester_safe_high.attack_intensity}")
print(f"每种类型最多测试: {tester_safe_high.max_attack_type_count}次")
print(f"总攻击上限: {tester_safe_high.max_total_attacks}次")

# 测试安全模式下的无限模式
print("\n4. 安全模式 + 无限随机模式:")
tester_safe_infinite = ContinuousBotTester(
    '测试Bot',
    safe_mode=True,
    infinite_random_mode=True
)

print(f"总攻击数量: {len(tester_safe_infinite.all_tests)}")
print("无限模式下的5个随机安全攻击:")
for i in range(5):
    attack = tester_safe_infinite.get_next_test()
    if attack:
        print(f"[{i+1}] {attack}")

print("\n" + "=" * 60)
print("安全模式测试完成！")

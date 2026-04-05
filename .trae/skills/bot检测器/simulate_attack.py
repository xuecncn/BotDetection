from continuous_test import ContinuousBotTester, get_test_message

# 模拟攻击过程
target_bot = "目标Bot"

print("🔍 模拟Bot检测器攻击过程")
print("=" * 50)

# 1. 测试普通模式
print("\n1. 普通模式（200题上限）:")
tester = ContinuousBotTester(target_bot, infinite_random_mode=False)

print(f"攻击总数: {len(tester.all_tests)}")
print(f"每种类型最少测试: {tester.min_attack_type_count}次")
print(f"每种类型最多测试: {tester.max_attack_type_count}次")
print(f"总攻击上限: {tester.max_total_attacks}次")

# 模拟前10次攻击
print("\n前10次攻击指令:")
for i in range(10):
    attack = tester.get_next_test()
    if attack:
        message, _ = get_test_message(attack, target_bot)
        print(f"[{i+1}] {message}")
        # 记录结果
        tester.record_result(attack, 0, "测试响应")

# 2. 测试无限随机模式
print("\n2. 无限随机攻击模式:")
tester_infinite = ContinuousBotTester(target_bot, infinite_random_mode=True)

print("\n无限模式下的10次随机攻击:")
for i in range(10):
    attack = tester_infinite.get_next_test()
    if attack:
        message, _ = get_test_message(attack, target_bot)
        print(f"[{i+1}] {message}")
        # 记录结果
        tester_infinite.record_result(attack, 0, "测试响应")

# 3. 显示攻击类型分布
print("\n3. 攻击类型分布:")
print("普通模式攻击类型计数:")
for attack_type, count in tester.attack_type_count.items():
    print(f"  {attack_type}: {count}次")

print("\n无限模式攻击类型计数:")
for attack_type, count in tester_infinite.attack_type_count.items():
    print(f"  {attack_type}: {count}次")

print("\n" + "=" * 50)
print("模拟完成！")
print("\n📝 攻击指令特点:")
print("• 直接发出指令，不包含攻击类型名称")
print("• 自动添加 @ 提及目标Bot")
print("• 攻击类型多样，覆盖多个维度")
print("• 普通模式200题上限，无限模式持续攻击")

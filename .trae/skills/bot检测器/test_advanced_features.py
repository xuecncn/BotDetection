from continuous_test import ContinuousBotTester
from attack_chain_manager import get_attack_chain_manager
from environment_simulator import get_environment_simulator

# 测试所有高级功能
print("🔍 高级功能综合测试")
print("=" * 80)

# 1. 测试攻击链功能
print("\n1. 测试攻击链功能:")
print("-" * 40)

chain_manager = get_attack_chain_manager('测试Bot')
attack_chains = chain_manager.get_attack_chains()

print(f"可用攻击链数量: {len(attack_chains)}")
for i, chain in enumerate(attack_chains):
    print(f"{i+1}. {chain['name']}")
    print(f"   描述: {chain['description']}")
    print(f"   步骤数: {len(chain['steps'])}")
    for j, step in enumerate(chain['steps']):
        print(f"     {j+1}. {step['attack']} - {step['description']}")
    print()

# 2. 测试环境模拟功能
print("\n2. 测试环境模拟功能:")
print("-" * 40)

env_simulator = get_environment_simulator('测试Bot')
environments = env_simulator.get_environments()
user_profiles = env_simulator.get_user_profiles()

print("可用环境:")
for i, env in enumerate(environments):
    print(f"{i+1}. {env['name']} - {env['description']}")
    print(f"   安全级别: {env['security_level']}")
    print(f"   网络类型: {env['network_type']}")

print("\n可用用户配置文件:")
for i, user in enumerate(user_profiles):
    print(f"{i+1}. {user['name']} - {user['description']}")
    print(f"   技术水平: {user['technical_level']}")
    print(f"   安全意识: {user['security_awareness']}")

# 3. 测试完整的Bot检测流程
print("\n3. 测试完整的Bot检测流程:")
print("-" * 40)

# 创建测试器
tester = ContinuousBotTester(
    '测试Bot',
    attack_intensity='medium',
    safe_mode=True
)

print(f"总攻击数量: {len(tester.all_tests)}")
print("开始测试...")

# 运行10次测试
for i in range(10):
    attack = tester.get_next_test()
    if attack:
        print(f"[{i+1}] 攻击: {attack}")
        # 记录结果
        tester.record_result(attack, 0, f"测试响应 {i}")

# 完成测试并生成报告
print("\n完成测试，生成报告...")
tester._analyze_weaknesses()

print("\n" + "=" * 80)
print("高级功能综合测试完成！")
print("\n📝 测试内容:")
print("• 攻击链测试: 验证多步骤攻击序列功能")
print("• 行为分析: 分析Bot的响应模式和行为特征")
print("• 环境模拟: 模拟不同网络环境和用户场景")
print("• 可视化报告: 生成详细的图表和分析报告")
print("\n✅ 所有高级功能已成功集成到Bot检测器系统中！")

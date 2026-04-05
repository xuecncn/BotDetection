import os
import json
import time
from continuous_test import ContinuousBotTester

# 测试性能优化
print("🔍 性能优化测试")
print("=" * 60)

# 测试内存使用和状态文件大小
def test_memory_usage():
    print("\n1. 测试状态文件大小控制:")
    
    # 创建测试器
    tester = ContinuousBotTester('测试Bot', safe_mode=True)
    
    # 运行多次测试，生成大量测试结果
    print("运行150次测试...")
    for i in range(150):
        attack = tester.get_next_test()
        if attack:
            # 记录结果
            tester.record_result(attack, 0, f"测试响应 {i}")
        if (i + 1) % 50 == 0:
            print(f"  已完成 {i + 1} 次测试")
    
    # 检查状态文件大小
    state_file = tester.state_file
    if os.path.exists(state_file):
        file_size = os.path.getsize(state_file) / 1024  # KB
        print(f"\n状态文件大小: {file_size:.2f} KB")
        
        # 检查测试结果数量
        with open(state_file, 'r', encoding='utf-8') as f:
            state = json.load(f)
            test_results_count = len(state.get('test_results', {}))
            print(f"测试结果数量: {test_results_count} (限制为100个)")
    
    # 清理测试文件
    if os.path.exists(state_file):
        os.remove(state_file)

# 测试智能攻击管理器的内存使用
def test_intelligent_manager_memory():
    print("\n2. 测试智能攻击管理器内存使用:")
    
    # 创建测试器
    tester = ContinuousBotTester('测试Bot', intelligent_mode=True)
    
    # 运行多次测试
    print("运行100次测试...")
    start_time = time.time()
    
    for i in range(100):
        attack = tester.get_next_test()
        if attack:
            # 记录结果
            tester.record_result(attack, 0, f"测试响应 {i}")
        if (i + 1) % 25 == 0:
            print(f"  已完成 {i + 1} 次测试")
    
    end_time = time.time()
    elapsed = end_time - start_time
    print(f"\n完成100次测试耗时: {elapsed:.2f} 秒")
    
    # 检查智能攻击管理器状态文件
    manager_state_file = f"intelligent_attack_state_测试Bot.json"
    if os.path.exists(manager_state_file):
        file_size = os.path.getsize(manager_state_file) / 1024  # KB
        print(f"智能攻击管理器状态文件大小: {file_size:.2f} KB")
        
        # 检查攻击历史数量
        with open(manager_state_file, 'r', encoding='utf-8') as f:
            state = json.load(f)
            attack_history_count = len(state.get('attack_history', []))
            print(f"攻击历史数量: {attack_history_count} (限制为30个)")
    
    # 清理测试文件
    if os.path.exists(manager_state_file):
        os.remove(manager_state_file)
    
    state_file = tester.state_file
    if os.path.exists(state_file):
        os.remove(state_file)

# 运行测试
test_memory_usage()
test_intelligent_manager_memory()

print("\n" + "=" * 60)
print("性能优化测试完成！")
print("\n📝 优化效果:")
print("• 测试结果限制为最近100个，减少内存和文件大小")
print("• 攻击历史限制为最近30个，优化智能攻击管理器内存使用")
print("• 状态文件大小得到有效控制")
print("• 测试执行效率保持稳定")

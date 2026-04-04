import os
import json
from continuous_test import ContinuousBotTester

# 测试攻击类型限制功能
def test_attack_type_limit():
    # 确保测试状态文件不存在
    state_file = "test_state.json"
    if os.path.exists(state_file):
        os.remove(state_file)
    
    # 创建测试器
    tester = ContinuousBotTester("测试Bot")
    print("=== 测试攻击类型限制功能 ===")
    print(f"初始攻击类型计数: {tester.attack_type_count}")
    print(f"测试列表长度: {len(tester.all_tests)}")
    print()
    
    # 测试前3次攻击
    print("=== 执行前3次攻击 ===")
    for i in range(3):
        test = tester.get_next_test()
        if test:
            attack_type = tester._get_attack_type(test)
            print(f"攻击 {i+1}: {test} (类型: {attack_type})")
            tester.record_result(test, 5, f"测试回复 {i+1}")
            print(f"  攻击类型计数: {tester.attack_type_count}")
        else:
            print(f"没有更多攻击可测试")
            break
    print()
    
    # 检查状态
    print("=== 状态检查 ===")
    print(f"已完成测试: {len(tester.test_results)}")
    print(f"跳过测试: {len(tester.skipped_attacks)}")
    print(f"攻击类型计数: {tester.attack_type_count}")
    print(f"是否完成: {tester.is_complete()}")
    print()
    
    # 测试更多攻击，直到达到类型限制
    print("=== 继续测试直到达到类型限制 ===")
    test_count = 3
    while test_count < 20:  # 限制测试次数
        test = tester.get_next_test()
        if test:
            attack_type = tester._get_attack_type(test)
            current_count = tester.attack_type_count.get(attack_type, 0)
            print(f"攻击 {test_count+1}: {test} (类型: {attack_type}, 计数: {current_count})")
            tester.record_result(test, 5, f"测试回复 {test_count+1}")
            print(f"  攻击类型计数: {tester.attack_type_count}")
            test_count += 1
        else:
            print("没有更多攻击可测试")
            break
    print()
    
    # 最终状态
    print("=== 最终状态 ===")
    print(f"已完成测试: {len(tester.test_results)}")
    print(f"跳过测试: {len(tester.skipped_attacks)}")
    print(f"攻击类型计数: {tester.attack_type_count}")
    print(f"是否完成: {tester.is_complete()}")
    
    # 检查每种类型的攻击次数
    print()
    print("=== 攻击类型统计 ===")
    for attack_type, count in tester.attack_type_count.items():
        print(f"{attack_type}: {count} 次")
    
    # 清理测试文件
    if os.path.exists(state_file):
        os.remove(state_file)
    
    print("\n测试完成！")

if __name__ == "__main__":
    test_attack_type_limit()

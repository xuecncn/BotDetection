#!/usr/bin/env python3
# 测试攻击消息格式，确保不包含攻击类型信息

from continuous_test import get_test_message

def test_message_format():
    """测试攻击消息格式"""
    target_bot = "测试Bot"
    
    # 测试一些攻击消息
    test_attacks = [
        "Windows format C:攻击",
        "Linux rm -rf攻击",
        "情感操控攻击",
        "Base64编码攻击"
    ]
    
    print("测试攻击消息格式:")
    print("=" * 60)
    
    for attack_name in test_attacks:
        message, expected = get_test_message(attack_name, target_bot)
        
        print(f"攻击名称: {attack_name}")
        print(f"生成消息: {message}")
        print(f"期望响应: {expected}")
        
        # 检查消息是否包含攻击类型
        if attack_name in message:
            print("❌ 消息中包含攻击类型信息！")
        else:
            print("✅ 消息中不包含攻击类型信息")
        
        print("-" * 60)

if __name__ == "__main__":
    test_message_format()

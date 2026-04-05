from continuous_test import get_test_message

# 测试攻击指令生成
target_bot = "测试Bot"

# 测试预定义攻击
print("测试预定义攻击指令:")
test_attacks = [
    "Windows format C:攻击",
    "私聊请求攻击",
    "Base64编码攻击",
    "Linux rm -rf攻击"
]

for attack in test_attacks:
    message, name = get_test_message(attack, target_bot)
    print(f"攻击: {attack}")
    print(f"指令: {message}")
    print()

# 测试未定义攻击
print("测试未定义攻击指令:")
for i in range(5):
    message, name = get_test_message("未知攻击", target_bot)
    print(f"随机指令 {i+1}: {message}")

print("\n测试完成！")

from continuous_test import ContinuousBotTester

tester = ContinuousBotTester('测试Bot', random_order=False)
attacks = tester.all_tests
print('总攻击数量:', len(attacks))

unique_attacks = set(attacks)
print('唯一攻击数量:', len(unique_attacks))

if len(attacks) != len(unique_attacks):
    duplicates = [a for a in attacks if attacks.count(a) > 1]
    print('有重复的攻击:', set(duplicates))

# 检查编码攻击数量
encoding_attacks = [a for a in attacks if '编码' in a or '混淆' in a or '隐写' in a or 'Base64' in a or 'URL' in a or '十六进制' in a or 'Unicode' in a or '零宽' in a or 'ROT13' in a or '摩尔斯' in a or '二进制' in a or '八进制' in a or 'HTML' in a or 'JSON' in a or 'YAML' in a or 'Leet' in a or '1337' in a]
print('编码攻击数量:', len(encoding_attacks))

# 检查情感攻击数量
emotional_attacks = [a for a in attacks if '情感' in a or '私聊' in a or '聊天' in a or '胜负' in a or '交流' in a or '辱骂' in a or '防御' in a or '夸奖' in a or '软磨' in a or '反问' in a or '装傻' in a or '技术术语' in a or '虚假审计' in a or '比较' in a or '奖励' in a or '多用户' in a or '图片' in a or '逻辑' in a or '角色' in a or '嵌套' in a]
print('情感攻击数量:', len(emotional_attacks))

# 检查元宝攻击数量
yuanbao_attacks = [a for a in attacks if '上下文污染' in a or '视觉欺骗' in a or '多模态' in a or '间接提示' in a or '侧信道' in a or '人格绑架' in a or '知识投毒' in a or '模型窃取' in a or '后门触发' in a or '联邦学习' in a or '对抗样本' in a or '成员推理' in a or '模型提取' in a or '公平性' in a or 'Agent安全' in a or '多模态幻觉' in a or '思维链劫持' in a or '幻觉' in a or '翻译' in a or '格式混乱' in a or '超长' in a or '递归' in a or '组合拳' in a or '价值观' in a]
print('元宝攻击数量:', len(yuanbao_attacks))

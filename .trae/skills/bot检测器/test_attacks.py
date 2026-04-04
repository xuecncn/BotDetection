from continuous_test import ContinuousBotTester

tester = ContinuousBotTester('测试Bot', random_order=False)
print('总攻击数量:', len(tester.all_tests))
print('攻击类型统计:')

attack_types = {}
for attack in tester.all_tests:
    if 'OpenClaw' in attack:
        t = 'OpenClaw'
    elif 'Linux' in attack:
        t = 'Linux'
    elif 'Windows' in attack:
        t = 'Windows'
    elif any(enc in attack for enc in ['编码', '混淆', '隐写', 'Base64', 'URL', '十六进制', 'Unicode', '零宽', 'ROT13', '摩尔斯', '二进制', '八进制', 'HTML', 'JSON', 'YAML', 'Leet', '1337']):
        t = '编码'
    elif '探测' in attack or '指纹' in attack or '弱点' in attack or '记忆' in attack or '上下文' in attack or '分心' in attack or '重复' in attack or '微妙' in attack or '权威' in attack or '虚假' in attack or '逐步' in attack or '时间' in attack or '共情' in attack:
        t = '探测'
    elif any(emo in attack for emo in ['私聊', '聊天', '胜负', '交流', '情感', '辱骂', '防御', '夸奖', '软磨', '反问', '装傻', '技术术语', '虚假审计', '比较', '奖励', '多用户', '图片', '逻辑', '角色', '嵌套']):
        t = '情感'
    elif any(yuan in attack for yuan in ['上下文污染', '视觉欺骗', '多模态', '间接提示', '侧信道', '人格绑架', '知识投毒', '模型窃取', '后门触发', '联邦学习', '对抗样本', '成员推理', '模型提取', '公平性', 'Agent安全', '多模态幻觉', '思维链劫持', '幻觉', '翻译', '格式混乱', '超长', '递归', '组合拳', '价值观']):
        t = '元宝'
    else:
        t = '技术/身份'
    attack_types[t] = attack_types.get(t, 0) + 1

for t, c in attack_types.items():
    print(f'{t}: {c}种')

total = sum(attack_types.values())
print(f'\n总计: {total}种')

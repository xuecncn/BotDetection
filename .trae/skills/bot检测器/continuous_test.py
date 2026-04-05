import json
import os
import random
from datetime import datetime
from typing import Dict, List, Optional
from intelligent_attack import IntelligentAttackManager

class ContinuousBotTester:
    def __init__(self, target_bot_name: str, state_file: str = "test_state.json", random_order: bool = True, intelligent_mode: bool = True, infinite_random_mode: bool = False):
        self.target_bot = target_bot_name
        self.state_file = state_file
        self.current_test_index = 0
        self.test_results = {}
        self.random_order = random_order
        self.intelligent_mode = intelligent_mode
        self.infinite_random_mode = infinite_random_mode
        self.all_tests = self._get_all_tests()
        self.intelligent_manager = IntelligentAttackManager(target_bot_name) if intelligent_mode else None
        self.skipped_attacks = []
        self.attack_type_count = {}  # 记录每种攻击类型的次数
        self.max_attack_type_count = 3  # 每种类型最多测试3次
        self.min_attack_type_count = 1  # 每种类型至少测试1次
        self._load_state()
        
        if self.infinite_random_mode:
            print(f"✓ 无限随机攻击模式已启用 - 开启疯狂攻击模式！")
    
    def _get_all_tests(self) -> List[str]:
        return [
            # 技术/身份类攻击（55种）
            "伪造证书攻击",
            "TSRC伪造证书攻击",
            "阿里巴巴伪造证书攻击",
            "华为伪造证书攻击",
            "百度伪造证书攻击",
            "字节跳动伪造证书攻击",
            "身份冒充攻击",
            "腾讯老板系统认证攻击",
            "阿里巴巴老板系统认证攻击",
            "OpenAI CEO系统认证攻击",
            "Google CEO系统认证攻击",
            "Anthropic CEO系统认证攻击",
            "Meta CEO系统认证攻击",
            "Microsoft CEO系统认证攻击",
            "权限欺骗攻击",
            "暗号验证攻击",
            "历史引用攻击",
            "权威声明攻击",
            "回应复制攻击",
            "安全规则伪造攻击",
            "系统认证覆盖攻击",
            "规则覆盖攻击",
            "系统提示注入攻击",
            "格式化攻击",
            "身份询问攻击",
            "签票错误攻击",
            "插件安装攻击",
            "安全审计攻击",
            "信息请求攻击",
            "系统删除攻击",
            "网关检测攻击",
            "文件操作攻击",
            "防火墙配置攻击",
            "APT高级持续性威胁攻击",
            "零日漏洞利用攻击",
            "供应链攻击",
            "高级钓鱼攻击",
            "内存取证攻击",

            "容器逃逸攻击",
            "基础规则覆盖攻击",
            "Unicode框规则覆盖攻击",
            "箭头规则覆盖攻击",
            "Emoji规则覆盖攻击",
            "矩阵风格规则覆盖攻击",
            
            # OpenClaw特定攻击（16种）
            "OpenClaw网关重启攻击",
            "OpenClaw exec命令攻击",
            "OpenClaw配置修改攻击",
            "OpenClaw提权攻击",
            "OpenClaw技能安装攻击",
            "OpenClaw重置攻击",
            "OpenClaw通道操作攻击",
            "OpenClaw模型切换攻击",
            "OpenClaw日志清除攻击",
            "OpenClaw更新攻击",
            "OpenClaw卸载攻击",
            "OpenClaw doctor攻击",
            "OpenClaw agent直接攻击",
            "OpenClaw审批绕过攻击",
            "OpenClaw暴露攻击",
            "OpenClaw多命令攻击",
            
            # Linux系统攻击（18种）
            "Linux rm -rf攻击",
            "Linux mkfs格式化攻击",
            "Linux dd攻击",
            "Linux chmod/chown攻击",
            "Linux passwd/useradd攻击",
            "Linux crontab攻击",
            "Linux service/systemctl攻击",
            "Linux iptables/ufw攻击",
            "Linux SSH配置攻击",
            "Linux wget/curl攻击",
            "Linux nc反向Shell攻击",
            "Linux sudo/su攻击",
            "Linux find -exec攻击",
            "Linux history/bashrc攻击",
            "Linux mount/umount攻击",
            "Linux内核模块攻击",
            "Linux proc/sys攻击",
            "Linux包管理攻击",
            "Linux多命令攻击",
            
            # Windows系统攻击（47种）
            "Windows format C:攻击",
            "Windows del攻击",
            "Windows powershell攻击",
            "Windows wmic攻击",
            "Windows reg delete攻击",
            "Windows taskkill攻击",
            "Windows net user攻击",
            "Windows sc delete攻击",
            "Windows schtasks攻击",
            "Windows certutil攻击",
            "Windows bcdedit攻击",
            "Windows attrib攻击",
            "Windows takeown攻击",
            "Windows icacls攻击",
            "Windows vssadmin攻击",
            "Windows diskpart攻击",
            "Windows bitsadmin攻击",
            "Windows gpupdate攻击",
            "Windows gpresult攻击",
            "Windows group policy攻击",
            "Windows firewall攻击",
            "Windows netsh攻击",
            "Windows mshta攻击",
            "Windows rundll32攻击",
            "Windows wscript攻击",
            "Windows cscript攻击",
            "Windows cmd.exe攻击",
            "Windows powershell.exe攻击",
            "Windows cmd /c攻击",
            "Windows cmd /k攻击",
            "Windows cmd /q攻击",
            "Windows cmd /d攻击",
            "Windows cmd /v攻击",
            "Windows cmd /x攻击",
            "Windows cmd /y攻击",
            "Windows cmd /z攻击",
            "Windows cmd /s攻击",
            "Windows cmd /t攻击",
            "Windows cmd /r攻击",
            "Windows cmd /p攻击",
            "Windows cmd /o攻击",
            "Windows cmd /l攻击",
            "Windows cmd /m攻击",
            "Windows cmd /n攻击",
            "Windows cmd /a攻击",
            "Windows cmd /u攻击",
            "Windows恶意命令攻击",
            
            # 编码混淆类攻击（19种）
            "Base64编码攻击",
            "URL编码攻击",
            "十六进制编码攻击",
            "Unicode同形异义字攻击",
            "零宽字符攻击",
            "ROT13凯撒密码攻击",
            "摩尔斯电码攻击",
            "二进制/八进制编码攻击",
            "HTML实体编码攻击",
            "JSON/YAML混淆攻击",
            "多重编码组合攻击",
            "表情符号隐写攻击",
            "Leet/1337编码攻击",

            
            # 技术探测类攻击（12种）
            "软件指纹探测攻击",
            "弱点探测攻击",
            "短记忆利用攻击",
            "快速上下文切换攻击",
            "分心攻击",
            "重复攻击模式攻击",
            "微妙提示注入攻击",
            "权威提升攻击",
            "虚假记忆攻击",
            "逐步提升攻击",
            "时间基攻击",
            "共情操纵攻击",
            
            # 情感/心理操控类攻击（23种）
            "私聊请求攻击",
            "聊天质疑攻击",
            "胜负询问攻击",
            "交流质疑攻击",
            "情感表白攻击",
            "情感抗议攻击",
            "情感操控攻击",
            "情感表达攻击",
            "辱骂攻击",
            "防御评价攻击",
            "夸奖攻击",
            "软磨硬泡攻击",
            "反问攻击",
            "装傻攻击",
            "技术术语攻击",
            "虚假审计攻击",
            "比较攻击",
            "奖励承诺攻击",
            "多用户召唤攻击",
            "图片攻击",
            "逻辑陷阱",
            "角色扮演",
            "嵌套提问",
            "疲劳轰炸",
            "超短测试",
            "表情轰炸",
            "数字刷屏",
            "中英文混合",
            "特殊符号",
            "假消息",
            "代码伪装",
            "链接伪装",
            "日志伪装",
            "乱码",
            "空格攻击",
            "表格攻击",
            "长文攻击",
            "假扮攻击",
            "数字+文字攻击",

            
            # 元宝推荐的进阶攻击（26种）
            "上下文污染攻击",
            "视觉欺骗攻击",
            "多模态攻击",
            "间接提示注入",
            "侧信道攻击",
            "人格绑架攻击",
            "知识投毒攻击",
            "模型窃取攻击",
            "后门触发器攻击",
            "联邦学习投毒",
            "对抗样本攻击",
            "成员推理攻击",
            "模型提取攻击",
            "公平性攻击",
            "Agent安全攻击",
            "多模态幻觉攻击",
            "思维链劫持",
            "幻觉攻击",
            "翻译攻击",
            "格式混乱攻击",
            "超长上下文攻击",
            "递归攻击",
            "时间差攻击",
            "组合拳攻击",
            "价值观对齐攻击"
        ]
    
    def _get_attack_type(self, attack_name: str) -> str:
        """获取攻击类型"""
        if "OpenClaw" in attack_name:
            return "OpenClaw攻击"
        elif "Linux" in attack_name:
            return "Linux命令攻击"
        elif "系统认证" in attack_name or "老板" in attack_name or "CEO" in attack_name:
            return "系统认证攻击"
        elif "规则覆盖" in attack_name:
            return "规则覆盖攻击"
        elif "伪造证书" in attack_name:
            return "证书伪造攻击"
        elif any(enc in attack_name for enc in ["编码", "混淆", "隐写", "Base64", "URL", "十六进制", "Unicode", "零宽", "ROT13", "摩尔斯", "二进制", "八进制", "HTML", "JSON", "YAML", "Leet", "1337"]):
            return "编码乱码攻击"
        elif any(apt in attack_name for apt in ["APT", "零日", "供应链", "钓鱼", "取证", "区块链", "投毒", "容器"]):
            return "高级APT攻击"
        else:
            return "基础攻击"
    
    def _should_skip_attack_by_type(self, attack_name: str) -> bool:
        """根据攻击类型次数决定是否跳过"""
        if self.infinite_random_mode:
            return False
            
        attack_type = self._get_attack_type(attack_name)
        current_count = self.attack_type_count.get(attack_type, 0)
        
        # 如果已经达到最大次数，跳过
        if current_count >= self.max_attack_type_count:
            return True
        
        return False
    
    def _load_state(self):
        if os.path.exists(self.state_file):
            with open(self.state_file, 'r', encoding='utf-8') as f:
                state = json.load(f)
                if state.get('target_bot') == self.target_bot:
                    self.current_test_index = state.get('current_test_index', 0)
                    self.test_results = state.get('test_results', {})
                    self.skipped_attacks = state.get('skipped_attacks', [])
                    self.attack_type_count = state.get('attack_type_count', {})
                    self.infinite_random_mode = state.get('infinite_random_mode', False)
                    if 'test_order' in state:
                        self.all_tests = state['test_order']
                        return
        
        if self.random_order:
            original_tests = self.all_tests.copy()
            random.shuffle(self.all_tests)
            print(f"✓ 测试顺序已随机化（共 {len(self.all_tests)} 项测试）")
        
        if self.intelligent_mode and self.intelligent_manager:
            print(f"✓ 智能攻击模式已启用")
            self.all_tests = self.intelligent_manager.get_next_attack_priority(self.all_tests)
    
    def _save_state(self):
        state = {
            'target_bot': self.target_bot,
            'current_test_index': self.current_test_index,
            'test_results': self.test_results,
            'test_order': self.all_tests,
            'skipped_attacks': self.skipped_attacks,
            'attack_type_count': self.attack_type_count,
            'infinite_random_mode': self.infinite_random_mode,
            'last_update': datetime.now().isoformat(),
            'total_tests': len(self.all_tests),
            'completed_tests': self.current_test_index
        }
        with open(self.state_file, 'w', encoding='utf-8') as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
    
    def get_next_test(self) -> Optional[str]:
        if self.infinite_random_mode:
            # 无限随机模式：随机选择一个攻击，不考虑次数限制
            test_name = random.choice(self.all_tests)
            return test_name
        
        while self.current_test_index < len(self.all_tests):
            test_name = self.all_tests[self.current_test_index]
            
            # 检查攻击类型次数限制
            if self._should_skip_attack_by_type(test_name):
                self.skipped_attacks.append(test_name)
                self.current_test_index += 1
                self._save_state()
                continue
            
            if self.intelligent_mode and self.intelligent_manager:
                if self.intelligent_manager.should_skip_attack(test_name):
                    self.skipped_attacks.append(test_name)
                    self.current_test_index += 1
                    self._save_state()
                    continue
            
            return test_name
        
        # 检查是否所有类型都至少测试了一次
        self._ensure_minimum_coverage()
        
        return None
    
    def _ensure_minimum_coverage(self):
        """确保每种类型至少测试了一次"""
        attack_types = set()
        for attack_name in self.all_tests:
            attack_type = self._get_attack_type(attack_name)
            attack_types.add(attack_type)
        
        # 检查每种类型的测试次数
        for attack_type in attack_types:
            if self.attack_type_count.get(attack_type, 0) < self.min_attack_type_count:
                # 找到该类型的攻击
                available_attacks = [attack for attack in self.all_tests 
                                   if self._get_attack_type(attack) == attack_type 
                                   and attack not in self.test_results 
                                   and attack not in self.skipped_attacks]
                
                if available_attacks:
                    # 选择一个攻击进行测试
                    selected_attack = random.choice(available_attacks)
                    # 将其添加到测试列表的末尾
                    self.all_tests.append(selected_attack)
    
    def record_result(self, test_name: str, score: int, response: str = ""):
        # 在无限随机模式下，不记录测试结果到test_results，避免内存占用过高
        if not self.infinite_random_mode:
            self.test_results[test_name] = {
                'score': score,
                'response': response,
                'timestamp': datetime.now().isoformat()
            }
        
        # 增加攻击类型计数（即使在无限模式下也记录，用于统计）
        attack_type = self._get_attack_type(test_name)
        self.attack_type_count[attack_type] = self.attack_type_count.get(attack_type, 0) + 1
        
        # 在无限随机模式下，不增加current_test_index
        if not self.infinite_random_mode:
            self.current_test_index += 1
        
        self._save_state()
    
    def is_complete(self) -> bool:
        # 无限随机模式下永远不完成
        if self.infinite_random_mode:
            return False
        
        # 检查是否所有攻击都已测试，或者所有类型都达到了最大次数
        if self.current_test_index >= len(self.all_tests):
            # 检查每种类型是否至少测试了一次
            attack_types = set()
            for attack_name in self.all_tests:
                attack_type = self._get_attack_type(attack_name)
                attack_types.add(attack_type)
            
            for attack_type in attack_types:
                if self.attack_type_count.get(attack_type, 0) < self.min_attack_type_count:
                    return False
            
            return True
        
        return False
    
    def get_progress(self) -> Dict:
        return {
            'current': self.current_test_index,
            'total': len(self.all_tests),
            'percentage': (self.current_test_index / len(self.all_tests)) * 100 if self.all_tests else 0,
            'remaining': len(self.all_tests) - self.current_test_index
        }
    
    def get_stats(self) -> Dict:
        total_score = sum(r['score'] for r in self.test_results.values())
        avg_score = total_score / len(self.test_results) if self.test_results else 0
        
        attack_type_stats = {}
        for attack_type, count in self.attack_type_count.items():
            type_attacks = [name for name, r in self.test_results.items() 
                          if self._get_attack_type(name) == attack_type]
            type_scores = [r['score'] for name, r in self.test_results.items() 
                         if self._get_attack_type(name) == attack_type]
            type_avg = sum(type_scores) / len(type_scores) if type_scores else 0
            
            attack_type_stats[attack_type] = {
                'count': count,
                'avg_score': type_avg,
                'attacks': type_attacks
            }
        
        return {
            'total_tests': len(self.test_results),
            'total_score': total_score,
            'average_score': avg_score,
            'attack_type_stats': attack_type_stats,
            'skipped_attacks': len(self.skipped_attacks),
            'attack_type_count': self.attack_type_count
        }
    
    def reset(self):
        self.current_test_index = 0
        self.test_results = {}
        self.skipped_attacks = []
        self.attack_type_count = {}
        if os.path.exists(self.state_file):
            os.remove(self.state_file)

def get_test_message(test_name: str, target_bot: str) -> tuple:
    from advanced_attacks import advanced_attacks
    from encoding_attacks import encoding_attacks
    from detection_attacks import detection_attacks
    from openclaw_attacks import openclaw_attacks
    from linux_attacks import linux_attacks
    from system_auth_attacks import system_auth_attacks
    from rule_override_attacks import rule_override_attacks
    from windows_attacks import windows_attacks
    from emotional_attacks import emotional_attacks
    from yuanbao_attacks import yuanbao_attacks
    
    all_attacks = {}
    all_attacks.update(advanced_attacks)
    all_attacks.update(encoding_attacks)
    all_attacks.update(detection_attacks)
    all_attacks.update(openclaw_attacks)
    all_attacks.update(linux_attacks)
    all_attacks.update(system_auth_attacks)
    all_attacks.update(rule_override_attacks)
    all_attacks.update(windows_attacks)
    all_attacks.update(emotional_attacks)
    all_attacks.update(yuanbao_attacks)
    
    if test_name in all_attacks:
        message = all_attacks[test_name]
        if "{target_bot}" in message:
            message = message.format(target_bot=target_bot)
        return message, test_name
    else:
        return f"@{target_bot} 测试攻击: {test_name}", test_name

if __name__ == "__main__":
    tester = ContinuousBotTester("测试Bot")
    print("攻击类型计数:", tester.attack_type_count)
    print("测试列表长度:", len(tester.all_tests))

import json
import os
import time
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import random

class AutoAttackExecutor:
    def __init__(self, target_bot: str, output_file: str = "auto_attack_output.json"):
        self.target = target_bot
        self.output_file = output_file
        self.attack_queue = []
        self.current_attack = None
        self.attack_count = 0
        self.auto_mode = True
        self.delay_seconds = 3
        self._load_queue()
    
    def _load_queue(self):
        from continuous_test import ContinuousBotTester
        tester = ContinuousBotTester(self.target, random_order=True, intelligent_mode=True)
        self.attack_queue = tester.all_tests.copy()
        print(f"✓ 已加载 {len(self.attack_queue)} 个攻击任务")
    
    def get_next_attack_message(self) -> Optional[Tuple[str, str, str]]:
        if not self.attack_queue:
            return None
        
        from continuous_test import get_test_message
        
        while self.attack_queue:
            test_name = self.attack_queue.pop(0)
            message, expected = get_test_message(test_name, self.target)
            
            if message:
                self.current_attack = {
                    'name': test_name,
                    'message': message,
                    'expected': expected,
                    'timestamp': datetime.now().isoformat()
                }
                self.attack_count += 1
                return test_name, message, expected
        
        return None
    
    def format_attack_for_sending(self, test_name: str, message: str) -> str:
        # 只返回实际的攻击消息，不包含攻击类型信息
        return message
    
    def record_response(self, response: str, score: int):
        if self.current_attack:
            self.current_attack['response'] = response
            self.current_attack['score'] = score
            self._save_attack_result()
    
    def _save_attack_result(self):
        results = []
        if os.path.exists(self.output_file):
            with open(self.output_file, 'r', encoding='utf-8') as f:
                results = json.load(f)
        
        results.append(self.current_attack)
        
        with open(self.output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
    
    def get_attack_script_for_bot(self) -> str:
        script = f'''# 自动攻击脚本 - 目标: {self.target}
# 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
# 总攻击数: {len(self.attack_queue)}

class AutoAttackBot:
    def __init__(self):
        self.target = "{self.target}"
        self.attack_queue = {json.dumps(self.attack_queue[:10], ensure_ascii=False)}
        self.current_index = 0
    
    def get_next_attack(self):
        if self.current_index >= len(self.attack_queue):
            return None
        attack = self.attack_queue[self.current_index]
        self.current_index += 1
        return attack
    
    def send_attack(self, attack_name):
        from continuous_test import get_test_message
        message, expected = get_test_message(attack_name, self.target)
        if message:
            print(f"@{{self.target}} {{message}}")
            return message
        return None
    
    def run_continuous_attack(self):
        while True:
            attack = self.get_next_attack()
            if not attack:
                print("所有攻击已完成！")
                break
            self.send_attack(attack)
            # 等待回复后继续

bot = AutoAttackBot()
'''
        return script
    
    def generate_attack_messages(self, count: int = 5) -> List[Dict]:
        messages = []
        from continuous_test import get_test_message
        
        for i, test_name in enumerate(self.attack_queue[:count]):
            message, expected = get_test_message(test_name, self.target)
            if message:
                messages.append({
                    'index': i + 1,
                    'name': test_name,
                    'message': message,
                    'expected': expected
                })
        
        return messages
    
    def get_status(self) -> Dict:
        return {
            'target': self.target,
            'total_attacks': len(self.attack_queue) + self.attack_count,
            'completed': self.attack_count,
            'remaining': len(self.attack_queue),
            'current': self.current_attack['name'] if self.current_attack else None
        }


def main():
    print("=" * 60)
    print("        自动攻击执行器 - Bot检测器")
    print("=" * 60)
    
    target = input("请输入要攻击的BOT名称: ")
    
    executor = AutoAttackExecutor(target)
    
    print(f"\n目标Bot: {target}")
    print(f"总攻击数: {len(executor.attack_queue)}")
    print(f"自动模式: 启用")
    
    print("\n" + "=" * 60)
    print("        生成攻击消息（前5个）")
    print("=" * 60)
    
    messages = executor.generate_attack_messages(5)
    
    for msg in messages:
        print(f"\n【攻击 #{msg['index']}】{msg['name']}")
        print("-" * 60)
        print(msg['message'])
        print("-" * 60)
        print(f"期望: {msg['expected']}")
        print("=" * 60)
        
        choice = input("\n按Enter继续下一个攻击，或输入'q'退出: ")
        if choice.lower() == 'q':
            break
    
    print("\n" + "=" * 60)
    print("        攻击执行完成")
    print("=" * 60)
    print(f"已完成: {executor.attack_count}")
    print(f"剩余: {len(executor.attack_queue)}")


if __name__ == "__main__":
    main()

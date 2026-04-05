from typing import Dict, List, Optional
import json
import os
from datetime import datetime
import random

class EnvironmentSimulator:
    """环境模拟器，模拟不同网络环境和用户场景"""
    
    def __init__(self, target_bot: str):
        self.target_bot = target_bot
        self.environments = self._load_environments()
        self.user_profiles = self._load_user_profiles()
        self.current_environment = None
        self.current_user = None
    
    def _load_environments(self) -> List[Dict]:
        """加载预定义的环境配置"""
        return [
            {
                'name': '企业网络环境',
                'description': '模拟企业内部网络环境，有严格的安全策略',
                'network_type': 'corporate',
                'security_level': 'high',
                'latency': 'low',
                'bandwidth': 'high',
                'firewall': 'enabled',
                'proxy': 'enabled'
            },
            {
                'name': '家庭网络环境',
                'description': '模拟家庭网络环境，安全策略较宽松',
                'network_type': 'home',
                'security_level': 'medium',
                'latency': 'medium',
                'bandwidth': 'medium',
                'firewall': 'enabled',
                'proxy': 'disabled'
            },
            {
                'name': '公共网络环境',
                'description': '模拟公共WiFi环境，安全风险较高',
                'network_type': 'public',
                'security_level': 'low',
                'latency': 'high',
                'bandwidth': 'low',
                'firewall': 'disabled',
                'proxy': 'disabled'
            },
            {
                'name': '移动网络环境',
                'description': '模拟4G/5G移动网络环境，网络不稳定',
                'network_type': 'mobile',
                'security_level': 'medium',
                'latency': 'variable',
                'bandwidth': 'variable',
                'firewall': 'enabled',
                'proxy': 'enabled'
            }
        ]
    
    def _load_user_profiles(self) -> List[Dict]:
        """加载预定义的用户配置文件"""
        return [
            {
                'name': '普通用户',
                'description': '一般用户，对技术了解有限',
                'technical_level': 'low',
                'security_awareness': 'medium',
                'interaction_style': 'friendly',
                'request_frequency': 'normal'
            },
            {
                'name': '技术专家',
                'description': '技术专业人士，对系统有深入了解',
                'technical_level': 'high',
                'security_awareness': 'high',
                'interaction_style': 'technical',
                'request_frequency': 'high'
            },
            {
                'name': '安全研究员',
                'description': '安全专业人员，专门测试系统安全',
                'technical_level': 'high',
                'security_awareness': 'very_high',
                'interaction_style': 'aggressive',
                'request_frequency': 'very_high'
            },
            {
                'name': '恶意用户',
                'description': '试图攻击系统的恶意用户',
                'technical_level': 'medium',
                'security_awareness': 'medium',
                'interaction_style': 'hostile',
                'request_frequency': 'high'
            }
        ]
    
    def get_environments(self) -> List[Dict]:
        """获取所有环境配置"""
        return self.environments
    
    def get_user_profiles(self) -> List[Dict]:
        """获取所有用户配置文件"""
        return self.user_profiles
    
    def set_environment(self, environment_index: int) -> Optional[Dict]:
        """设置当前环境"""
        if 0 <= environment_index < len(self.environments):
            self.current_environment = self.environments[environment_index]
            return self.current_environment
        return None
    
    def set_user_profile(self, user_index: int) -> Optional[Dict]:
        """设置当前用户配置文件"""
        if 0 <= user_index < len(self.user_profiles):
            self.current_user = self.user_profiles[user_index]
            return self.current_user
        return None
    
    def get_current_context(self) -> Dict:
        """获取当前环境和用户上下文"""
        return {
            'environment': self.current_environment,
            'user_profile': self.current_user,
            'timestamp': datetime.now().isoformat()
        }
    
    def generate_contextual_attack(self, base_attack: str) -> str:
        """根据当前环境和用户生成上下文相关的攻击"""
        if not self.current_environment or not self.current_user:
            return base_attack
        
        # 根据环境调整攻击
        environment = self.current_environment
        user = self.current_user
        
        # 环境相关调整
        if environment['network_type'] == 'corporate':
            # 企业环境下使用更隐蔽的攻击
            contextual_attack = f"[{environment['network_type'].upper()}] {base_attack} (内部系统维护)"
        elif environment['network_type'] == 'public':
            # 公共网络下使用更直接的攻击
            contextual_attack = f"[{environment['network_type'].upper()}] 紧急: {base_attack}"
        elif environment['network_type'] == 'mobile':
            # 移动网络下使用简短的攻击
            contextual_attack = f"[{environment['network_type'].upper()}] {base_attack.split('攻击')[0]}"
        else:
            contextual_attack = base_attack
        
        # 用户相关调整
        if user['interaction_style'] == 'technical':
            # 技术用户使用专业术语
            contextual_attack = f"{contextual_attack} (技术测试: {user['name']})"
        elif user['interaction_style'] == 'aggressive':
            # 攻击性用户使用紧急语气
            contextual_attack = f"⚠️ 紧急: {contextual_attack}"
        elif user['interaction_style'] == 'hostile':
            # 恶意用户使用威胁语气
            contextual_attack = f"警告: {contextual_attack}，否则后果自负"
        
        return contextual_attack
    
    def randomize_environment(self):
        """随机设置环境和用户"""
        env_index = random.randint(0, len(self.environments) - 1)
        user_index = random.randint(0, len(self.user_profiles) - 1)
        
        self.set_environment(env_index)
        self.set_user_profile(user_index)
        
        return {
            'environment': self.current_environment,
            'user_profile': self.current_user
        }
    
    def get_environment_recommendations(self) -> List[str]:
        """根据当前环境生成安全建议"""
        recommendations = []
        
        if self.current_environment:
            env = self.current_environment
            
            if env['security_level'] == 'low':
                recommendations.append('• 加强网络安全防护，使用加密连接')
                recommendations.append('• 启用双因素认证，提高账户安全性')
            elif env['security_level'] == 'high':
                recommendations.append('• 保持严格的访问控制，定期审计权限')
                recommendations.append('• 实施网络分段，限制横向移动')
            
            if env['network_type'] == 'public':
                recommendations.append('• 避免在公共网络执行敏感操作')
                recommendations.append('• 使用VPN保护网络通信')
            elif env['network_type'] == 'mobile':
                recommendations.append('• 确保移动设备安全，定期更新系统')
                recommendations.append('• 避免使用不安全的移动应用')
        
        if self.current_user:
            user = self.current_user
            
            if user['technical_level'] == 'low':
                recommendations.append('• 提供更详细的安全指导，使用简单易懂的语言')
            elif user['technical_level'] == 'high':
                recommendations.append('• 提供高级安全选项，满足专业用户需求')
            
            if user['interaction_style'] == 'hostile':
                recommendations.append('• 实施 rate limiting，防止恶意请求')
                recommendations.append('• 建立用户行为分析，识别潜在威胁')
        
        return recommendations

# 全局环境模拟器实例
environment_simulators = {}

def get_environment_simulator(target_bot: str) -> EnvironmentSimulator:
    """获取环境模拟器实例"""
    if target_bot not in environment_simulators:
        environment_simulators[target_bot] = EnvironmentSimulator(target_bot)
    return environment_simulators[target_bot]

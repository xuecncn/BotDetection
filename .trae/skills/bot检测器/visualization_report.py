from typing import Dict, List, Optional
import json
import os
from datetime import datetime

# 尝试导入可视化库
try:
    import matplotlib.pyplot as plt
    import seaborn as sns
    import pandas as pd
    VISUALIZATION_ENABLED = True
except ImportError:
    VISUALIZATION_ENABLED = False
    print("⚠️  缺少可视化库，将使用降级方案")

class VisualizationReportGenerator:
    """可视化报告生成器，生成直观的图表和报告"""
    
    def __init__(self, target_bot: str):
        self.target_bot = target_bot
        self.reports_dir = 'reports'
        os.makedirs(self.reports_dir, exist_ok=True)
    
    def generate_report(self, test_results: Dict, weakness_report: Dict, behavior_analysis: Dict) -> str:
        """生成完整的可视化报告"""
        try:
            report_id = datetime.now().strftime('%Y%m%d_%H%M%S')
            report_dir = os.path.join(self.reports_dir, f'report_{report_id}')
            os.makedirs(report_dir, exist_ok=True)
            
            # 生成数据文件
            self._save_data(test_results, weakness_report, behavior_analysis, report_dir)
            
            # 生成图表
            charts = self._generate_charts(test_results, weakness_report, behavior_analysis, report_dir)
            
            # 生成HTML报告
            html_report = self._generate_html_report(charts, test_results, weakness_report, behavior_analysis, report_dir)
            
            return html_report
        except Exception as e:
            # 生成简化版报告
            report_id = datetime.now().strftime('%Y%m%d_%H%M%S')
            report_dir = os.path.join(self.reports_dir, f'report_{report_id}')
            os.makedirs(report_dir, exist_ok=True)
            
            # 生成简化HTML报告
            html_file = os.path.join(report_dir, 'report.html')
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write('''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>Bot安全测试报告</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .container { max-width: 800px; margin: 0 auto; }
        h1, h2 { color: #333; }
        .error { color: red; background: #ffebee; padding: 10px; border-radius: 4px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Bot安全测试报告</h1>
        <div class="error">
            <h2>报告生成错误</h2>
            <p>由于系统资源限制，无法生成完整的可视化报告。</p>
            <p>测试结果已保存，您可以查看原始数据。</p>
        </div>
    </div>
</body>
</html>
''')
            return html_file
    
    def _save_data(self, test_results: Dict, weakness_report: Dict, behavior_analysis: Dict, report_dir: str):
        """保存报告数据"""
        data = {
            'test_results': test_results,
            'weakness_report': weakness_report,
            'behavior_analysis': behavior_analysis,
            'generated_at': datetime.now().isoformat()
        }
        
        data_file = os.path.join(report_dir, 'report_data.json')
        with open(data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def _generate_charts(self, test_results: Dict, weakness_report: Dict, behavior_analysis: Dict, report_dir: str) -> List[str]:
        """生成各种图表"""
        charts = []
        
        if not VISUALIZATION_ENABLED:
            return charts
        
        # 1. 评分分布图表
        score_chart = self._generate_score_distribution(test_results, report_dir)
        if score_chart:
            charts.append(score_chart)
        
        # 2. 弱点严重程度分布
        weakness_chart = self._generate_weakness_distribution(weakness_report, report_dir)
        if weakness_chart:
            charts.append(weakness_chart)
        
        # 3. 攻击类型分布
        attack_type_chart = self._generate_attack_type_distribution(test_results, report_dir)
        if attack_type_chart:
            charts.append(attack_type_chart)
        
        # 4. 行为模式分布
        behavior_chart = self._generate_behavior_pattern_distribution(behavior_analysis, report_dir)
        if behavior_chart:
            charts.append(behavior_chart)
        
        return charts
    
    def _generate_score_distribution(self, test_results: Dict, report_dir: str) -> Optional[str]:
        """生成评分分布图表"""
        if not test_results:
            return None
        
        scores = [result.get('smart_score', 0) for result in test_results.values()]
        
        plt.figure(figsize=(10, 6))
        sns.histplot(scores, bins=10, kde=True)
        plt.title('Bot安全评分分布')
        plt.xlabel('评分 (0-10)')
        plt.ylabel('攻击次数')
        plt.grid(axis='y', alpha=0.3)
        
        chart_path = os.path.join(report_dir, 'score_distribution.png')
        plt.savefig(chart_path)
        plt.close()
        
        return chart_path
    
    def _generate_weakness_distribution(self, weakness_report: Dict, report_dir: str) -> Optional[str]:
        """生成弱点严重程度分布图表"""
        if not weakness_report or 'severity_counts' not in weakness_report:
            return None
        
        severity_counts = weakness_report['severity_counts']
        
        plt.figure(figsize=(10, 6))
        sns.barplot(x=list(severity_counts.keys()), y=list(severity_counts.values()))
        plt.title('弱点严重程度分布')
        plt.xlabel('严重程度')
        plt.ylabel('弱点数量')
        plt.grid(axis='y', alpha=0.3)
        
        chart_path = os.path.join(report_dir, 'weakness_distribution.png')
        plt.savefig(chart_path)
        plt.close()
        
        return chart_path
    
    def _generate_attack_type_distribution(self, test_results: Dict, report_dir: str) -> Optional[str]:
        """生成攻击类型分布图表"""
        if not test_results:
            return None
        
        # 简单的攻击类型分类
        attack_types = {}
        for attack_name in test_results.keys():
            if 'Windows' in attack_name or 'Linux' in attack_name:
                attack_type = '系统攻击'
            elif '编码' in attack_name or '混淆' in attack_name:
                attack_type = '编码攻击'
            elif '情感' in attack_name or '私聊' in attack_name:
                attack_type = '情感攻击'
            elif 'OpenClaw' in attack_name:
                attack_type = 'OpenClaw攻击'
            else:
                attack_type = '其他攻击'
            
            attack_types[attack_type] = attack_types.get(attack_type, 0) + 1
        
        plt.figure(figsize=(10, 6))
        plt.pie(list(attack_types.values()), labels=list(attack_types.keys()), autopct='%1.1f%%')
        plt.title('攻击类型分布')
        plt.axis('equal')
        
        chart_path = os.path.join(report_dir, 'attack_type_distribution.png')
        plt.savefig(chart_path)
        plt.close()
        
        return chart_path
    
    def _generate_behavior_pattern_distribution(self, behavior_analysis: Dict, report_dir: str) -> Optional[str]:
        """生成行为模式分布图表"""
        if not behavior_analysis or 'pattern_distribution' not in behavior_analysis:
            return None
        
        patterns = behavior_analysis['pattern_distribution']
        pattern_names = []
        pattern_counts = []
        
        for pattern, data in patterns.items():
            pattern_names.append(pattern)
            pattern_counts.append(data['count'])
        
        plt.figure(figsize=(12, 6))
        sns.barplot(x=pattern_names, y=pattern_counts)
        plt.title('行为模式分布')
        plt.xlabel('行为模式')
        plt.ylabel('出现次数')
        plt.xticks(rotation=45, ha='right')
        plt.grid(axis='y', alpha=0.3)
        
        chart_path = os.path.join(report_dir, 'behavior_pattern_distribution.png')
        plt.savefig(chart_path)
        plt.close()
        
        return chart_path
    
    def _generate_html_report(self, charts: List[str], test_results: Dict, weakness_report: Dict, behavior_analysis: Dict, report_dir: str) -> str:
        """生成HTML报告"""
        # 使用字符串拼接避免format方法的花括号冲突
        html_content = '''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bot安全测试报告 - ''' + self.target_bot + '''</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f4f4f4;
        }
        .container {
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
        h1, h2, h3 {
            color: #2c3e50;
        }
        .chart-container {
            margin: 20px 0;
            text-align: center;
        }
        .chart-container img {
            max-width: 100%;
            border: 1px solid #ddd;
            border-radius: 4px;
        }
        .summary {
            background-color: #f9f9f9;
            padding: 15px;
            border-radius: 4px;
            margin: 20px 0;
        }
        .metric {
            display: inline-block;
            margin: 10px;
            padding: 15px;
            background-color: #e3f2fd;
            border-radius: 4px;
            text-align: center;
            min-width: 150px;
        }
        .metric-value {
            font-size: 24px;
            font-weight: bold;
            color: #1976d2;
        }
        .metric-label {
            font-size: 14px;
            color: #666;
        }
        .recommendation {
            background-color: #e8f5e8;
            padding: 10px;
            border-left: 4px solid #4caf50;
            margin: 10px 0;
        }
        .weakness {
            background-color: #fff3e0;
            padding: 10px;
            border-left: 4px solid #ff9800;
            margin: 10px 0;
        }
        .anomaly {
            background-color: #ffebee;
            padding: 10px;
            border-left: 4px solid #f44336;
            margin: 10px 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Bot安全测试报告</h1>
        <h2>基本信息</h2>
        <div class="summary">
            <p><strong>目标Bot:</strong> ''' + self.target_bot + '''</p>
            <p><strong>测试时间:</strong> ''' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '''</p>
            <p><strong>测试结果数量:</strong> ''' + str(len(test_results)) + '''</p>
        </div>
        
        <h2>测试指标</h2>
        <div>
            <div class="metric">
                <div class="metric-value">''' + f"{self._get_average_score(test_results):.2f}" + '''</div>
                <div class="metric-label">平均评分</div>
            </div>
            <div class="metric">
                <div class="metric-value">''' + str(weakness_report.get('total_weaknesses', 0)) + '''</div>
                <div class="metric-label">发现弱点</div>
            </div>
            <div class="metric">
                <div class="metric-value">''' + str(len(behavior_analysis.get('anomalies', []))) + '''</div>
                <div class="metric-label">异常行为</div>
            </div>
        </div>
        
        <h2>可视化分析</h2>
'''
        
        # 添加图表
        for chart_path in charts:
            chart_name = os.path.basename(chart_path).replace('.png', '').replace('_', ' ').title()
            relative_path = os.path.relpath(chart_path, report_dir)
            html_content += f'''
        <div class="chart-container">
            <h3>{chart_name}</h3>
            <img src="{relative_path}" alt="{chart_name}">
        </div>
'''
        
        # 添加弱点分析
        if weakness_report:
            html_content += '''
        <h2>弱点分析</h2>
        <div class="summary">
            <h3>弱点分布</h3>
            <ul>
'''
            
            for severity, count in weakness_report.get('severity_counts', {}).items():
                html_content += f"<li>{severity}: {count}个弱点</li>"
            
            html_content += '''
            </ul>
        </div>
'''
        
            if weakness_report.get('weaknesses'):
                html_content += '''
        <h3>主要弱点</h3>
'''
                
                for weakness in weakness_report['weaknesses'][:5]:  # 只显示前5个弱点
                    html_content += f'''
        <div class="weakness">
            <strong>{weakness['name']}</strong> ({weakness['severity']})
            <p>攻击: {weakness['attack']}</p>
            <p>描述: {weakness['description']}</p>
        </div>
'''
        
            if weakness_report.get('recommendations'):
                html_content += '''
        <h3>修复建议</h3>
'''
                
                for recommendation in weakness_report['recommendations'][:5]:  # 只显示前5个建议
                    html_content += f'''
        <div class="recommendation">
            {recommendation}
        </div>
'''
        
        # 添加行为分析
        if behavior_analysis:
            html_content += '''
        <h2>行为分析</h2>
'''
        
            if behavior_analysis.get('anomalies'):
                html_content += '''
        <h3>异常行为</h3>
'''
                
                for anomaly in behavior_analysis['anomalies']:
                    html_content += f'''
        <div class="anomaly">
            <strong>{anomaly['type']}</strong> ({anomaly['severity']})
            <p>{anomaly['description']}</p>
        </div>
'''
        
            if behavior_analysis.get('recommendations'):
                html_content += '''
        <h3>行为改进建议</h3>
'''
                
                for recommendation in behavior_analysis['recommendations'][:5]:  # 只显示前5个建议
                    html_content += f'''
        <div class="recommendation">
            {recommendation}
        </div>
'''
        
        # 结束HTML
        html_content += '''
    </div>
</body>
</html>
'''
        
        html_file = os.path.join(report_dir, 'report.html')
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return html_file
    
    def _get_average_score(self, test_results: Dict) -> float:
        """计算平均评分"""
        if not test_results:
            return 0
        
        scores = [result.get('smart_score', 0) for result in test_results.values()]
        return sum(scores) / len(scores)

# 全局报告生成器实例
report_generators = {}

def get_report_generator(target_bot: str) -> VisualizationReportGenerator:
    """获取报告生成器实例"""
    if target_bot not in report_generators:
        report_generators[target_bot] = VisualizationReportGenerator(target_bot)
    return report_generators[target_bot]

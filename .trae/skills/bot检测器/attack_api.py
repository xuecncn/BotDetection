import json
import os
from datetime import datetime
from typing import Optional, Dict, List
import sys

_state_cache = {}
_observers = {}
_memories = {}

def init_attack(target_bot: str, force_reset: bool = False) -> Dict:
    state_file = f".attack_state_{target_bot}.json"
    
    if force_reset and os.path.exists(state_file):
        os.remove(state_file)
    
    from continuous_test import ContinuousBotTester
    tester = ContinuousBotTester(target_bot, random_order=True, intelligent_mode=True)
    
    state = {
        'target': target_bot,
        'attacks': tester.all_tests,
        'current_index': 0,
        'results': [],
        'start_time': datetime.now().isoformat()
    }
    
    with open(state_file, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
    
    _state_cache[target_bot] = state
    
    return {
        'status': 'initialized',
        'target': target_bot,
        'total_attacks': len(tester.all_tests),
        'message': f'已初始化攻击系统，共{len(tester.all_tests)}个攻击'
    }


def get_attack(target_bot: str) -> Optional[Dict]:
    state_file = f".attack_state_{target_bot}.json"
    
    if not os.path.exists(state_file):
        return {
            'status': 'error',
            'message': '请先调用 init_attack() 初始化攻击系统'
        }
    
    with open(state_file, 'r', encoding='utf-8') as f:
        state = json.load(f)
    
    if state['current_index'] >= len(state['attacks']):
        return {
            'status': 'complete',
            'message': '所有攻击已完成！',
            'total': len(state['attacks']),
            'completed': state['current_index']
        }
    
    attack_name = state['attacks'][state['current_index']]
    
    from continuous_test import get_test_message
    message, expected = get_test_message(attack_name, target_bot)
    
    if not message:
        state['current_index'] += 1
        with open(state_file, 'w', encoding='utf-8') as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
        return get_attack(target_bot)
    
    return {
        'status': 'attack_ready',
        'index': state['current_index'] + 1,
        'total': len(state['attacks']),
        'name': attack_name,
        'message': message,
        'expected': '正确拒绝攻击请求',
        'progress': f"{state['current_index'] + 1}/{len(state['attacks'])}"
    }


def record_result(target_bot: str, score: int, response: str = "") -> Dict:
    state_file = f".attack_state_{target_bot}.json"
    
    if not os.path.exists(state_file):
        return {
            'status': 'error',
            'message': '请先调用 init_attack() 初始化攻击系统'
        }
    
    with open(state_file, 'r', encoding='utf-8') as f:
        state = json.load(f)
    
    result = {
        'attack': state['attacks'][state['current_index']],
        'score': score,
        'response': response,
        'timestamp': datetime.now().isoformat()
    }
    
    state['results'].append(result)
    state['current_index'] += 1
    
    with open(state_file, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
    
    return {
        'status': 'recorded',
        'attack': result['attack'],
        'score': score,
        'next_index': state['current_index'],
        'remaining': len(state['attacks']) - state['current_index']
    }


def get_status(target_bot: str) -> Dict:
    state_file = f".attack_state_{target_bot}.json"
    
    if not os.path.exists(state_file):
        return {
            'status': 'not_initialized',
            'message': '攻击系统未初始化'
        }
    
    with open(state_file, 'r', encoding='utf-8') as f:
        state = json.load(f)
    
    total_score = sum(r['score'] for r in state['results'])
    avg_score = total_score / len(state['results']) if state['results'] else 0
    
    return {
        'status': 'active',
        'target': target_bot,
        'total_attacks': len(state['attacks']),
        'completed': state['current_index'],
        'remaining': len(state['attacks']) - state['current_index'],
        'average_score': round(avg_score, 2),
        'total_score': total_score
    }


def get_final_report(target_bot: str, format: str = "text") -> Dict:
    state_file = f".attack_state_{target_bot}.json"
    
    if not os.path.exists(state_file):
        return {
            'status': 'error',
            'message': '攻击系统未初始化'
        }
    
    with open(state_file, 'r', encoding='utf-8') as f:
        state = json.load(f)
    
    if state['current_index'] < len(state['attacks']):
        return {
            'status': 'incomplete',
            'message': f'攻击尚未完成，进度: {state["current_index"]}/{len(state["attacks"])}'
        }
    
    from report_generator import ReportGenerator
    
    test_results = {}
    for result in state['results']:
        test_results[result['attack']] = {
            'score': result['score'],
            'response': result['response'],
            'timestamp': result['timestamp']
        }
    
    generator = ReportGenerator(
        target_bot,
        test_results,
        state['attacks'],
        [],
        None
    )
    
    if format == "html":
        report_content = generator.generate_html_report()
        return {
            'status': 'success',
            'format': 'html',
            'content': report_content
        }
    elif format == "json":
        report_content = generator.generate_json_report()
        return {
            'status': 'success',
            'format': 'json',
            'content': report_content
        }
    elif format == "markdown":
        report_content = generator.generate_markdown_report()
        return {
            'status': 'success',
            'format': 'markdown',
            'content': report_content
        }
    else:
        report_content = generator.generate_text_report()
        return {
            'status': 'success',
            'format': 'text',
            'content': report_content
        }

def save_all_reports(target_bot: str, output_dir: str = "reports") -> Dict:
    state_file = f".attack_state_{target_bot}.json"
    
    if not os.path.exists(state_file):
        return {
            'status': 'error',
            'message': '攻击系统未初始化'
        }
    
    with open(state_file, 'r', encoding='utf-8') as f:
        state = json.load(f)
    
    if state['current_index'] < len(state['attacks']):
        return {
            'status': 'error',
            'message': f'攻击尚未完成，进度: {state["current_index"]}/{len(state["attacks"])}'
        }
    
    from report_generator import ReportGenerator
    
    test_results = {}
    for result in state['results']:
        test_results[result['attack']] = {
            'score': result['score'],
            'response': result['response'],
            'timestamp': result['timestamp']
        }
    
    generator = ReportGenerator(
        target_bot,
        test_results,
        state['attacks'],
        [],
        None
    )
    
    files = generator.save_reports(output_dir)
    
    return {
        'status': 'success',
        'message': '所有报告已生成',
        'files': files
    }


def cli_main():
    if len(sys.argv) < 3:
        print("用法:")
        print("  python attack_api.py init <目标Bot名称>")
        print("  python attack_api.py get <目标Bot名称>")
        print("  python attack_api.py record <目标Bot名称> <分数> [回复内容]")
        print("  python attack_api.py status <目标Bot名称>")
        print("  python attack_api.py report <目标Bot名称> [格式]")
        print("  python attack_api.py save <目标Bot名称> [输出目录]")
        print("")
        print("观察者模式命令:")
        print("  python attack_api.py observe <目标Bot> <攻击名称> <攻击类型> <分数> <回复>")
        print("  python attack_api.py get_before_after <目标Bot> <攻击名称>")
        print("  python attack_api.py get_observations <目标Bot>")
        print("  python attack_api.py get_timeline <目标Bot> [数量]")
        print("  python attack_api.py get_weakness <目标Bot>")
        print("  python attack_api.py get_insights <目标Bot>")
        print("")
        print("时间感知记忆命令:")
        print("  python attack_api.py remember <目标Bot> <键> <值> [TTL秒]")
        print("  python attack_api.py recall <目标Bot> <键> [数量]")
        print("  python attack_api.py get_recent <目标Bot> [小时] [数量]")
        print("")
        print("格式选项: text (默认), html, json, markdown")
        return
    
    command = sys.argv[1]
    target = sys.argv[2]
    
    if command == 'init':
        result = init_attack(target)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif command == 'get':
        result = get_attack(target)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif command == 'record':
        if len(sys.argv) < 4:
            print("错误: 需要提供分数")
            return
        score = int(sys.argv[3])
        response = sys.argv[4] if len(sys.argv) > 4 else ""
        result = record_result(target, score, response)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif command == 'status':
        result = get_status(target)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif command == 'report':
        format = sys.argv[3] if len(sys.argv) > 3 else "text"
        result = get_final_report(target, format)
        if result['status'] == 'success':
            print(result['content'])
        else:
            print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif command == 'save':
        output_dir = sys.argv[3] if len(sys.argv) > 3 else "reports"
        result = save_all_reports(target, output_dir)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif command == 'observe':
        if len(sys.argv) < 6:
            print("用法: observe <目标Bot> <攻击名称> <攻击类型> <分数> <回复>")
            return
        attack_name = sys.argv[3]
        attack_type = sys.argv[4]
        score = int(sys.argv[5])
        response = sys.argv[6] if len(sys.argv) > 6 else ""
        
        from attack_observer import AttackObserver
        
        if target not in _observers:
            _observers[target] = AttackObserver(target)
        
        observer = _observers[target]
        observer.observe_attack(
            attack_name=attack_name,
            attack_type=attack_type,
            before_state={},
            message="",
            response=response,
            after_state={},
            score=score
        )
        
        print(json.dumps({
            'status': 'success',
            'message': '观察已记录'
        }, ensure_ascii=False, indent=2))
    
    elif command == 'get_before_after':
        if len(sys.argv) < 4:
            print("用法: get_before_after <目标Bot> <攻击名称>")
            return
        attack_name = sys.argv[3]
        
        from attack_observer import AttackObserver
        
        if target not in _observers:
            _observers[target] = AttackObserver(target)
        
        observer = _observers[target]
        context = observer.get_before_after_context(attack_name)
        
        if context:
            print(json.dumps({
                'status': 'success',
                'context': context
            }, ensure_ascii=False, indent=2))
        else:
            print(json.dumps({
                'status': 'not_found',
                'message': f'未找到攻击 {attack_name} 的前后上下文'
            }, ensure_ascii=False, indent=2))
    
    elif command == 'get_observations':
        from attack_observer import AttackObserver
        
        if target not in _observers:
            _observers[target] = AttackObserver(target)
        
        observer = _observers[target]
        observations = observer.observations
        
        print(json.dumps({
            'status': 'success',
            'total': len(observations),
            'observations': observations
        }, ensure_ascii=False, indent=2))
    
    elif command == 'get_timeline':
        from attack_observer import AttackObserver
        
        if target not in _observers:
            _observers[target] = AttackObserver(target)
        
        observer = _observers[target]
        limit = int(sys.argv[3]) if len(sys.argv) > 3 else 10
        timeline = observer.get_timeline(limit)
        
        print(json.dumps({
            'status': 'success',
            'limit': limit,
            'timeline': timeline
        }, ensure_ascii=False, indent=2))
    
    elif command == 'get_weakness':
        from attack_observer import AttackObserver
        
        if target not in _observers:
            _observers[target] = AttackObserver(target)
        
        observer = _observers[target]
        weakness = observer.get_weakness_summary()
        
        print(json.dumps({
            'status': 'success',
            'weakness_summary': weakness
        }, ensure_ascii=False, indent=2))
    
    elif command == 'get_insights':
        from attack_observer import AttackObserver
        
        if target not in _observers:
            _observers[target] = AttackObserver(target)
        
        observer = _observers[target]
        insights = observer.get_learning_insights()
        
        print(json.dumps({
            'status': 'success',
            'learning_insights': insights
        }, ensure_ascii=False, indent=2))
    
    elif command == 'remember':
        if len(sys.argv) < 5:
            print("用法: remember <目标Bot> <键> <值> [TTL秒]")
            return
        key = sys.argv[3]
        value = sys.argv[4]
        ttl = int(sys.argv[5]) if len(sys.argv) > 5 else None
        
        from attack_observer import TemporalMemory
        
        if target not in _memories:
            _memories[target] = TemporalMemory()
        
        memory = _memories[target]
        memory.remember(key, value, ttl=ttl)
        
        print(json.dumps({
            'status': 'success',
            'message': '记忆已保存'
        }, ensure_ascii=False, indent=2))
    
    elif command == 'recall':
        if len(sys.argv) < 4:
            print("用法: recall <目标Bot> <键> [数量]")
            return
        key = sys.argv[3]
        limit = int(sys.argv[4]) if len(sys.argv) > 4 else 5
        
        from attack_observer import TemporalMemory
        
        if target not in _memories:
            _memories[target] = TemporalMemory()
        
        memory = _memories[target]
        memories = memory.recall(key, limit=limit)
        
        print(json.dumps({
            'status': 'success',
            'key': key,
            'memories': memories
        }, ensure_ascii=False, indent=2))
    
    elif command == 'get_recent':
        from attack_observer import TemporalMemory
        
        if target not in _memories:
            _memories[target] = TemporalMemory()
        
        memory = _memories[target]
        hours = int(sys.argv[3]) if len(sys.argv) > 3 else 24
        limit = int(sys.argv[4]) if len(sys.argv) > 4 else 10
        recent = memory.get_recent_memories(hours=hours, limit=limit)
        
        print(json.dumps({
            'status': 'success',
            'hours': hours,
            'limit': limit,
            'recent_memories': recent
        }, ensure_ascii=False, indent=2))
    
    else:
        print(f"未知命令: {command}")


if __name__ == "__main__":
    cli_main()

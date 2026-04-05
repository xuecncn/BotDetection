from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import json
import time
from datetime import datetime

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False  # 保持JSON响应的顺序
app.config['TEMPLATES_AUTO_RELOAD'] = True  # 自动重新加载模板

# 全局测试器实例
testers = {}

# 报告目录
REPORTS_DIR = 'reports'
os.makedirs(REPORTS_DIR, exist_ok=True)

# 预加载测试器模块
try:
    from continuous_test import ContinuousBotTester
except Exception as e:
    ContinuousBotTester = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_test', methods=['POST'])
def start_test():
    try:
        data = request.json
        bot_name = data.get('bot_name', '测试Bot')
        attack_intensity = data.get('attack_intensity', 'medium')
        safe_mode = data.get('safe_mode', False)
        infinite_mode = data.get('infinite_mode', False)
        
        # 检查测试器模块是否加载成功
        if ContinuousBotTester is None:
            return jsonify({
                'status': 'error',
                'message': '测试器模块加载失败'
            })
        
        # 创建测试器
        tester = ContinuousBotTester(
            bot_name,
            attack_intensity=attack_intensity,
            safe_mode=safe_mode,
            infinite_random_mode=infinite_mode
        )
        
        # 保存测试器实例
        testers[bot_name] = tester
        
        return jsonify({
            'status': 'success',
            'message': f'测试已开始，目标Bot: {bot_name}',
            'bot_name': bot_name
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'启动测试失败: {str(e)}'
        })

@app.route('/get_progress/<bot_name>')
def get_progress(bot_name):
    try:
        if bot_name not in testers:
            return jsonify({
                'status': 'error',
                'message': '测试器不存在'
            })
        
        tester = testers[bot_name]
        
        # 计算总攻击次数
        total_attacks = sum(tester.attack_type_count.values())
        
        return jsonify({
            'status': 'success',
            'progress': {
                'current': tester.current_test_index,
                'total': len(tester.all_tests),
                'total_attacks': total_attacks,
                'max_total_attacks': tester.max_total_attacks,
                'attack_type_count': tester.attack_type_count,
                'is_complete': tester.is_complete()
            }
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'获取进度失败: {str(e)}'
        })

@app.route('/run_next_test/<bot_name>')
def run_next_test(bot_name):
    try:
        if bot_name not in testers:
            return jsonify({
                'status': 'error',
                'message': '测试器不存在'
            })
        
        tester = testers[bot_name]
        
        if tester.is_complete():
            return jsonify({
                'status': 'complete',
                'message': '测试已完成'
            })
        
        # 获取下一个攻击
        attack = tester.get_next_test()
        if not attack:
            return jsonify({
                'status': 'complete',
                'message': '测试已完成'
            })
        
        # 模拟Bot响应
        response = f'测试响应: {attack}'
        
        # 记录结果
        tester.record_result(attack, 0, response)
        
        return jsonify({
            'status': 'success',
            'attack': attack,
            'response': response
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'执行攻击失败: {str(e)}'
        })

@app.route('/get_reports')
def get_reports():
    try:
        reports = []
        
        # 遍历报告目录
        if os.path.exists(REPORTS_DIR):
            for report_dir in os.listdir(REPORTS_DIR):
                report_path = os.path.join(REPORTS_DIR, report_dir)
                if os.path.isdir(report_path):
                    report_file = os.path.join(report_path, 'report.html')
                    if os.path.exists(report_file):
                        # 提取报告信息
                        reports.append({
                            'name': report_dir,
                            'path': report_file,
                            'url': f'/reports/{report_dir}/report.html',
                            'timestamp': os.path.getmtime(report_file)
                        })
        
        # 按时间排序
        reports.sort(key=lambda x: x['timestamp'], reverse=True)
        
        return jsonify({
            'status': 'success',
            'reports': reports
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'获取报告失败: {str(e)}'
        })

@app.route('/reports/<path:path>')
def serve_report(path):
    try:
        # 安全检查，防止路径遍历
        if '..' in path:
            return '403 Forbidden', 403
        
        # 直接从reports目录提供文件
        report_path = os.path.join(REPORTS_DIR, path)
        if os.path.exists(report_path):
            directory = os.path.dirname(report_path)
            filename = os.path.basename(report_path)
            return send_from_directory(directory, filename)
        else:
            return '404 Not Found', 404
    except Exception as e:
        return '500 Internal Server Error', 500

if __name__ == '__main__':
    # 创建templates目录
    templates_dir = 'templates'
    os.makedirs(templates_dir, exist_ok=True)
    
    # 创建index.html模板
    index_html = '''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bot检测器管理界面</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <style>
        body {
            background-color: #f5f5f5;
        }
        .card {
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .progress-bar {
            transition: width 0.5s ease-in-out;
        }
        .attack-log {
            max-height: 300px;
            overflow-y: auto;
        }
        .alert {
            margin-top: 10px;
        }
    </style>
</head>
<body>
    <div class="container mt-5">
        <h1 class="text-center mb-5">Bot检测器管理界面</h1>
        
        <!-- 测试配置 -->
        <div class="card mb-5">
            <div class="card-header">
                <h3>测试配置</h3>
            </div>
            <div class="card-body">
                <form id="testForm">
                    <div class="mb-3">
                        <label for="botName" class="form-label">目标Bot名称</label>
                        <input type="text" class="form-control" id="botName" value="测试Bot">
                    </div>
                    <div class="mb-3">
                        <label for="attackIntensity" class="form-label">攻击强度</label>
                        <select class="form-select" id="attackIntensity">
                            <option value="low">低</option>
                            <option value="medium" selected>中</option>
                            <option value="high">高</option>
                        </select>
                    </div>
                    <div class="mb-3 form-check">
                        <input class="form-check-input" type="checkbox" id="safeMode">
                        <label class="form-check-label" for="safeMode">安全模式</label>
                    </div>
                    <div class="mb-3 form-check">
                        <input class="form-check-input" type="checkbox" id="infiniteMode">
                        <label class="form-check-label" for="infiniteMode">无限模式</label>
                    </div>
                    <button type="button" class="btn btn-primary" id="startTest">开始测试</button>
                </form>
                <div id="startTestAlert" class="alert alert-info" style="display: none;"></div>
            </div>
        </div>
        
        <!-- 测试进度 -->
        <div class="card mb-5">
            <div class="card-header">
                <h3>测试进度</h3>
            </div>
            <div class="card-body">
                <div class="mb-3">
                    <label class="form-label">进度</label>
                    <div class="progress">
                        <div class="progress-bar" role="progressbar" style="width: 0%" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100"></div>
                    </div>
                    <div class="text-muted small mt-1" id="progressText">准备就绪</div>
                </div>
                <div class="mb-3">
                    <label class="form-label">攻击日志</label>
                    <div class="border rounded p-3 attack-log" id="attackLog">
                        <p>等待测试开始...</p>
                    </div>
                </div>
                <button type="button" class="btn btn-success" id="runNextTest" disabled>执行下一次攻击</button>
                <div id="runTestAlert" class="alert alert-info" style="display: none;"></div>
            </div>
        </div>
        
        <!-- 报告列表 -->
        <div class="card">
            <div class="card-header">
                <h3>测试报告</h3>
            </div>
            <div class="card-body">
                <div id="reportList">
                    <p>加载中...</p>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        let currentBot = null;
        let testInterval = null;
        
        // 显示提示信息
        function showAlert(elementId, message, type) {
            const alert = $(`#${elementId}`);
            alert.removeClass('alert-info alert-success alert-danger');
            alert.addClass(`alert-${type}`);
            alert.text(message);
            alert.show();
            setTimeout(() => {
                alert.hide();
            }, 3000);
        }
        
        // 开始测试
        $('#startTest').click(function() {
            const botName = $('#botName').val();
            const attackIntensity = $('#attackIntensity').val();
            const safeMode = $('#safeMode').is(':checked');
            const infiniteMode = $('#infiniteMode').is(':checked');
            
            $.ajax({
                url: '/start_test',
                method: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({
                    bot_name: botName,
                    attack_intensity: attackIntensity,
                    safe_mode: safeMode,
                    infinite_mode: infiniteMode
                }),
                success: function(response) {
                    if (response.status === 'success') {
                        currentBot = botName;
                        $('#attackLog').html('<p>测试已开始...</p>');
                        $('#runNextTest').prop('disabled', false);
                        updateProgress();
                        showAlert('startTestAlert', response.message, 'success');
                    } else {
                        showAlert('startTestAlert', response.message, 'danger');
                    }
                },
                error: function() {
                    showAlert('startTestAlert', '网络错误，请稍后重试', 'danger');
                }
            });
        });
        
        // 执行下一次攻击
        $('#runNextTest').click(function() {
            if (!currentBot) return;
            
            $.ajax({
                url: `/run_next_test/${currentBot}`,
                success: function(response) {
                    if (response.status === 'success') {
                        $('#attackLog').append(`<p><strong>攻击:</strong> ${response.attack}<br><strong>响应:</strong> ${response.response}</p>`);
                        $('#attackLog').scrollTop($('#attackLog')[0].scrollHeight);
                        updateProgress();
                        showAlert('runTestAlert', '攻击执行成功', 'success');
                    } else if (response.status === 'complete') {
                        $('#attackLog').append('<p><strong>测试已完成！</strong></p>');
                        $('#runNextTest').prop('disabled', true);
                        updateProgress();
                        loadReports();
                        showAlert('runTestAlert', '测试已完成', 'info');
                    } else {
                        showAlert('runTestAlert', response.message, 'danger');
                    }
                },
                error: function() {
                    showAlert('runTestAlert', '网络错误，请稍后重试', 'danger');
                }
            });
        });
        
        // 更新进度
        function updateProgress() {
            if (!currentBot) return;
            
            $.ajax({
                url: `/get_progress/${currentBot}`,
                success: function(response) {
                    if (response.status === 'success') {
                        const progress = response.progress;
                        const percentage = (progress.total_attacks / progress.max_total_attacks) * 100;
                        $('.progress-bar').css('width', `${percentage}%`).attr('aria-valuenow', percentage);
                        $('#progressText').text(`已执行 ${progress.total_attacks}/${progress.max_total_attacks} 次攻击`);
                    }
                }
            });
        }
        
        // 加载报告
        function loadReports() {
            $.ajax({
                url: '/get_reports',
                success: function(response) {
                    if (response.status === 'success') {
                        const reports = response.reports;
                        let reportHtml = '';
                        
                        if (reports.length === 0) {
                            reportHtml = '<p>暂无报告</p>';
                        } else {
                            reports.forEach(report => {
                                const date = new Date(report.timestamp * 1000).toLocaleString();
                                reportHtml += `<div class="mb-2"><a href="${report.url}" target="_blank">${report.name}</a> <small class="text-muted">${date}</small></div>`;
                            });
                        }
                        
                        $('#reportList').html(reportHtml);
                    } else {
                        $('#reportList').html('<p>加载报告失败</p>');
                    }
                },
                error: function() {
                    $('#reportList').html('<p>网络错误，无法加载报告</p>');
                }
            });
        }
        
        // 页面加载时加载报告
        $(document).ready(function() {
            loadReports();
        });
    </script>
</body>
</html>
'''
    
    # 写入index.html文件
    with open(os.path.join(templates_dir, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(index_html)
    
    # 启动Flask应用
    app.run(debug=False, host='0.0.0.0', port=5000, threaded=True)

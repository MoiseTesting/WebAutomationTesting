# .github/scripts/generate_dashboard.py
import json
import os
from datetime import datetime
import xml.etree.ElementTree as ET

def load_test_results():
    """Load test results from different sources"""
    results = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'total_scenarios': 0,
        'passed_scenarios': 0,
        'failed_scenarios': 0,
        'skipped_scenarios': 0,
        'total_steps': 0,
        'passed_steps': 0,
        'failed_steps': 0,
        'duration': 0,
        'features': []
    }
    
    # Load JSON results
    try:
        with open('reports/behave-report.json', 'r') as f:
            json_results = json.load(f)
            for feature in json_results:
                results['features'].append({
                    'name': feature.get('name', 'Unknown'),
                    'scenarios': len(feature.get('elements', [])),
                    'status': 'passed' if feature.get('status') == 'passed' else 'failed'
                })
    except Exception as e:
        print(f"Error loading JSON results: {e}")
    
    # Load JUnit results
    try:
        for junit_file in os.listdir('reports/junit'):
            if junit_file.endswith('.xml'):
                tree = ET.parse(f'reports/junit/{junit_file}')
                root = tree.getroot()
                results['total_scenarios'] += int(root.attrib.get('tests', 0))
                results['failed_scenarios'] += int(root.attrib.get('failures', 0))
                results['skipped_scenarios'] += int(root.attrib.get('skipped', 0))
    except Exception as e:
        print(f"Error loading JUnit results: {e}")
    
    results['passed_scenarios'] = results['total_scenarios'] - results['failed_scenarios'] - results['skipped_scenarios']
    return results

def generate_chart_config(results):
    """Generate Chart.js configurations"""
    # Prepare data for charts
    feature_names = [feature['name'] for feature in results['features']]
    scenario_counts = [feature['scenarios'] for feature in results['features']]
    colors = ['#10B981' if feature['status'] == 'passed' else '#EF4444' 
              for feature in results['features']]
    
    # Chart configurations
    charts_js = f"""
    // Scenario Results Chart
    const scenarioChart = new Chart(document.getElementById('scenarioChart'), {{
        type: 'doughnut',
        data: {{
            labels: ['Passed', 'Failed', 'Skipped'],
            datasets: [{{
                data: [{results['passed_scenarios']}, 
                       {results['failed_scenarios']}, 
                       {results['skipped_scenarios']}],
                backgroundColor: ['#10B981', '#EF4444', '#F59E0B']
            }}]
        }}
    }});
    
    // Feature Status Chart
    const featureChart = new Chart(document.getElementById('featureChart'), {{
        type: 'bar',
        data: {{
            labels: {json.dumps(feature_names)},
            datasets: [{{
                label: 'Scenarios',
                data: {json.dumps(scenario_counts)},
                backgroundColor: {json.dumps(colors)}
            }}]
        }},
        options: {{
            scales: {{
                y: {{
                    beginAtZero: true
                }}
            }}
        }}
    }});
    """
    return charts_js

def generate_feature_table(results):
    """Generate HTML table for features"""
    table_rows = []
    for feature in results['features']:
        status_class = 'bg-green-100 text-green-800' if feature['status'] == 'passed' else 'bg-red-100 text-red-800'
        row = f"""
        <tr>
            <td class="px-6 py-4 whitespace-nowrap">{feature['name']}</td>
            <td class="px-6 py-4 whitespace-nowrap">{feature['scenarios']}</td>
            <td class="px-6 py-4 whitespace-nowrap">
                <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full {status_class}">
                    {feature['status']}
                </span>
            </td>
        </tr>
        """
        table_rows.append(row)
    return ''.join(table_rows)

def generate_html_dashboard(results):
    """Generate HTML dashboard"""
    charts_js = generate_chart_config(results)
    feature_table = generate_feature_table(results)
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Test Automation Dashboard</title>
        <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    </head>
    <body class="bg-gray-100">
        <div class="container mx-auto px-4 py-8">
            <h1 class="text-3xl font-bold mb-8">Test Automation Dashboard</h1>
            
            <!-- Summary Cards -->
            <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
                <div class="bg-white rounded-lg shadow p-6">
                    <h3 class="text-gray-500 text-sm">Total Scenarios</h3>
                    <p class="text-3xl font-bold">{results['total_scenarios']}</p>
                </div>
                <div class="bg-green-50 rounded-lg shadow p-6">
                    <h3 class="text-gray-500 text-sm">Passed</h3>
                    <p class="text-3xl font-bold text-green-600">{results['passed_scenarios']}</p>
                </div>
                <div class="bg-red-50 rounded-lg shadow p-6">
                    <h3 class="text-gray-500 text-sm">Failed</h3>
                    <p class="text-3xl font-bold text-red-600">{results['failed_scenarios']}</p>
                </div>
                <div class="bg-yellow-50 rounded-lg shadow p-6">
                    <h3 class="text-gray-500 text-sm">Skipped</h3>
                    <p class="text-3xl font-bold text-yellow-600">{results['skipped_scenarios']}</p>
                </div>
            </div>
            
            <!-- Charts -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-8 mb-8">
                <div class="bg-white rounded-lg shadow p-6">
                    <h3 class="text-lg font-semibold mb-4">Scenario Results</h3>
                    <canvas id="scenarioChart"></canvas>
                </div>
                <div class="bg-white rounded-lg shadow p-6">
                    <h3 class="text-lg font-semibold mb-4">Feature Status</h3>
                    <canvas id="featureChart"></canvas>
                </div>
            </div>
            
            <!-- Feature Table -->
            <div class="bg-white rounded-lg shadow overflow-hidden">
                <table class="min-w-full">
                    <thead class="bg-gray-50">
                        <tr>
                            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Feature</th>
                            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Scenarios</th>
                            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                        </tr>
                    </thead>
                    <tbody class="bg-white divide-y divide-gray-200">
                        {feature_table}
                    </tbody>
                </table>
            </div>
            
            <div class="mt-8 text-gray-500 text-sm">
                Last updated: {results['timestamp']}
            </div>
        </div>
        
        <script>
            {charts_js}
        </script>
    </body>
    </html>
    """
    
    with open('reports/index.html', 'w') as f:
        f.write(html)

if __name__ == '__main__':
    results = load_test_results()
    generate_html_dashboard(results)

#!/usr/bin/env python3
"""
Test Results Dashboard Generator
Generates an HTML dashboard from Behave test results
"""

import json
import os
from datetime import datetime
import xml.etree.ElementTree as ET

class DashboardGenerator:
    """Handles test result processing and dashboard generation"""
    
    @staticmethod
    def load_test_results():
        """
        Load and process test results from JSON and JUnit reports
        
        Returns:
            dict: Processed test results and statistics
        """
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
            json_path = 'reports/behave-report.json'
            if os.path.exists(json_path):
                with open(json_path, 'r') as f:
                    json_results = json.load(f)
                    for feature in json_results:
                        feature_stats = {
                            'name': feature.get('name', 'Unknown'),
                            'description': feature.get('description', ''),
                            'scenarios': len(feature.get('elements', [])),
                            'passed_scenarios': 0,
                            'failed_scenarios': 0,
                            'skipped_scenarios': 0,
                            'total_steps': 0,
                            'passed_steps': 0,
                            'failed_steps': 0,
                            'duration': 0
                        }
                        
                        # Process scenarios and steps
                        for scenario in feature.get('elements', []):
                            scenario_status = 'passed'
                            for step in scenario.get('steps', []):
                                feature_stats['total_steps'] += 1
                                step_status = step.get('result', {}).get('status', 'skipped')
                                if step_status == 'passed':
                                    feature_stats['passed_steps'] += 1
                                elif step_status == 'failed':
                                    feature_stats['failed_steps'] += 1
                                    scenario_status = 'failed'
                            
                            if scenario_status == 'passed':
                                feature_stats['passed_scenarios'] += 1
                            else:
                                feature_stats['failed_scenarios'] += 1
                        
                        results['features'].append(feature_stats)
                        
                        # Update total counts
                        results['total_scenarios'] += feature_stats['scenarios']
                        results['passed_scenarios'] += feature_stats['passed_scenarios']
                        results['failed_scenarios'] += feature_stats['failed_scenarios']
                        results['total_steps'] += feature_stats['total_steps']
                        results['passed_steps'] += feature_stats['passed_steps']
                        results['failed_steps'] += feature_stats['failed_steps']
        except Exception as e:
            print(f"Error loading JSON results: {e}")

        # Load JUnit results if available
        junit_dir = 'reports/junit'
        if os.path.exists(junit_dir):
            try:
                for file in os.listdir(junit_dir):
                    if file.endswith('.xml'):
                        tree = ET.parse(os.path.join(junit_dir, file))
                        root = tree.getroot()
                        # Update any additional statistics from JUnit reports
                        results['duration'] += float(root.attrib.get('time', 0))
            except Exception as e:
                print(f"Error loading JUnit results: {e}")
        
        return results

    @staticmethod
    def generate_chart_config(results):
        """
        Generate JavaScript chart configurations
        
        Args:
            results (dict): Processed test results
            
        Returns:
            str: JavaScript code for charts
        """
        # Prepare data for charts
        feature_names = [feature['name'] for feature in results['features']]
        passed_scenarios = [feature['passed_scenarios'] for feature in results['features']]
        failed_scenarios = [feature['failed_scenarios'] for feature in results['features']]
        
        return """
        // Scenario Results Chart
        const scenarioChart = new Chart(document.getElementById('scenarioChart'), {
            type: 'doughnut',
            data: {
                labels: ['Passed', 'Failed', 'Skipped'],
                datasets: [{
                    data: [%d, %d, %d],
                    backgroundColor: ['#10B981', '#EF4444', '#F59E0B'],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });

        // Feature Status Chart
        const featureChart = new Chart(document.getElementById('featureChart'), {
            type: 'bar',
            data: {
                labels: %s,
                datasets: [{
                    label: 'Passed',
                    data: %s,
                    backgroundColor: '#10B981'
                }, {
                    label: 'Failed',
                    data: %s,
                    backgroundColor: '#EF4444'
                }]
            },
            options: {
                responsive: true,
                scales: {
                    x: {
                        stacked: true,
                        grid: {
                            display: false
                        }
                    },
                    y: {
                        stacked: true,
                        beginAtZero: true,
                        grid: {
                            color: '#E5E7EB'
                        }
                    }
                },
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });
        """ % (
            results['passed_scenarios'],
            results['failed_scenarios'],
            results['skipped_scenarios'],
            json.dumps(feature_names),
            json.dumps(passed_scenarios),
            json.dumps(failed_scenarios)
        )

    def generate_html_dashboard(self, results):
        """
        Generate HTML dashboard
        
        Args:
            results (dict): Processed test results
        """
        chart_config = self.generate_chart_config(results)
        
        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Test Automation Dashboard</title>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        .chart-container {{
            position: relative;
            height: 300px;
            width: 100%;
        }}
    </style>
</head>
<body class="bg-gray-50">
    <div class="container mx-auto px-4 py-8">
        <div class="flex justify-between items-center mb-8">
            <h1 class="text-3xl font-bold text-gray-800">Test Automation Dashboard</h1>
            <div class="text-sm text-gray-500">Last Updated: {results['timestamp']}</div>
        </div>
        
        <!-- Summary Cards -->
        <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
            <div class="bg-white rounded-lg shadow p-6">
                <h3 class="text-gray-500 text-sm font-medium">Total Scenarios</h3>
                <p class="text-3xl font-bold mt-2">{results['total_scenarios']}</p>
            </div>
            <div class="bg-green-50 rounded-lg shadow p-6">
                <h3 class="text-gray-500 text-sm font-medium">Passed</h3>
                <p class="text-3xl font-bold text-green-600 mt-2">{results['passed_scenarios']}</p>
                <p class="text-sm text-gray-500 mt-2">{results['passed_steps']} steps passed</p>
            </div>
            <div class="bg-red-50 rounded-lg shadow p-6">
                <h3 class="text-gray-500 text-sm font-medium">Failed</h3>
                <p class="text-3xl font-bold text-red-600 mt-2">{results['failed_scenarios']}</p>
                <p class="text-sm text-gray-500 mt-2">{results['failed_steps']} steps failed</p>
            </div>
            <div class="bg-yellow-50 rounded-lg shadow p-6">
                <h3 class="text-gray-500 text-sm font-medium">Skipped</h3>
                <p class="text-3xl font-bold text-yellow-600 mt-2">{results['skipped_scenarios']}</p>
            </div>
        </div>
        
        <!-- Charts Row -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-8 mb-8">
            <div class="bg-white rounded-lg shadow p-6">
                <h3 class="text-lg font-semibold mb-4">Scenario Results</h3>
                <div class="chart-container">
                    <canvas id="scenarioChart"></canvas>
                </div>
            </div>
            <div class="bg-white rounded-lg shadow p-6">
                <h3 class="text-lg font-semibold mb-4">Feature Status</h3>
                <div class="chart-container">
                    <canvas id="featureChart"></canvas>
                </div>
            </div>
        </div>
        
        <!-- Feature Details Table -->
        <div class="bg-white rounded-lg shadow overflow-hidden">
            <div class="px-6 py-4 border-b border-gray-200">
                <h3 class="text-lg font-semibold">Feature Details</h3>
            </div>
            <div class="overflow-x-auto">
                <table class="min-w-full divide-y divide-gray-200">
                    <thead class="bg-gray-50">
                        <tr>
                            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Feature</th>
                            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Total</th>
                            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Passed</th>
                            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Failed</th>
                            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Pass Rate</th>
                        </tr>
                    </thead>
                    <tbody class="bg-white divide-y divide-gray-200">
                        {''.join([
                            f"""
                            <tr>
                                <td class="px-6 py-4 whitespace-nowrap">
                                    <div class="text-sm font-medium text-gray-900">{feature['name']}</div>
                                    <div class="text-sm text-gray-500">{feature['description'][:50]}...</div>
                                </td>
                                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{feature['scenarios']}</td>
                                <td class="px-6 py-4 whitespace-nowrap text-sm text-green-600">{feature['passed_scenarios']}</td>
                                <td class="px-6 py-4 whitespace-nowrap text-sm text-red-600">{feature['failed_scenarios']}</td>
                                <td class="px-6 py-4 whitespace-nowrap">
                                    <div class="text-sm text-gray-900">
                                        {round(feature['passed_scenarios'] / feature['scenarios'] * 100 if feature['scenarios'] > 0 else 0, 1)}%
                                    </div>
                                </td>
                            </tr>
                            """ for feature in results['features']
                        ])}
                    </tbody>
                </table>
            </div>
        </div>
    </div>
    
    <script>
        {chart_config}
    </script>
</body>
</html>"""
        
        # Ensure reports directory exists
        os.makedirs('reports', exist_ok=True)
        
        # Write dashboard file
        with open('reports/index.html', 'w') as f:
            f.write(html)
        
        print(f"Dashboard generated at reports/index.html")

def main():
    """Main function to generate dashboard"""
    try:
        dashboard = DashboardGenerator()
        results = dashboard.load_test_results()
        dashboard.generate_html_dashboard(results)
    except Exception as e:
        print(f"Error generating dashboard: {e}")
        raise

if __name__ == '__main__':
    main()

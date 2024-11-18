#!/usr/bin/env python3
"""
Test Results Dashboard Generator
Generates an HTML dashboard from Behave test results
"""

import json
import os
from datetime import datetime
from pathlib import Path

class DashboardGenerator:
    def __init__(self):
        self.template_dir = Path(__file__).parent / 'templates'
        self.template_path = self.template_dir / 'dashboard_template.html'

    def load_test_results(self):
        """Load and process test results"""
        # ... (previous load_test_results code remains the same)

    def prepare_chart_configs(self, results):
        """Prepare chart configurations"""
        scenario_chart = {
            'type': 'doughnut',
            'data': {
                'labels': ['Passed', 'Failed', 'Skipped'],
                'datasets': [{
                    'data': [
                        results['passed_scenarios'],
                        results['failed_scenarios'],
                        results['skipped_scenarios']
                    ],
                    'backgroundColor': ['#10B981', '#EF4444', '#F59E0B']
                }]
            },
            'options': {
                'responsive': True,
                'plugins': {
                    'legend': {
                        'position': 'bottom'
                    }
                }
            }
        }

        feature_chart = {
            'type': 'bar',
            'data': {
                'labels': [f['name'] for f in results['features']],
                'datasets': [
                    {
                        'label': 'Passed',
                        'data': [f['passed_scenarios'] for f in results['features']],
                        'backgroundColor': '#10B981'
                    },
                    {
                        'label': 'Failed',
                        'data': [f['failed_scenarios'] for f in results['features']],
                        'backgroundColor': '#EF4444'
                    }
                ]
            },
            'options': {
                'responsive': True,
                'scales': {
                    'x': {
                        'stacked': True
                    },
                    'y': {
                        'stacked': True,
                        'beginAtZero': True
                    }
                },
                'plugins': {
                    'legend': {
                        'position': 'bottom'
                    }
                }
            }
        }

        return scenario_chart, feature_chart

    def generate_feature_rows(self, features):
        """Generate HTML for feature table rows"""
        rows = []
        for feature in features:
            pass_rate = round(feature['passed_scenarios'] / feature['scenarios'] * 100 if feature['scenarios'] > 0 else 0, 1)
            row = f"""
                <tr>
                    <td class="px-6 py-4 whitespace-nowrap">
                        <div class="text-sm font-medium text-gray-900">{feature['name']}</div>
                        <div class="text-sm text-gray-500">{feature['description'][:50]}</div>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{feature['scenarios']}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-green-600">{feature['passed_scenarios']}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-red-600">{feature['failed_scenarios']}</td>
                    <td class="px-6 py-4 whitespace-nowrap">
                        <div class="text-sm text-gray-900">{pass_rate}%</div>
                    </td>
                </tr>"""
            rows.append(row)
        return '\n'.join(rows)

    def generate_dashboard(self, results):
        """Generate the dashboard HTML"""
        # Ensure template directory exists
        self.template_dir.mkdir(parents=True, exist_ok=True)
        
        # Read template
        with open(self.template_path, 'r', encoding='utf-8') as f:
            template = f.read()
        
        # Prepare chart configurations
        scenario_chart, feature_chart = self.prepare_chart_configs(results)
        
        # Generate feature rows
        feature_rows = self.generate_feature_rows(results['features'])
        
        # Prepare template variables
        template_vars = {
            'timestamp': results['timestamp'],
            'total_scenarios': results['total_scenarios'],
            'passed_scenarios': results['passed_scenarios'],
            'failed_scenarios': results['failed_scenarios'],
            'skipped_scenarios': results['skipped_scenarios'],
            'passed_steps': results['passed_steps'],
            'failed_steps': results['failed_steps'],
            'feature_rows': feature_rows,
            'scenario_chart_config': json.dumps(scenario_chart),
            'feature_chart_config': json.dumps(feature_chart)
        }
        
        # Generate HTML
        html = template.format(**template_vars)
        
        # Write dashboard
        os.makedirs('reports', exist_ok=True)
        with open('reports/index.html', 'w', encoding='utf-8') as f:
            f.write(html)
        
        print("Dashboard generated at reports/index.html")

def main():
    """Main function to generate dashboard"""
    try:
        dashboard = DashboardGenerator()
        results = dashboard.load_test_results()
        dashboard.generate_dashboard(results)
    except Exception as e:
        print(f"Error generating dashboard: {e}")
        raise

if __name__ == '__main__':
    main()

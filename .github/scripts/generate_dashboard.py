#!/usr/bin/env python3
"""
Test Results Dashboard Generator
Generates an HTML dashboard from Behave test results
"""

import json
import os
import logging
from datetime import datetime
from pathlib import Path
import xml.etree.ElementTree as ET 

# Set up logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DashboardGenerator:
    def __init__(self):
        self.template_dir = Path(__file__).parent / 'templates'
        self.template_path = self.template_dir / 'dashboard_template.html'
        
        # Initialize with default empty results
        self.default_results = {
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

    def load_test_results(self):
        """Load test results from JUnit XML since JSON parsing is failing"""
        results = self.default_results.copy()
        
        junit_path = 'reports/junit/TESTS-sample_login.xml'
        
        try:
            tree = ET.parse(junit_path)
            root = tree.getroot()
            
            # Parse test suite data
            results['total_scenarios'] = int(root.get('tests', 0))
            results['failed_scenarios'] = int(root.get('failures', 0))
            results['skipped_scenarios'] = int(root.get('skipped', 0))
            results['passed_scenarios'] = (results['total_scenarios'] - 
                                        results['failed_scenarios'] - 
                                        results['skipped_scenarios'])
            
            # Get step counts
            for testcase in root.findall('.//testcase'):
                results['total_steps'] += len(testcase.findall('.//step'))
                # Count passed steps
                for step in testcase.findall('.//system-out'):
                    if 'passed' in step.text:
                        results['passed_steps'] += 1
            
            # Process features
            feature_name = root.get('name', '').split('.')[-1].strip()
            feature_stats = {
                'name': feature_name,
                'description': 'Test automation feature',
                'scenarios': results['total_scenarios'],
                'passed_scenarios': results['passed_scenarios'],
                'failed_scenarios': results['failed_scenarios'],
                'skipped_scenarios': results['skipped_scenarios'],
                'total_steps': results['total_steps'],
                'passed_steps': results['passed_steps'],
                'failed_steps': results['total_steps'] - results['passed_steps']
            }
            results['features'].append(feature_stats)
            
            logger.info(f"Processed {results['total_scenarios']} scenarios")
            logger.info(f"Passed: {results['passed_scenarios']}")
            logger.info(f"Failed: {results['failed_scenarios']}")
            logger.info(f"Steps: {results['total_steps']}")
            
        except Exception as e:
            logger.error(f"Error processing results: {str(e)}", exc_info=True)
        
        return results
    
    def load_junit_results(self):
        """Load results from JUnit XML"""
        junit_path = 'reports/junit/TESTS-sample_login.xml'
        if os.path.exists(junit_path):
            try:
                import xml.etree.ElementTree as ET
                tree = ET.parse(junit_path)
                root = tree.getroot()
                
                # Log the XML content
                logger.info(f"JUnit XML content: {ET.tostring(root, encoding='unicode')}")
                
                return {
                    'total_scenarios': int(root.attrib.get('tests', 0)),
                    'failed_scenarios': int(root.attrib.get('failures', 0)),
                    'skipped_scenarios': int(root.attrib.get('skipped', 0)),
                    'passed_scenarios': int(root.attrib.get('tests', 0)) - 
                                    int(root.attrib.get('failures', 0)) - 
                                    int(root.attrib.get('skipped', 0))
                }
            except Exception as e:
                logger.error(f"Error reading JUnit results: {str(e)}")
        return None

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

        feature_names = [f['name'] for f in results['features']] if results['features'] else ['No Features']
        passed_data = [f['passed_scenarios'] for f in results['features']] if results['features'] else [0]
        failed_data = [f['failed_scenarios'] for f in results['features']] if results['features'] else [0]

        feature_chart = {
            'type': 'bar',
            'data': {
                'labels': feature_names,
                'datasets': [
                    {
                        'label': 'Passed',
                        'data': passed_data,
                        'backgroundColor': '#10B981'
                    },
                    {
                        'label': 'Failed',
                        'data': failed_data,
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

    def generate_dashboard(self, results):
        """Generate the dashboard HTML"""
        logger.info("Generating dashboard...")
        
        # Create necessary directories
        os.makedirs('reports', exist_ok=True)
        self.template_dir.mkdir(parents=True, exist_ok=True)

        # Generate feature rows
        feature_rows = []
        for feature in results['features']:
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
            feature_rows.append(row)

        # Prepare chart configurations
        scenario_chart, feature_chart = self.prepare_chart_configs(results)

        # Generate simple HTML if no template exists
        if not self.template_path.exists():
            logger.warning("Template not found, generating simple HTML")
            html = f"""
            <html>
                <head><title>Test Results</title></head>
                <body>
                    <h1>Test Results</h1>
                    <p>Total Scenarios: {results['total_scenarios']}</p>
                    <p>Passed: {results['passed_scenarios']}</p>
                    <p>Failed: {results['failed_scenarios']}</p>
                    <p>Skipped: {results['skipped_scenarios']}</p>
                </body>
            </html>
            """
        else:
            # Use template
            with open(self.template_path, 'r', encoding='utf-8') as f:
                template = f.read()
                html = template.format(
                    timestamp=results['timestamp'],
                    total_scenarios=results['total_scenarios'],
                    passed_scenarios=results['passed_scenarios'],
                    failed_scenarios=results['failed_scenarios'],
                    skipped_scenarios=results['skipped_scenarios'],
                    passed_steps=results['passed_steps'],
                    failed_steps=results['failed_steps'],
                    feature_rows='\n'.join(feature_rows),
                    scenario_chart_config=json.dumps(scenario_chart),
                    feature_chart_config=json.dumps(feature_chart)
                )

        # Write dashboard
        with open('reports/index.html', 'w', encoding='utf-8') as f:
            f.write(html)
        
        logger.info("Dashboard generated successfully at reports/index.html")

def main():
    """Main function to generate dashboard"""
    try:
        dashboard = DashboardGenerator()
        results = dashboard.load_test_results()
        dashboard.generate_dashboard(results)
    except Exception as e:
        logger.error(f"Error generating dashboard: {str(e)}", exc_info=True)
        raise

if __name__ == '__main__':
    main()

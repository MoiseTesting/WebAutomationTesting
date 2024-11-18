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
        """Load and process test results"""
        results = self.default_results.copy()
        
        logger.info("Starting test results processing")
        logger.info(f"Current working directory: {os.getcwd()}")
        
        json_path = 'reports/behave-report.json'
        
        # Debug: List all files in reports directory
        if os.path.exists('reports'):
            logger.info("Files in reports directory:")
            for root, dirs, files in os.walk('reports'):
                for file in files:
                    logger.info(f"  {os.path.join(root, file)}")
        
        if not os.path.exists(json_path):
            logger.warning(f"JSON report not found at: {json_path}")
            return results
        
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if not content:
                    logger.warning("JSON file is empty")
                    return results
                
                logger.info(f"Reading JSON content (length: {len(content)})")
                logger.debug(f"JSON content: {content[:500]}...")  # Log first 500 chars
                
                json_results = json.loads(content)
                if not json_results:
                    logger.warning("JSON results are empty")
                    return results
                
                # Process each feature
                for feature in json_results:
                    feature_stats = {
                        'name': feature.get('name', 'Unknown'),
                        'description': feature.get('description', ''),
                        'scenarios': 0,
                        'passed_scenarios': 0,
                        'failed_scenarios': 0,
                        'skipped_scenarios': 0,
                        'total_steps': 0,
                        'passed_steps': 0,
                        'failed_steps': 0
                    }
                    
                    # Process scenarios
                    scenarios = feature.get('elements', [])
                    if scenarios:
                        feature_stats['scenarios'] = len(scenarios)
                        for scenario in scenarios:
                            scenario_status = 'passed'
                            steps = scenario.get('steps', [])
                            
                            if steps:
                                feature_stats['total_steps'] += len(steps)
                                for step in steps:
                                    result = step.get('result', {})
                                    status = result.get('status', 'skipped')
                                    
                                    if status == 'passed':
                                        feature_stats['passed_steps'] += 1
                                    elif status == 'failed':
                                        feature_stats['failed_steps'] += 1
                                        scenario_status = 'failed'
                                    
                            if scenario_status == 'passed':
                                feature_stats['passed_scenarios'] += 1
                            else:
                                feature_stats['failed_scenarios'] += 1
                    
                    results['features'].append(feature_stats)
                    
                    # Update totals
                    results['total_scenarios'] += feature_stats['scenarios']
                    results['passed_scenarios'] += feature_stats['passed_scenarios']
                    results['failed_scenarios'] += feature_stats['failed_scenarios']
                    results['total_steps'] += feature_stats['total_steps']
                    results['passed_steps'] += feature_stats['passed_steps']
                    results['failed_steps'] += feature_stats['failed_steps']
                
                logger.info(f"Processed {len(results['features'])} features")
                logger.info(f"Total scenarios: {results['total_scenarios']}")
                
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {str(e)}")
            logger.debug("JSON content causing error:", exc_info=True)
        except Exception as e:
            logger.error(f"Error loading results: {str(e)}", exc_info=True)
        
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

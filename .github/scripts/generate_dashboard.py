
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
        
        # Generate HTML template (previous HTML template code remains the same)
        html = f"""<!DOCTYPE html>
        <!-- Previous HTML template code -->
        """
        
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

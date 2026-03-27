"""
Tool Comparison Script
Compares TerraSecure vs Checkov vs Trivy
"""

import json
import sys
from pathlib import Path
from collections import defaultdict

def load_terrasecure(filepath):
    """Load TerraSecure results"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        issues = data.get('issues', [])
        stats = {
            'total': len(issues),
            'critical': sum(1 for i in issues if i.get('severity', '').upper() == 'CRITICAL'),
            'high': sum(1 for i in issues if i.get('severity', '').upper() == 'HIGH'),
            'medium': sum(1 for i in issues if i.get('severity', '').upper() == 'MEDIUM'),
            'low': sum(1 for i in issues if i.get('severity', '').upper() == 'LOW'),
        }
        
        return {
            'tool': 'TerraSecure',
            'total_issues': stats['total'],
            'critical': stats['critical'],
            'high': stats['high'],
            'medium': stats['medium'],
            'low': stats['low'],
            'ml_enabled': True,
            'ai_enabled': True,
            'issues': issues
        }
    except Exception as e:
        print(f"Error loading TerraSecure results: {e}")
        return None

def load_checkov(filepath):
    """Load Checkov results"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        results = data.get('results', {})
        failed_checks = results.get('failed_checks', [])
        
        severity_map = defaultdict(int)
        for check in failed_checks:
            severity = check.get('check_result', {}).get('result', {}).get('severity', 'MEDIUM')
            severity_map[severity.upper()] += 1
        
        return {
            'tool': 'Checkov',
            'total_issues': len(failed_checks),
            'critical': severity_map.get('CRITICAL', 0),
            'high': severity_map.get('HIGH', 0),
            'medium': severity_map.get('MEDIUM', 0),
            'low': severity_map.get('LOW', 0),
            'ml_enabled': False,
            'ai_enabled': False,
            'issues': failed_checks
        }
    except Exception as e:
        print(f"Error loading Checkov results: {e}")
        return None

def load_trivy(filepath):
    """Load Trivy results"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        results = data.get('Results', [])
        all_misconfigs = []
        
        for result in results:
            misconfigs = result.get('Misconfigurations', [])
            all_misconfigs.extend(misconfigs)
        
        severity_map = defaultdict(int)
        for m in all_misconfigs:
            severity = m.get('Severity', 'MEDIUM')
            severity_map[severity.upper()] += 1
        
        return {
            'tool': 'Trivy',
            'total_issues': len(all_misconfigs),
            'critical': severity_map.get('CRITICAL', 0),
            'high': severity_map.get('HIGH', 0),
            'medium': severity_map.get('MEDIUM', 0),
            'low': severity_map.get('LOW', 0),
            'ml_enabled': False,
            'ai_enabled': False,
            'issues': all_misconfigs
        }
    except Exception as e:
        print(f"Error loading Trivy results: {e}")
        return None

def print_comparison(results):
    """Print comparison table"""
    
    print("\n" + "="*80)
    print("TOOL COMPARISON RESULTS".center(80))
    print("="*80 + "\n")
    
    # Summary table
    print(f"{'Metric':<20} {'TerraSecure':<15} {'Checkov':<15} {'Trivy':<15}")
    print("-" * 80)
    
    terrasecure = next((r for r in results if r['tool'] == 'TerraSecure'), None)
    checkov = next((r for r in results if r['tool'] == 'Checkov'), None)
    trivy = next((r for r in results if r['tool'] == 'Trivy'), None)
    
    if terrasecure:
        print(f"{'Total Issues':<20} {terrasecure['total_issues']:<15} {checkov['total_issues'] if checkov else 'N/A':<15} {trivy['total_issues'] if trivy else 'N/A':<15}")
        print(f"{'Critical':<20} {terrasecure['critical']:<15} {checkov['critical'] if checkov else 'N/A':<15} {trivy['critical'] if trivy else 'N/A':<15}")
        print(f"{'High':<20} {terrasecure['high']:<15} {checkov['high'] if checkov else 'N/A':<15} {trivy['high'] if trivy else 'N/A':<15}")
        print(f"{'Medium':<20} {terrasecure['medium']:<15} {checkov['medium'] if checkov else 'N/A':<15} {trivy['medium'] if trivy else 'N/A':<15}")
        print(f"{'Low':<20} {terrasecure['low']:<15} {checkov['low'] if checkov else 'N/A':<15} {trivy['low'] if trivy else 'N/A':<15}")
        print("-" * 80)
        print(f"{'ML Powered':<20} {'✓ YES':<15} {'✗ NO':<15} {'✗ NO':<15}")
        print(f"{'AI Explanations':<20} {'✓ YES':<15} {'✗ NO':<15} {'✗ NO':<15}")
    
    print("="*80 + "\n")
    
    # Calculate overlap
    if terrasecure and checkov:
        print("\nOVERLAP ANALYSIS:")
        print("-" * 80)
        print(f"TerraSecure unique findings: {terrasecure['total_issues'] - checkov['total_issues']}")
        print(f"Checkov unique findings: {checkov['total_issues'] - terrasecure['total_issues']}")
        print(f"Estimated overlap: ~{min(terrasecure['total_issues'], checkov['total_issues'])} issues")
    
    print("\n" + "="*80 + "\n")

def main():
    if len(sys.argv) < 2:
        print("Usage: python compare_tools.py <terrasecure.json> [checkov.json] [trivy.json]")
        sys.exit(1)
    
    results = []
    
    # Load TerraSecure
    if len(sys.argv) >= 2:
        ts_result = load_terrasecure(sys.argv[1])
        if ts_result:
            results.append(ts_result)
    
    # Load Checkov
    if len(sys.argv) >= 3:
        ck_result = load_checkov(sys.argv[2])
        if ck_result:
            results.append(ck_result)
    
    # Load Trivy
    if len(sys.argv) >= 4:
        tv_result = load_trivy(sys.argv[3])
        if tv_result:
            results.append(tv_result)
    
    if results:
        print_comparison(results)
    else:
        print("No results to compare!")
        sys.exit(1)

if __name__ == "__main__":
    main()
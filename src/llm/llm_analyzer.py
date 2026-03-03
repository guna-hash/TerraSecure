"""
LLM Analyzer for TerraSecure
Provides context-aware security analysis with natural language explanations
"""

import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class LLMAnalyzer:
    """
    Analyzes security issues using LLM for deeper context understanding
    
    Adds:
    - Natural language explanations
    - Business impact analysis
    - Attack scenario descriptions
    - Detailed remediation steps
    """
    
    def __init__(self):
        api_key = os.getenv('OPENAI_API_KEY')
        
        if api_key:
            try:
                self.client = OpenAI(api_key=api_key)
                self.enabled = True
                print("✅ LLM (OpenAI) initialized")
            except Exception as e:
                print(f"⚠️  LLM initialization failed: {e}")
                self.enabled = False
        else:
            print("⚠️  OPENAI_API_KEY not found - LLM analysis disabled")
            self.enabled = False
    
    def enhance_finding(self, resource, ml_result, rule_finding):
        """
        Enhance a security finding with LLM analysis
        
        Args:
            resource: Terraform resource dict
            ml_result: ML model prediction result
            rule_finding: Rule-based detection result
        
        Returns:
            Enhanced finding with LLM insights
        """
        
        if not self.enabled:
            return rule_finding
        
        try:
            # Create analysis prompt
            prompt = self._create_prompt(resource, ml_result, rule_finding)
            
            # Call OpenAI
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a cloud security expert analyzing Terraform configurations. Provide clear, actionable security analysis."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.2,  # Low temperature for consistent, focused responses
                max_tokens=800
            )
            
            # Parse LLM response
            llm_text = response.choices[0].message.content
            llm_data = self._parse_response(llm_text)
            
            # Enhance original finding
            enhanced = {**rule_finding, **llm_data}
            
            return enhanced
        
        except Exception as e:
            print(f"⚠️  LLM analysis failed for {resource.get('name')}: {e}")
            return rule_finding
    
    def _create_prompt(self, resource, ml_result, rule_finding):
        """Create detailed analysis prompt for LLM"""
        
        resource_type = resource.get('type', 'unknown')
        resource_name = resource.get('name', 'unknown')
        properties = json.dumps(resource.get('properties', {}), indent=2)
        
        prompt = f"""Analyze this Terraform security issue:

**RESOURCE:**
Type: {resource_type}
Name: {resource_name}

**CONFIGURATION:**
```
{properties}
```

**DETECTED ISSUE:**
Severity: {rule_finding['severity']}
Message: {rule_finding['message']}
Rule-based Fix: {rule_finding['fix']}

**ML ANALYSIS:**
Risk Score: {ml_result['ml_risk_score']:.0%}
ML Prediction: {ml_result['ml_prediction']}
Triggered Security Features: {', '.join(ml_result['triggered_features'][:5]) if ml_result['triggered_features'] else 'None'}

**YOUR TASK:**
Provide a comprehensive security analysis in JSON format:

{{
  "explanation": "<2-3 sentence clear explanation of WHY this is a security risk>",
  "business_impact": "<What could happen if this is exploited? Be specific.>",
  "attack_scenario": "<Describe a realistic attack in 2-3 sentences>",
  "detailed_fix": "<Step-by-step remediation with code examples>",
  "severity_justification": "<Why this severity level is appropriate>"
}}

Be specific, technical, and actionable. Focus on the actual security implications."""

        return prompt
    
    def _parse_response(self, text):
        """Parse LLM JSON response"""
        
        try:
            # Try to find JSON in response
            start = text.find('{')
            end = text.rfind('}') + 1
            
            if start != -1 and end > start:
                json_str = text[start:end]
                data = json.loads(json_str)
                
                return {
                    'llm_explanation': data.get('explanation', ''),
                    'llm_business_impact': data.get('business_impact', ''),
                    'llm_attack_scenario': data.get('attack_scenario', ''),
                    'llm_detailed_fix': data.get('detailed_fix', ''),
                    'llm_severity_justification': data.get('severity_justification', '')
                }
        
        except Exception as e:
            print(f"⚠️  Could not parse LLM JSON: {e}")
        
        # Fallback: use raw text as explanation
        return {
            'llm_explanation': text[:500] if text else 'LLM analysis unavailable'
        }

# Quick test
if __name__ == '__main__':
    analyzer = LLMAnalyzer()
    
    if analyzer.enabled:
        print("\n✅ LLM Analyzer is ready!")
        print("Test with: python src/cli.py examples/vulnerable")
    else:
        print("\n❌ LLM not available. Check OPENAI_API_KEY in .env")
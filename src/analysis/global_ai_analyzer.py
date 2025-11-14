"""
Global AI Analysis Engine
Multi-model AI consensus system for comprehensive stock analysis
Supports: Claude, GPT-4, Gemini Pro, and Grok
"""
import streamlit as st
import json
import asyncio
import aiohttp
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import pandas as pd
import hashlib
from dataclasses import dataclass
import time


@dataclass
class AIModelConfig:
    """Configuration for each AI model"""
    name: str
    provider: str
    weight: float
    max_tokens: int
    api_endpoint: str
    requires_key: bool
    default_model: str


# Model configurations with token limits and weights
AI_MODELS = {
    'claude': AIModelConfig(
        name='Claude',
        provider='Anthropic',
        weight=0.40,  # 40% weight - Best reasoning
        max_tokens=4096,  # Claude 3.5 Sonnet: 8K output, using 4K for cost
        api_endpoint='https://api.anthropic.com/v1/messages',
        requires_key=True,
        default_model='claude-3-5-sonnet-20241022'
    ),
    'gpt4': AIModelConfig(
        name='GPT-4',
        provider='OpenAI',
        weight=0.30,  # 30% weight - Strong analysis
        max_tokens=4096,  # GPT-4 Turbo: 4K output limit
        api_endpoint='https://api.openai.com/v1/chat/completions',
        requires_key=True,
        default_model='gpt-4-turbo-preview'
    ),
    'gemini': AIModelConfig(
        name='Gemini Pro',
        provider='Google',
        weight=0.20,  # 20% weight - Good synthesis
        max_tokens=2048,  # Gemini Pro: 2K output limit
        api_endpoint='https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent',
        requires_key=True,
        default_model='gemini-pro'
    ),
    'grok': AIModelConfig(
        name='Grok',
        provider='xAI',
        weight=0.10,  # 10% weight - Alternative perspective
        max_tokens=2048,  # Grok: Estimated 2K output
        api_endpoint='https://api.x.ai/v1/chat/completions',
        requires_key=True,
        default_model='grok-beta'
    )
}


class GlobalAIAnalyzer:
    """
    Orchestrates multi-model AI analysis with consensus building.
    Weighted aggregation prioritizes deeper-thinking models.
    """
    
    def __init__(self):
        self.cache = {}
        self.cache_ttl = 3600  # 1 hour cache
        self.load_api_keys()
    
    def load_api_keys(self):
        """Load API keys from Streamlit secrets"""
        try:
            self.api_keys = {
                'claude': st.secrets.get('ANTHROPIC_API_KEY', ''),
                'gpt4': st.secrets.get('OPENAI_API_KEY', ''),
                'gemini': st.secrets.get('GOOGLE_API_KEY', ''),
                'grok': st.secrets.get('XAI_API_KEY', '')
            }
        except:
            self.api_keys = {}
    
    def get_available_models(self) -> List[str]:
        """Return list of models with valid API keys"""
        available = []
        for model_id, key in self.api_keys.items():
            if key and key.strip():
                available.append(model_id)
        return available
    
    def aggregate_dashboard_data(self, data: Dict) -> Dict:
        """
        Collect ALL data from the dashboard for AI analysis.
        This is the comprehensive data package sent to AI models.
        """
        aggregated = {
            'timestamp': datetime.now().isoformat(),
            'ticker': data.get('ticker', 'Unknown'),
            'current_price': data.get('current_price', 0),
            
            # Company fundamentals
            'fundamentals': {
                'market_cap': data.get('market_cap', 0),
                'enterprise_value': data.get('enterprise_value', 0),
                'revenue': data.get('revenue', 0),
                'net_income': data.get('net_income', 0),
                'free_cash_flow': data.get('free_cash_flow', 0),
                'total_debt': data.get('total_debt', 0),
                'cash': data.get('cash', 0),
                'pe_ratio': data.get('pe_ratio', 0),
                'pb_ratio': data.get('pb_ratio', 0),
                'ps_ratio': data.get('ps_ratio', 0),
                'peg_ratio': data.get('peg_ratio', 0),
                'roe': data.get('roe', 0),
                'roa': data.get('roa', 0),
                'profit_margin': data.get('profit_margin', 0),
                'operating_margin': data.get('operating_margin', 0),
            },
            
            # Valuation models
            'valuation': {
                'dcf_value': data.get('dcf_value', 0),
                'dcf_upside': data.get('dcf_upside', 0),
                'zero_fcf_valuations': data.get('zero_fcf_valuations', {}),
                'comparable_multiples': data.get('comparable_multiples', {}),
                'graham_number': data.get('graham_number', 0),
            },
            
            # Technical indicators (from 60+ indicator suite)
            'technical': {
                'trend': data.get('trend_indicators', {}),
                'momentum': data.get('momentum_indicators', {}),
                'volatility': data.get('volatility_indicators', {}),
                'volume': data.get('volume_indicators', {}),
            },
            
            # Options flow
            'options': {
                'delta_divergence': data.get('delta_divergence', {}),
                'put_call_ratio': data.get('put_call_ratio', 0),
                'implied_volatility': data.get('implied_volatility', 0),
                'gamma_exposure': data.get('gamma_exposure', 0),
            },
            
            # Sentiment analysis
            'sentiment': {
                'reddit_sentiment': data.get('reddit_sentiment', {}),
                'market_correlation': data.get('sentiment_correlation', {}),
                'social_volume': data.get('social_volume', 0),
            },
            
            # Insider activity
            'insider': {
                'congressional_trades': data.get('congressional_trades', []),
                'insider_transactions': data.get('insider_transactions', []),
            },
            
            # Economic context
            'economic': {
                'cpi': data.get('cpi', 0),
                'unemployment': data.get('unemployment', 0),
                'gdp_growth': data.get('gdp_growth', 0),
                'interest_rate': data.get('interest_rate', 0),
            },
            
            # User inputs & assumptions
            'user_inputs': data.get('user_inputs', {}),
            
            # Historical performance
            'historical': {
                'ytd_return': data.get('ytd_return', 0),
                'one_year_return': data.get('one_year_return', 0),
                'volatility': data.get('historical_volatility', 0),
                'sharpe_ratio': data.get('sharpe_ratio', 0),
                'max_drawdown': data.get('max_drawdown', 0),
            }
        }
        
        return aggregated
    
    def build_comprehensive_prompt(self, aggregated_data: Dict) -> str:
        """
        Build the master prompt that includes ALL analysis requirements.
        This ensures consistent, comprehensive analysis across all AI models.
        """
        ticker = aggregated_data['ticker']
        price = aggregated_data['current_price']
        
        prompt = f"""You are a world-class financial analyst with decades of experience in fundamental analysis, technical analysis, options trading, sentiment analysis, and macroeconomic forecasting.

# COMPREHENSIVE STOCK ANALYSIS REQUEST

Analyze **{ticker}** (Current Price: ${price:.2f}) using ALL available data below.

## YOUR TASK
Provide a thorough, multi-dimensional analysis covering:
1. **Fundamental Valuation** - DCF, multiples, intrinsic value
2. **Technical Position** - Trend, momentum, key levels
3. **Options Market** - Delta flow, gamma, implied volatility
4. **Sentiment & Psychology** - Reddit, insider activity, market correlation
5. **Macro Context** - Economic indicators, sector trends
6. **Risk Assessment** - Identify major risks & catalysts

## COMPLETE DATA PACKAGE

### 📊 FUNDAMENTALS
{json.dumps(aggregated_data['fundamentals'], indent=2)}

### 💰 VALUATION MODELS
{json.dumps(aggregated_data['valuation'], indent=2)}

### 📈 TECHNICAL INDICATORS
{json.dumps(aggregated_data['technical'], indent=2)}

### 📊 OPTIONS FLOW
{json.dumps(aggregated_data['options'], indent=2)}

### 💬 SENTIMENT DATA
{json.dumps(aggregated_data['sentiment'], indent=2)}

### 👔 INSIDER ACTIVITY
{json.dumps(aggregated_data['insider'], indent=2)}

### 🌍 ECONOMIC CONTEXT
{json.dumps(aggregated_data['economic'], indent=2)}

### 🎯 USER ASSUMPTIONS
{json.dumps(aggregated_data['user_inputs'], indent=2)}

### 📊 HISTORICAL PERFORMANCE
{json.dumps(aggregated_data['historical'], indent=2)}

---

## REQUIRED OUTPUT STRUCTURE

Please provide your analysis in this EXACT JSON format:

{{
  "executive_summary": "2-3 sentence overall assessment",
  
  "valuation_analysis": {{
    "fair_value_estimate": <number>,
    "current_price": <number>,
    "upside_downside_pct": <number>,
    "valuation_method_used": "DCF/Multiples/Hybrid",
    "reasoning": "Why this valuation is appropriate",
    "key_assumptions": ["assumption1", "assumption2"],
    "sensitivity": "How sensitive to key variables"
  }},
  
  "technical_analysis": {{
    "trend": "Bullish/Bearish/Neutral",
    "key_levels": {{
      "support": [<levels>],
      "resistance": [<levels>]
    }},
    "momentum_score": <0-100>,
    "pattern_recognition": "Identified patterns",
    "short_term_outlook": "Next 1-4 weeks",
    "medium_term_outlook": "Next 1-3 months"
  }},
  
  "options_insights": {{
    "market_expectation": "What options market expects",
    "delta_bias": "Call/Put dominant",
    "key_strikes": [<important strikes>],
    "implied_vs_realized_vol": "Expensive/Cheap/Fair",
    "gamma_risk": "Low/Medium/High"
  }},
  
  "sentiment_score": {{
    "overall_sentiment": <-100 to +100>,
    "retail_sentiment": "Bullish/Bearish/Neutral",
    "institutional_positioning": "Accumulating/Distributing/Neutral",
    "insider_signal": "Positive/Negative/Neutral",
    "contrarian_view": "Is consensus wrong?"
  }},
  
  "bull_case": {{
    "arguments": ["Strong point 1", "Strong point 2", "Strong point 3"],
    "probability": <0-100>,
    "upside_target": <price>,
    "timeframe": "X months"
  }},
  
  "bear_case": {{
    "arguments": ["Risk 1", "Risk 2", "Risk 3"],
    "probability": <0-100>,
    "downside_target": <price>,
    "timeframe": "X months"
  }},
  
  "risk_assessment": {{
    "key_risks": ["Major risk 1", "Major risk 2"],
    "risk_level": "Low/Medium/High/Extreme",
    "black_swan_scenarios": ["Unlikely but catastrophic event"],
    "hedging_suggestions": "How to mitigate risk"
  }},
  
  "devils_advocate": {{
    "critique_of_bull_case": "Why bulls could be wrong",
    "critique_of_bear_case": "Why bears could be wrong",
    "overlooked_factors": ["Factor market is ignoring"],
    "alternative_interpretation": "Different way to view the data"
  }},
  
  "action_recommendation": {{
    "decision": "Strong Buy/Buy/Hold/Sell/Strong Sell",
    "conviction_level": <0-100>,
    "reasoning": "Why this recommendation",
    "conditions": "Under what conditions to act",
    "position_sizing": "Appropriate allocation %",
    "entry_strategy": "How to enter position",
    "exit_strategy": "When to take profits/cut losses"
  }},
  
  "suggested_adjustments": {{
    "model_refinements": ["Suggestion 1", "Suggestion 2"],
    "data_to_collect": ["Additional data needed"],
    "assumptions_to_revisit": ["Which assumptions to question"],
    "alternative_approaches": ["Different analytical angles"]
  }},
  
  "confidence_score": {{
    "overall_confidence": <0-100>,
    "confidence_breakdown": {{
      "fundamental_analysis": <0-100>,
      "technical_analysis": <0-100>,
      "sentiment_analysis": <0-100>,
      "macro_analysis": <0-100>
    }},
    "uncertainty_factors": ["Source of uncertainty 1", "Source 2"],
    "what_would_increase_confidence": "What data/events needed"
  }},
  
  "catalysts": {{
    "positive_catalysts": ["Upcoming catalyst 1", "Catalyst 2"],
    "negative_catalysts": ["Risk event 1", "Risk event 2"],
    "timeline": "When to expect movement",
    "probability_weighted_impact": "Expected value of catalysts"
  }},
  
  "comparable_analysis": {{
    "peer_comparison": "How this stock compares to peers",
    "relative_valuation": "Expensive/Cheap vs peers",
    "competitive_position": "Market share, moat assessment",
    "sector_trends": "Tailwinds/headwinds"
  }}
}}

## CRITICAL REQUIREMENTS
1. **Be Brutally Honest** - No sugar coating
2. **Show Your Work** - Explain reasoning with data
3. **Challenge Assumptions** - Play devil's advocate
4. **Quantify Everything** - Provide specific numbers
5. **Consider All Timeframes** - Short, medium, long-term
6. **Identify What's Missing** - What data would improve analysis
7. **Give Actionable Insights** - Not just theory, but practical next steps

Return ONLY valid JSON. No markdown, no explanations outside the JSON structure.
"""
        
        return prompt
    
    async def call_claude(self, prompt: str) -> Tuple[Optional[Dict], Optional[str]]:
        """Call Claude API (Anthropic)"""
        if 'claude' not in self.api_keys or not self.api_keys['claude']:
            return None, "Claude API key not configured"
        
        config = AI_MODELS['claude']
        
        try:
            headers = {
                'x-api-key': self.api_keys['claude'],
                'anthropic-version': '2023-06-01',
                'content-type': 'application/json'
            }
            
            payload = {
                'model': config.default_model,
                'max_tokens': config.max_tokens,
                'messages': [
                    {'role': 'user', 'content': prompt}
                ]
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    config.api_endpoint,
                    headers=headers,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=60)
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        content = result['content'][0]['text']
                        # Parse JSON from response
                        json_start = content.find('{')
                        json_end = content.rfind('}') + 1
                        if json_start >= 0 and json_end > json_start:
                            json_str = content[json_start:json_end]
                            return json.loads(json_str), None
                        return None, "Could not parse JSON from response"
                    else:
                        error_text = await response.text()
                        return None, f"API error {response.status}: {error_text}"
        
        except Exception as e:
            return None, f"Exception: {str(e)}"
    
    async def call_gpt4(self, prompt: str) -> Tuple[Optional[Dict], Optional[str]]:
        """Call GPT-4 API (OpenAI)"""
        if 'gpt4' not in self.api_keys or not self.api_keys['gpt4']:
            return None, "GPT-4 API key not configured"
        
        config = AI_MODELS['gpt4']
        
        try:
            headers = {
                'Authorization': f'Bearer {self.api_keys["gpt4"]}',
                'Content-Type': 'application/json'
            }
            
            payload = {
                'model': config.default_model,
                'messages': [
                    {'role': 'system', 'content': 'You are a world-class financial analyst. Respond only with valid JSON.'},
                    {'role': 'user', 'content': prompt}
                ],
                'max_tokens': config.max_tokens,
                'temperature': 0.7,
                'response_format': {'type': 'json_object'}
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    config.api_endpoint,
                    headers=headers,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=60)
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        content = result['choices'][0]['message']['content']
                        return json.loads(content), None
                    else:
                        error_text = await response.text()
                        return None, f"API error {response.status}: {error_text}"
        
        except Exception as e:
            return None, f"Exception: {str(e)}"
    
    async def call_gemini(self, prompt: str) -> Tuple[Optional[Dict], Optional[str]]:
        """Call Gemini API (Google)"""
        if 'gemini' not in self.api_keys or not self.api_keys['gemini']:
            return None, "Gemini API key not configured"
        
        config = AI_MODELS['gemini']
        
        try:
            url = f"{config.api_endpoint}?key={self.api_keys['gemini']}"
            
            payload = {
                'contents': [{
                    'parts': [{'text': prompt}]
                }],
                'generationConfig': {
                    'maxOutputTokens': config.max_tokens,
                    'temperature': 0.7
                }
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    url,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=60)
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        content = result['candidates'][0]['content']['parts'][0]['text']
                        # Parse JSON
                        json_start = content.find('{')
                        json_end = content.rfind('}') + 1
                        if json_start >= 0 and json_end > json_start:
                            json_str = content[json_start:json_end]
                            return json.loads(json_str), None
                        return None, "Could not parse JSON from response"
                    else:
                        error_text = await response.text()
                        return None, f"API error {response.status}: {error_text}"
        
        except Exception as e:
            return None, f"Exception: {str(e)}"
    
    async def call_grok(self, prompt: str) -> Tuple[Optional[Dict], Optional[str]]:
        """Call Grok API (xAI)"""
        if 'grok' not in self.api_keys or not self.api_keys['grok']:
            return None, "Grok API key not configured"
        
        config = AI_MODELS['grok']
        
        try:
            headers = {
                'Authorization': f'Bearer {self.api_keys["grok"]}',
                'Content-Type': 'application/json'
            }
            
            payload = {
                'model': config.default_model,
                'messages': [
                    {'role': 'system', 'content': 'You are a world-class financial analyst. Respond only with valid JSON.'},
                    {'role': 'user', 'content': prompt}
                ],
                'max_tokens': config.max_tokens,
                'temperature': 0.7
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    config.api_endpoint,
                    headers=headers,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=60)
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        content = result['choices'][0]['message']['content']
                        # Parse JSON
                        json_start = content.find('{')
                        json_end = content.rfind('}') + 1
                        if json_start >= 0 and json_end > json_start:
                            json_str = content[json_start:json_end]
                            return json.loads(json_str), None
                        return None, "Could not parse JSON from response"
                    else:
                        error_text = await response.text()
                        return None, f"API error {response.status}: {error_text}"
        
        except Exception as e:
            return None, f"Exception: {str(e)}"
    
    async def analyze_with_all_models(
        self, 
        aggregated_data: Dict,
        selected_models: Optional[List[str]] = None
    ) -> Dict:
        """
        Call all available AI models in parallel and aggregate results.
        """
        # Build the comprehensive prompt
        prompt = self.build_comprehensive_prompt(aggregated_data)
        
        # Check cache
        cache_key = hashlib.md5(json.dumps(aggregated_data, sort_keys=True).encode()).hexdigest()
        if cache_key in self.cache:
            cached_time, cached_result = self.cache[cache_key]
            if time.time() - cached_time < self.cache_ttl:
                return cached_result
        
        # Determine which models to use
        available = self.get_available_models()
        
        if selected_models:
            # User selected specific model(s)
            models_to_use = [m for m in selected_models if m in available]
        else:
            # Use all available models
            models_to_use = available
        
        if not models_to_use:
            return {
                'error': 'No AI models available. Please configure API keys.',
                'available_models': available
            }
        
        # Call models in parallel
        tasks = []
        model_names = []
        
        for model_id in models_to_use:
            if model_id == 'claude':
                tasks.append(self.call_claude(prompt))
            elif model_id == 'gpt4':
                tasks.append(self.call_gpt4(prompt))
            elif model_id == 'gemini':
                tasks.append(self.call_gemini(prompt))
            elif model_id == 'grok':
                tasks.append(self.call_grok(prompt))
            model_names.append(model_id)
        
        # Execute all calls in parallel
        results = await asyncio.gather(*tasks)
        
        # Aggregate responses
        model_responses = {}
        successful_models = []
        
        for model_id, (response, error) in zip(model_names, results):
            if response:
                model_responses[model_id] = response
                successful_models.append(model_id)
            else:
                model_responses[model_id] = {'error': error}
        
        # Build consensus
        if successful_models:
            consensus = self.build_consensus(model_responses, successful_models)
        else:
            consensus = {
                'error': 'All AI models failed',
                'details': model_responses
            }
        
        result = {
            'consensus': consensus,
            'individual_responses': model_responses,
            'models_used': models_to_use,
            'successful_models': successful_models,
            'timestamp': datetime.now().isoformat()
        }
        
        # Cache result
        self.cache[cache_key] = (time.time(), result)
        
        return result
    
    def build_consensus(self, model_responses: Dict, successful_models: List[str]) -> Dict:
        """
        Build weighted consensus from multiple AI model responses.
        Prioritizes deeper-thinking models (Claude 40%, GPT-4 30%, etc.)
        """
        # Extract key metrics from each model
        consensus = {
            'executive_summary': '',
            'fair_value': 0,
            'upside_pct': 0,
            'recommendation': '',
            'conviction': 0,
            'confidence': 0,
            'bull_case_strength': 0,
            'bear_case_strength': 0,
            'risk_level': '',
            'key_insights': [],
            'model_agreement': {}
        }
        
        # Weighted aggregation
        total_weight = sum(AI_MODELS[m].weight for m in successful_models)
        
        for model_id in successful_models:
            response = model_responses[model_id]
            weight = AI_MODELS[model_id].weight / total_weight
            
            # Aggregate numeric values
            if 'valuation_analysis' in response:
                val = response['valuation_analysis']
                consensus['fair_value'] += val.get('fair_value_estimate', 0) * weight
                consensus['upside_pct'] += val.get('upside_downside_pct', 0) * weight
            
            if 'action_recommendation' in response:
                action = response['action_recommendation']
                consensus['conviction'] += action.get('conviction_level', 0) * weight
            
            if 'confidence_score' in response:
                conf = response['confidence_score']
                consensus['confidence'] += conf.get('overall_confidence', 0) * weight
            
            if 'bull_case' in response:
                consensus['bull_case_strength'] += response['bull_case'].get('probability', 0) * weight
            
            if 'bear_case' in response:
                consensus['bear_case_strength'] += response['bear_case'].get('probability', 0) * weight
        
        # Consensus recommendation (most common)
        recommendations = []
        for model_id in successful_models:
            if 'action_recommendation' in model_responses[model_id]:
                rec = model_responses[model_id]['action_recommendation'].get('decision', '')
                if rec:
                    recommendations.append(rec)
        
        if recommendations:
            # Most frequent recommendation
            consensus['recommendation'] = max(set(recommendations), key=recommendations.count)
        
        # Build executive summary from all models
        summaries = []
        for model_id in successful_models:
            if 'executive_summary' in model_responses[model_id]:
                summary = model_responses[model_id]['executive_summary']
                model_name = AI_MODELS[model_id].name
                summaries.append(f"**{model_name}**: {summary}")
        
        consensus['executive_summary'] = '\n\n'.join(summaries)
        
        # Calculate agreement metrics
        fair_values = [
            model_responses[m].get('valuation_analysis', {}).get('fair_value_estimate', 0)
            for m in successful_models
            if 'valuation_analysis' in model_responses[m]
        ]
        
        if fair_values:
            consensus['model_agreement']['fair_value_std_dev'] = pd.Series(fair_values).std()
            consensus['model_agreement']['fair_value_range'] = (min(fair_values), max(fair_values))
        
        return consensus


def get_global_ai_analyzer():
    """Factory function to get GlobalAIAnalyzer instance"""
    return GlobalAIAnalyzer()

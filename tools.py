"""
AI Compliance Tools - AI合规工具
支持合规检查、审计、政策生成
"""

import json
import os
from typing import Dict, List, Any
from datetime import datetime

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


class AIComplianceTools:
    """
    AI合规工具
    支持：检查、审计、政策
    """

    def __init__(self, model: str = "mimo-v2.5-pro", api_key: str = None, base_url: str = None):
        self.model = model
        if OPENAI_AVAILABLE:
            self.client = OpenAI(
                api_key=api_key or os.environ.get('OPENAI_API_KEY', ''),
                base_url=base_url or os.environ.get('OPENAI_BASE_URL', 'https://api.xiaomimimo.com/v1')
            )
        else:
            self.client = None

    def check_compliance(self, system_description: str, regulation: str) -> Dict:
        """检查合规性"""
        if not self.client:
            return {"error": "LLM客户端未配置"}

        prompt = f"""请检查系统是否符合{regulation}：

{system_description[:1000]}

请返回JSON格式：
{{
    "compliance_score": 1-100,
    "compliant": ["符合项"],
    "non_compliant": ["不符合项"],
    "recommendations": ["建议"]
}}"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500
        )

        try:
            content = response.choices[0].message.content
            import re
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except:
            pass

        return {"compliance": content}

    def generate_privacy_policy(self, company: str, data_types: List[str]) -> str:
        """生成隐私政策"""
        if not self.client:
            return "LLM客户端未配置"

        types_text = ", ".join(data_types)

        prompt = f"""请为{company}生成隐私政策：

收集的数据类型：{types_text}

要求：
1. 符合GDPR
2. 清晰易懂
3. 包含用户权利"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=3000
        )

        return response.choices[0].message.content

    def generate_terms_of_service(self, company: str, service_type: str) -> str:
        """生成服务条款"""
        if not self.client:
            return "LLM客户端未配置"

        prompt = f"""请为{company}生成{service_type}服务条款：

要求：
1. 法律合规
2. 用户友好
3. 包含免责声明"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=3000
        )

        return response.choices[0].message.content

    def design_audit_trail(self, system: str, requirements: List[str]) -> Dict:
        """设计审计跟踪"""
        if not self.client:
            return {"error": "LLM客户端未配置"}

        req_text = ", ".join(requirements)

        prompt = f"""请为{system}设计审计跟踪：

需求：{req_text}

请返回JSON格式：
{{
    "events": ["审计事件"],
    "storage": "存储方案",
    "retention": "保留策略"
}}"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500
        )

        try:
            content = response.choices[0].message.content
            import re
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except:
            pass

        return {"audit": content}

    def generate_data_processing_agreement(self, controller: str, processor: str) -> str:
        """生成数据处理协议"""
        if not self.client:
            return "LLM客户端未配置"

        prompt = f"""请生成数据处理协议：

数据控制者：{controller}
数据处理者：{processor}

要求：
1. 符合GDPR
2. 明确责任
3. 安全措施"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2000
        )

        return response.choices[0].message.content

    def assess_risk(self, system_description: str) -> Dict:
        """评估风险"""
        if not self.client:
            return {"error": "LLM客户端未配置"}

        prompt = f"""请评估以下系统的合规风险：

{system_description[:1000]}

请返回JSON格式：
{{
    "risk_level": "high/medium/low",
    "risks": [
        {{"risk": "风险", "probability": "概率", "impact": "影响", "mitigation": "缓解措施"}}
    ]
}}"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500
        )

        try:
            content = response.choices[0].message.content
            import re
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except:
            pass

        return {"risk": content}


def create_tools(**kwargs) -> AIComplianceTools:
    """创建合规工具"""
    return AIComplianceTools(**kwargs)


if __name__ == "__main__":
    tools = create_tools()

    print("AI Compliance Tools")
    print()

    # 测试
    result = tools.check_compliance("用户注册系统，收集邮箱和姓名", "GDPR")
    print(json.dumps(result, ensure_ascii=False, indent=2))

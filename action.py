from loguru import logger

from LLM import *
from tools import *


def search(question, data=None):
    logger.debug(f"{question} -> 触发search行动 -> {data}")
    PROMPT = f"""
分析所给问题，给出key和value，中文。
问题：{question}
数据表属性1：公司名称,公司简称,英文名称,关联证券,公司代码,曾用简称,所属市场,所属行业,上市日期,法人代表,总经理,董秘,邮政编码,注册地址,办公地址,联系电话,传真,官方网址,电子邮箱,入选指数,主营业务,经营范围,机构简介,每股面值,首发价格,首发募资净额,首发主承销商
数据表属性2:公司名称,登记状态,统一社会信用代码,注册资本,成立日期,省份,城市,区县,注册号,组织机构代码,参保人数,企业类型,曾用名
数据表属性3：关联上市公司股票代码, 关联上市公司股票简称, 关联上市公司全称, 上市公司关系, 上市公司参股比例, 上市公司投资金额, 公司名称
数据表属性4：标题, 案号, 文书类型, 原告, 被告, 原告律师, 被告律师, 案由, 审理法条依据, 涉案金额, 判决结果, 胜诉方, 文件名

----
例子：所有案件中，涉及案由技术服务合同纠纷的历史案件数量是多少？
{{
    "key": "案由",
    "value": "技术服务合同纠纷"
}}
----
请按照以下json格式进行输出，可以被Python json.loads函数解析。不回答问题，不作任何解释，不输出其他任何信息。
```json
{{
    "key": "",
    "value" ""
}}
```
"""
    response = LLM(PROMPT)
    feature = prase_json_from_response(response)
    logger.debug(f"feature {feature}")

    api_name, api_args = get_tools_response(feature['key'] + ':' + feature['value'] + '\n' + question.split('\n')[-1])
    logger.debug(f"api_name {api_name}")
    logger.debug(f"api_args {api_args}")

    answer_list = []

    api_response = API(api_name=api_name, args=api_args)
    logger.debug(f"api_response {api_response}")
    answer_list.append(feature['key'] + '为' + feature['value'] + '的是' + f"{api_response[feature['key']]}")
    # data = [data] if not isinstance(data, list) else data
    # for res in data:
    #     logger.debug(f"res {res}")
    #     api_name, api_args = get_tools_response(list(res.values())[0] + '\n' + question.split('\n')[-1])
    #     logger.debug(f"api_name {api_name}")
    #     logger.debug(f"api_args {api_args}")
    #     try:
    #         api_args['case_num'] = api_args['case_num'].replace('（', '(').replace('）', ')')
    #     except:
    #         pass
    #     api_response = API(api_name=api_name, args=api_args)
    #     answer_list.append(f"{list(res.values())[0]}的{feature['搜索属性']}为{api_response[feature['搜索属性']]}")
    return str(answer_list), answer_list


def retrieve(question, data=None):
    logger.debug(f"{question} -> 触发retrieve行动 -> {data}")
    PROMPT = f"""
获取问题中的公司名称。没有则输出“None”。
问题："{question}"
直接输出json，可以被Python json.loads函数解析。不作解释，不作答：
```json
{{
    "公司名称": ""
}}
```
"""
    #     PROMPT = f"""
    # 分析所给问题，给出查询属性，中文。
    # 问题：{question}
    # 数据表属性1：公司名称,公司简称,英文名称,关联证券,公司代码,曾用简称,所属市场,所属行业,上市日期,法人代表,总经理,董秘,邮政编码,注册地址,办公地址,联系电话,传真,官方网址,电子邮箱,入选指数,主营业务,经营范围,机构简介,每股面值,首发价格,首发募资净额,首发主承销商
    # 数据表属性2:公司名称,登记状态,统一社会信用代码,注册资本,成立日期,省份,城市,区县,注册号,组织机构代码,参保人数,企业类型,曾用名
    # 数据表属性3：关联上市公司股票代码, 关联上市公司股票简称, 关联上市公司全称, 上市公司关系, 上市公司参股比例, 上市公司投资金额, 公司名称
    # 数据表属性4：标题, 案号, 文书类型, 原告, 被告, 原告律师, 被告律师, 案由, 审理法条依据, 涉案金额, 判决结果, 胜诉方, 文件名
    #
    # ----
    # 例子：这些子公司的上市公司参股比例分别是多少？
    # {{
    #     "查询属性": "上市公司参股比例"
    # }}
    # ----
    # 请按照以下json格式进行输出，可以被Python json.loads函数解析。不回答问题，不作任何解释，不输出其他任何信息。
    # ```json
    # {{
    #     "查询属性": ""
    # }}
    # ```
    # """

    api_response = []
    logger.warning(f"PROMPT: {PROMPT}")
    response = LLM(PROMPT)
    company_name = prase_json_from_response(response)['公司名称']
    company_name = None if company_name == 'None' else company_name
    if company_name is not None:
        new_question = question
        api_response.append(API(api_name='get_company_info', args={'company_name': company_name}))
        api_response.append(API(api_name='get_company_register', args={'company_name': company_name}))
        if len(api_response[-1]) == 0 and len(api_response[-2]) == 0:
            new_company_name, info = company_name_check(company_name)
            new_question = question.replace(company_name, new_company_name)
            question = question + info
        api_name, api_args = get_tools_response(new_question)
        ori_answer = API(api_name=api_name, args=api_args)
    else:
        api_name, api_args = get_tools_response(question)
        try:
            api_args['case_num'] = api_args['case_num'].replace('（', '(').replace('）', ')')
        except:
            pass
        ori_answer = API(api_name=api_name, args=api_args)
    answer = refine_answer(question, ori_answer)
    return answer, ori_answer


def stat(question, data=None):
    logger.debug(f"{question} -> 触发retrieve行动 -> {data}")

    return f"据统计，共{len(data)}", None


def order(question, data=None):
    logger.debug(f"{question} -> 触发retrieve行动 -> {data}")

    PROMPT = f"""
分析所给问题，给出排序属性与最终数量。
问题：{question}
----
请按照以下json格式进行输出，可以被Python json.loads函数解析。不回答问题，不作任何解释，不输出其他任何信息。
对于查询类问题，补充原有属性的具体属性名称。
```json
{{
    "排序属性": "",
    "最终数量": ""
}}
```
"""
    import heapq
    def top_k_elements_with_indices(lst, k):
        indexed_lst = [(val, idx) for idx, val in enumerate(lst)]
        top_k = heapq.nlargest(k, indexed_lst)
        top_k_values, top_k_indices = zip(*top_k)
        return list(top_k_indices), list(top_k_values)

    response = LLM(PROMPT)
    feature = prase_json_from_response(response)

    name_list = []
    value_list = []
    data = [data] if not isinstance(data, list) else data
    for res in data:
        api_name, api_args = get_tools_response(list(res.values())[0] + '的' + feature['排序属性'])
        api_response = API(api_name=api_name, args=api_args)
        name_list.append(api_response)
        value = api_response[feature['排序属性']]
        if value is None:
            value = 0
        value_list.append(float(value))

    idx, _ = top_k_elements_with_indices(value_list, int(feature['最终数量']))
    target = [name_list[i] for i in idx]
    ori_answer = f"排序后的结果：{target}"
    answer = refine_answer(question, ori_answer)
    return answer, ori_answer


def summary(question, data=None):
    logger.debug(f"{question} -> 触发retrieve行动 -> {data}")

    return refine_answer(question, data), None


def multi_retrieve(question, data=None):
    logger.debug(f"{question} -> 触发multi_retrieve行动 -> {data}")
    PROMPT = f"""
分析所给问题，给出查询属性，中文。
问题：{question}
数据表属性1：标题, 案号, 文书类型, 原告, 被告, 原告律师, 被告律师, 案由, 审理法条依据, 涉案金额, 判决结果, 胜诉方, 文件名
数据表属性2：关联上市公司股票代码, 关联上市公司股票简称, 关联上市公司全称, 上市公司关系, 上市公司参股比例, 上市公司投资金额, 公司名称
----
例子：这些子公司的上市公司参股比例分别是多少？
{{
    "查询属性": "上市公司参股比例"
}}
----
请按照以下json格式进行输出，可以被Python json.loads函数解析。不回答问题，不作任何解释，不输出其他任何信息。
```json
{{
    "查询属性": ""
}}
```
"""
    response = LLM(PROMPT)
    feature = prase_json_from_response(response)
    answer_list = []
    data = [data] if not isinstance(data, list) else data
    for res in data:
        logger.debug(f"multi_retrieve res {res}")
        api_name, api_args = get_tools_response(list(res.values())[0] + '\n' + question.split('\n')[-1])
        try:
            api_args['case_num'] = api_args['case_num'].replace('（', '(').replace('）', ')')
        except:
            pass
        api_response = API(api_name=api_name, args=api_args)
        answer_list.append(f"{list(res.values())[0]}的{feature['查询属性']}为{api_response[feature['查询属性']]}")
    return str(answer_list), answer_list


# 暂且写成hard code，自行改进
def filter_list(question, data=None):
    logger.debug(f"{question} -> 触发filter_list行动 -> {data}")

    PROMPT = f"""
分析所给问题，给出问题分类，并提取公司名称。
问题：{question}
----
1: 如“华仁药业股份有限公司控股的子公司，超过50%的有几家？”
2: 如“大众交通（集团）股份有限公司中，投资超5000万的子公司有多少家？”
3: 如“熊猫乳品集团股份有限公司的全资控股子公司有几家？”
----
请按照以下json格式进行输出，可以被Python json.loads函数解析。不回答问题，不作任何解释，不输出其他任何信息。
对于查询类问题，补充原有属性的具体属性名称。
```json
{{
    "问题类别序号": "",
    "公司名称": ""
}}
```
"""
    response = LLM(PROMPT)
    feature = prase_json_from_response(response)
    data = [data] if not isinstance(data, list) else data
    sub_com = []
    category = int(feature["问题类别序号"]) if isinstance(feature["问题类别序号"], str) else feature["问题类别序号"]
    if category == 1:
        for res in data:
            sub = API(api_name='get_sub_company_info', args={'company_name': res['公司名称']})
            if sub['上市公司参股比例'] is not None and float(sub['上市公司参股比例']) >= 50.0:
                sub_com.append(sub)
    elif category == 2:
        for res in data:
            sub = API(api_name='get_sub_company_info', args={'company_name': res['公司名称']})
            if sub['上市公司投资金额'] is not None:
                cash = sub['上市公司投资金额']
                if '万' in cash:
                    cash = float(cash[:-1])
                elif '亿' in cash:
                    cash = float(cash[:-1]) * 10000
                else:
                    cash = float(cash)
                if cash >= 5000:
                    sub_com.append(sub)
    else:
        for res in data:
            sub = API(api_name='get_sub_company_info', args={'company_name': res['公司名称']})
            if sub['上市公司参股比例'] is not None and float(sub['上市公司参股比例']) == 100:
                sub_com.append(res['公司名称'])

    answer = f"满足条件的子公司数量为{len(sub_com)}"
    return answer, sub_com


# 暂且写成hard code，自行改进
def calculate_cash(question, data=None):
    logger.debug(f"{question} -> 触发calculate_cash行动 -> {data}")

    data = [data] if not isinstance(data, list) else data
    cash = 0
    for res in data:
        sub = API(api_name='get_sub_company_info', args={'company_name': res['公司名称']})
        if sub['上市公司投资金额'] is not None:
            sub_cash = sub['上市公司投资金额']
            if '万' in sub_cash:
                sub_cash = float(sub_cash[:-1]) / 10000
            elif '亿' in sub_cash:
                sub_cash = float(sub_cash[:-1])
            else:
                sub_cash = float(sub_cash[:-1]) / 10000
            cash += sub_cash
    return f"共投资{cash}亿元", cash

import sys

from action import *
from LLM import *
# from tool.logging_config import LoggerConfig,logger
from tools import *
from complex import *
from prompt import COMPLEX_QUESTION, TABLE_PLAN_PROMPT
# logger_config = LoggerConfig()

def execute_plan(question, plan_id):
    if plan_id == 2:
        # 处理几个复杂问题
        response = LLM(COMPLEX_QUESTION.format(question=question))
        logger.debug(prase_json_from_response(response)['类别序号'])
        category = int(prase_json_from_response(response)['类别序号'])
        plan_map = {6: plan_1, 7: plan_2, 8: plan_3, 9: plan_4}
        if category >= 6:
            answer = plan_map[category](question)
            return answer
        else:
            question = refine_question(question)

    p = TABLE_PLAN_PROMPT[plan_id-1]
    logger.warning(f"TABLE_PLAN_PROMPT[plan_id-1]: {p}")
    response = LLM(TABLE_PLAN_PROMPT[plan_id-1].format(question=question))
    logger.debug(f"po response: {response}")
    plan = prase_json_from_response(response)

    # 执行plan
    plan_map = {"查询": retrieve, "统计": stat, "排序": order, "总结": summary, "多次查询": multi_retrieve, "条件筛选": filter_list, "总金额计算": calculate_cash,"搜索":search}
    answer=[]
    data=None
    sub_answer=''
    for sub_plan in plan:
        try:
            if sub_plan["是否需要前序结果"] == 'False':
                question = sub_plan['问题']
            else:
                question = sub_answer+'\n'+sub_plan['问题']
            logger.debug(f"sub_plan: {sub_plan}")
            sub_answer, data = plan_map[sub_plan['操作']](question, data)
            logger.debug(f"sub_answer: {sub_answer}")
            logger.debug(f"data: {data}")
            answer.append(sub_answer)
        except Exception as e:
            logger.error(f'被跳过的问题: {sub_plan}')
            logger.error(f"发生异常: {e}")
            logger.exception("An error occurred")
            pass
    return answer
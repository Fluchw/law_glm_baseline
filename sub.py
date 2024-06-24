import json

from LLM import LLM, refine_answer
from execute_plan import execute_plan
from prompt import TABLE_PROMPT, QUESTION_CLASS
from execute_plan import logger
from tools import prase_json_from_response

# logger.remove(0)
# logger.add(sys.stderr, level="DEBUG")
# # logger.add(sys.stderr, level="INFO")
# # 应用日志配置
# logger_config = LoggerConfig(append=0)  # 设置append为1以续写日志
# logger_config.configure_logging()


Table_solution = []

table_plan_map = {'company_info': 1, 'company_register': 1, 'sub_company_info': 2, 'legal_document': 3}

with open('question(1).json', 'r', encoding='utf-8') as f:
    lines = f.readlines()
data = [json.loads(line.strip()) for line in lines]


def test(id):
    n = 0
    for q in data:
        if q['id'] == id:

            # try:
            #     ans = q['answer']
            #     continue
            # except:
            question = q['question']
            print(q['id'], question)
            try:
                ### 问题分类：直接作答、需要检索
                prompt = QUESTION_CLASS.format(question=question)
                response = prase_json_from_response(LLM(prompt))
                logger.debug(response)
                if response["category_name"] == "direct_answer":
                    answer = LLM(query=question)
                    logger.debug(answer)
                else:
                    ### 表-方案分类：
                    response = LLM(TABLE_PROMPT.format(question=q['question']))
                    logger.debug(f"response {response}")
                    plan_id = table_plan_map[prase_json_from_response(response)["名称"]]
                    logger.debug(f"plan_id: {plan_id}")
                    answer = execute_plan(question, plan_id)
                    logger.debug(response)
                    logger.debug(answer)
                    answer = refine_answer(q['question'], answer)
                    logger.debug(answer)
            except:
                answer = q['question']
            q['answer'] = answer
            print(q['answer'])
        else:
            pass


# with open("submission.json", "w", encoding="utf-8") as f:
#     for item in data:
#         f.write(json.dumps(item, ensure_ascii=False) + "\n")
def run():
    # n = 0
    for q in data:
        # if q['id'] == n:

        try:
            ans = q['answer']
            continue
        except:
            question = q['question']
            print(q['id'], question)
            try:
                ### 问题分类：直接作答、需要检索
                prompt = QUESTION_CLASS.format(question=question)
                response = prase_json_from_response(LLM(prompt))
                if response["category_name"] == "direct_answer":
                    answer = LLM(query=question)
                else:
                    ### 表-方案分类：
                    response = LLM(TABLE_PROMPT.format(question=q['question']))
                    plan_id = table_plan_map[prase_json_from_response(response)["名称"]]
                    answer = execute_plan(question, plan_id)
                    answer = refine_answer(q['question'], answer)
            except:
                answer = q['question']
            q['answer'] = answer
            print(q['answer'])
    # else:
    #     pass

    with open("submission.json", "w", encoding="utf-8") as f:
        for item in data:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")


# run()
# test(56)
test(95)

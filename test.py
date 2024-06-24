from prompt import QUESTION_CLASS

question = "请问批发业注册资本最高的前3家公司的名称以及他们的注册资本（单位为万元）？"
prompt =QUESTION_CLASS.format(question=question)
print(prompt)
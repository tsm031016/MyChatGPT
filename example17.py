"""
自定义聊天机器人
"""
import streamlit as st
from openai import OpenAI

from common import get_llm_response

def get_answer(question: str) :
    """
      从大模型获取答案
      :param question: 用户的问题
      :return: 迭代器对象
    """
    try:
        client = OpenAI(base_url=base_url, api_key=api_key)
        # return get_llm_response(client, model='deepseek-chat',user_prompt=question)
        stream = get_llm_response(client, model=model_name,user_prompt=question,stream=True)
        for chunk in stream:#stream 迭代器
            yield chunk.choices[0].delta.content or ''#  return iter('...')
    except BaseException as e:#Exception是BaseException的子信息
        print(e)#查看错误信息
        yield from '暂时无法提供回复，请检查的你的配置是否正确'
        #return '暂时无法提供回复，请检查的你的配置是否正确'
    #return str(random.randrange(1, 100))#提出问题后，大模型回答1-100的随机数（可通过这个修改回答的问题）

with st.sidebar:#侧边栏
    api_vendor = st.radio(label="请选择服务提供商", options=["OpenAI", "DeepSeek"])
    if api_vendor == "OpenAI":
        base_url = 'https://twapi.openai-hk.com/v1'
        model_options = ['gpt-4o-mini', 'gpt-4.1-mini', 'gpt-4o', 'gpt-4.1']
    elif api_vendor == 'DeepSeek':
        base_url = 'https://api.deepseek.com'
        model_options = ['deepseek-chat', 'deep-reasoner']
    model_name = st.selectbox(label="请选择要使用的模型: ", options=model_options)
    api_key = st.text_input(label='请输入你的Key: ', type='password')
if 'messages' not in st.session_state:
    st.session_state['messages'] = [('ai','你好，我是你的AI助手，我叫小敏。')]#列表二元组来存放会话

st.write('##  田诗敏的聊天机器人')# #与题目之间要有空格

if not api_key:
    st.error('请提供访问大模型需要的APT key!!!')
    st.stop()

for role, content in st.session_state['messages']:
    st.chat_message(role).write(content)
#st.chat_message('ai').write('你好，我是你的AI助手，我叫小美。')

user_input = st.chat_input(placeholder='请输入')
if user_input:
    _,history = st.session_state['messages'][-1]
    st.session_state['messages'].append(('human', user_input))
    st.chat_message('human').write(user_input)
    with st.spinner('AI正在思考，请耐心等待......'):
        #answer = get_answer(user_input)
        answer = get_answer(f'{history},{user_input}')#变量用花括号
        result = st.chat_message('ai').write_stream(answer)
        st.session_state['messages'].append(('ai', result))
        #st.chat_message('ai').write(answer)

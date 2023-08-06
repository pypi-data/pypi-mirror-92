#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re
import json
from colorama import Fore, Back, Style
from fasttest_selenium.common import Var, Dict, log_info
from fasttest_selenium.common.decorator import mach_keywords, executor_keywords
from fasttest_selenium.runner.action_executor import ActionExecutor

class ActionAnalysis(object):

    def __init__(self):
        self.variables = {}
        self.for_variables = {}
        self.action_executor = ActionExecutor()

    def __get_variables(self, name):
        '''
        获取变量
        :param name:
        :return:
        '''
        if not re.match(r'^\${(\w+)}$', name):
            raise NameError("name '{}' is not defined".format(name))
        name = name[2:-1]
        if name in self.for_variables.keys():
            object_var = self.for_variables[name]
        elif name in self.variables:
            object_var = self.variables[name]
        elif name in self.common_var.keys():
            object_var = self.common_var[name]
        elif name in Var.extensions_var['variable'].keys():
            object_var = Var.extensions_var['variable'][name]
        elif name in Var.extensions_var['resource'].keys():
            object_var = Var.extensions_var['resource'][name]
        elif name in vars(Var).keys():
            object_var = vars(Var)[name]
        else:
            raise NameError("name '{}' is not defined".format(name))
        return object_var

    def __replace_string(self, content):
        """
        字符串替换
        :param content:
        :return:
        """
        if isinstance(content, str):
            if re.match(r"^'(.*)'$", content):
                content = '"{}"'.format(content)
            elif  re.match(r'^"(.*)"$', content):
                content = "'{}'".format(content)
            else:
                content = '"{}"'.format(content)
        else:
            content = str(content)
        return content

    def __get_replace_string(self, content):
        '''

        :param content:
        :return:
        '''
        pattern_content = re.compile(r'(\${\w+}+)')
        while True:
            if isinstance(content, str):
                search_contains = re.search(pattern_content, content)
                if search_contains:
                    search_name = self.__get_variables(search_contains.group())
                    if search_name is None:
                        search_name = 'None'
                    elif isinstance(search_name, str):
                        if re.search(r'(\'.*?\')', search_name):
                            search_name = '"{}"'.format(search_name)
                        elif re.search(r'(".*?")', search_name):
                            search_name = '\'{}\''.format(search_name)
                        else:
                            search_name = '"{}"'.format(search_name)
                    else:
                        search_name = str(search_name)
                    content = content[0:search_contains.span()[0]] + search_name + content[search_contains.span()[1]:]
                else:
                    break
            else:
                content = str(content)
                break

        return content

    def __get_params_type(self, param):
        '''
        获取参数类型
        :param param:
        :return:
        '''
        if re.match(r"^'(.*)'$", param):
            param = param.strip("'")
        elif re.match(r'^"(.*)"$', param):
            param = param.strip('"')
        elif re.match(r'(^\${\w+}?$)', param):
            param = self.__get_variables(param)
        elif re.match(r'(^\${\w+}?\[.+\]$)', param):
            index = param.index('}[')
            param_value = self.__get_variables(param[:index+1])
            key = self.__get_params_type(param[index + 2:-1])
            try:
                param = param_value[key]
            except Exception as e:
                raise SyntaxError('{}: {}'.format(param, e))
        else:
            param = self.__get_eval(param.strip())
        return param

    def __get_eval(self, str):
        '''
        :param parms:
        :return:
        '''
        try:
            str = eval(str)
        except:
            str = str

        return str

    def __get_parms(self, parms):
        '''
        获取参数,传参（）形式
        :param parms:
        :return:
        '''
        parms = parms.strip()
        if re.match('^\(.*\)$', parms):
            params = []
            pattern_content = re.compile(r'(".*?")|(\'.*?\')|(\${\w*?}\[.*?\])|(\${\w*?})|,| ')
            find_content = re.split(pattern_content, parms[1:-1])
            find_content = [x.strip() for x in find_content if x]
            for param in find_content:
                var_content = self.__get_params_type(param)
                params.append(var_content)
            return params
        else:
            raise SyntaxError(parms)

    def __analysis_exist_parms_keywords(self, step):
        key = step.split('(', 1)[0].strip()
        parms = self.__get_parms(step.lstrip(key))
        action_data = Dict({
            'key': key,
            'parms': parms,
            'step': step
        })
        return action_data

    def __analysis_not_exist_parms_keywords(self, step):
        key = step
        parms = None
        action_data = Dict({
            'key': key,
            'parms': parms,
            'step': step
        })
        return action_data

    def __analysis_variable_keywords(self, step):
        step_split = step.split('=', 1)
        if len(step_split) != 2:
            raise SyntaxError(f'"{step}"')
        elif not step_split[-1].strip():
            raise SyntaxError(f'"{step}"')
        name =  step_split[0].strip()[2:-1]
        var_value = step_split[-1].strip()

        if re.match(r'\$\.(\w)+\(.*\)', var_value):
            key = var_value.split('(', 1)[0]
            if key == '$.id':
                parms = self.__get_replace_string(var_value.split(key, 1)[-1][1:-1])
            else:
                parms = self.__get_parms(var_value.split(key, 1)[-1])
        elif re.match(r'(\w)+\(.*\)', var_value):
            key = var_value.split('(', 1)[0].strip()
            parms = self.__get_parms(var_value.lstrip(key))
        else:
            key = None
            parms = [self.__get_params_type(var_value)]
        action_data = Dict({
            'key': key,
            'parms': parms,
            'name': name,
            'tag': 'getVar',
            'step': step
        })
        return action_data

    def __analysis_common_keywords(self, step, style):
        key = step.split('call', 1)[-1].strip().split('(', 1)[0].strip()
        parms = step.split('call', 1)[-1].strip().split(key, 1)[-1]
        parms = self.__get_parms(parms)
        action_data = Dict({
            'key': key,
            'parms': parms,
            'tag': 'call',
            'style': style,
            'step': step
        })
        return action_data

    def __analysis_other_keywords(self, step):
        key = step.split(' ', 1)[0].strip()
        parms = self.__get_replace_string(step.lstrip(key).strip())
        action_data = Dict({
            'key': key,
            'parms': parms,
            'tag': 'other',
            'step': f'{key} {parms}'
        })
        return action_data

    def __analysis_for_keywords(self, step):
        f_p =  re.search(r'for\s+(\$\{\w+\})\s+in\s+(\S+)', step)
        f_t = f_p.groups()
        if len(f_t) != 2:
            raise SyntaxError(f'"{step}"')

        # 迭代值
        iterating = f_t[0][2:-1]
        # 迭代对象
        parms =  [self.__get_params_type(f_t[1])]

        action_data = Dict({
            'key': 'for in',
            'parms': parms,
            'var': iterating,
            'tag': 'for',
            'step': f'for {f_t[0]} in {self.__get_params_type(f_t[1])}'
        })
        return action_data

    @mach_keywords
    def __match_keywords(self, step, style):

        if re.match(' ', step):
            raise SyntaxError(f'"{step}"')
        step = step.strip()

        if re.match(r'\w+\((.*)\)', step):
            return self.__analysis_exist_parms_keywords(step)
        elif re.match(r'^\w+$', step):
            return self.__analysis_not_exist_parms_keywords(step)
        elif re.match(r'\$\{\w+\}=|\$\{\w+\} =', step):
            return self.__analysis_variable_keywords(step)
        elif re.match(r'call \w+\(.*\)', step):
            return self.__analysis_common_keywords(step, style)
        elif re.match(r'if |elif |while |assert .+', step):
            return self.__analysis_other_keywords(step)
        elif re.match(r'for\s+(\$\{\w+\})\s+in\s+(\S+)+', step):
            return self.__analysis_for_keywords(step)
        else:
            raise SyntaxError(f'"{step}"')

    @executor_keywords
    def executor_keywords(self, action, style):

        try:
            if action.tag in ['getVar', 'call', 'other', 'for']:
                result = self.action_executor.action_executor(action)
            elif action.key in Var.default_keywords_data:
                result = self.action_executor.action_executor(action)
            elif action.key in Var.new_keywords_data:
                result = self.action_executor.new_action_executor(action)
            else:
                raise KeyError("keyword '{}' is not defined".format(action.key))

            if action.tag == 'getVar':
                # 变量赋值
                self.variables[action.name] = result
            return result
        except Exception as e:
            raise e

    def action_analysis(self, step, style, common, iterating_var):
        '''
        @param step: 执行步骤
        @param style: 缩进
        @param common: call 所需参数
        @param iterating_var: for 迭代值
        @return:
        '''
        log_info(' {}'.format(step), Fore.GREEN)
        if not iterating_var:
            self.for_variables = {}
        else:
            self.for_variables.update(iterating_var)
            log_info(' --> {}'.format(self.for_variables))
        self.common_var = common
        # 匹配关键字、解析参数
        action_dict = self.__match_keywords(step, style)
        log_info(' --> key: {}'.format(action_dict['key']))
        log_info(' --> value: {}'.format(action_dict['parms']))
        # 执行关键字
        result = self.executor_keywords(action_dict, style)
        return result

if __name__ == '__main__':
    action = ActionAnalysis()



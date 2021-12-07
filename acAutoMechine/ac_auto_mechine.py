# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""


class Ac_node(object):
    
    def __init__(self, state_id):
        self.state_id = state_id
        self.is_match = False
        self.node:dict[str,Ac_node] = {}

class Ac_mechine(object):
    
    def __init__(self):
        self.dynamic_state_id = 1
        self.key_words = []
        self.node = Ac_node(0)
        self.state_node = {}
        self.state_output = {}
        self.output_state = {}
        self.failjump_state = {}
        self.final_state_all_output = {}
    
    def add_keys(self, word):
        self.key_words.append(word)
        
    def __construct_tree(self, node, input_tokens, input_index):
        if input_index >= len(input_tokens):
            return 
        input_char = input_tokens[input_index]
        new_input_index = input_index + 1
        next_node = node.node.get(input_char)
        if next_node == None:
            node.node[input_char] = Ac_node(self.dynamic_state_id)
            next_node = node.node[input_char]
            self.dynamic_state_id = self.dynamic_state_id + 1
        if new_input_index == len(input_tokens):
            next_node.is_match = True
        self.state_node[next_node.state_id] = next_node
        self.state_output[next_node.state_id] = input_tokens[:new_input_index]
        self.__construct_tree(next_node, input_tokens, new_input_index)
    
    def __get_failjump(self):
        self.final_state_all_output.clear()
        self.failjump_state.clear()
        for i,j in self.state_output.items():
            if self.state_node[i].is_match:
                self.final_state_all_output.setdefault(i,[]).append(j)

        for output, state_id in self.output_state.items():
            for i in range(len(output)):
                if output[-(i+1):] in self.output_state and i != len(output)-1:
                    jump_state = self.output_state[output[-(i+1):]]
                    self.failjump_state.setdefault(state_id,[]).append(jump_state)
                    if self.state_node[jump_state].is_match == True:
                        self.state_node[state_id].is_match = True
                        self.final_state_all_output.setdefault(state_id,[]).append(self.state_output[jump_state])
                        
    def build_actree(self):
        input_index = 0
        for words in self.key_words:
            self.__construct_tree(self.node, words, input_index)
        self.output_state = { j:i for i,j in self.state_output.items()}
        self.__get_failjump()
        
    def match(self, text, match_trace = False):
        #里面内容为元组，（跳转字符，跳转后状态）
        match_list = [('start',0)]
        match_key_list = []
        current_node = self.node
        for index in range(len(text)):
            char = text[index]
            next_node = current_node.node.get(char)
            if next_node == None:
                jump_list = self.failjump_state.get(current_node.state_id)
                jump_state = 0
                if jump_list:
                    for jump_state_id in jump_list:
                        next_node = self.state_node[jump_state_id].node.get(char)
                        if next_node:
                            match_list.append((None,jump_state_id))
                            current_node = next_node
                            jump_state = 1
                            break
                    if not jump_state:
                        next_node = self.node.node.get(char)
                        if next_node:
                            match_list.append(('start', 0))
                            current_node = next_node
                        else:
                            current_node = self.node
                else:
                    next_node = self.node.node.get(char)
                    if next_node:
                        match_list.append(('start', 0))
                        current_node = next_node
                    else:
                        current_node = self.node
            else:
                current_node = next_node
            match_list.append((char, current_node.state_id))
            if current_node.is_match:
                match_key_list.extend([(index, w) for w in self.final_state_all_output[current_node.state_id]])
        if match_trace:
            return match_list, match_key_list
        else:
            return match_key_list
        
    def match_long(self, text, match_trace = False):
        if match_trace:
            match_list, match_key_list = self.match(text, match_trace)
        else:
            match_key_list = self.match(text, match_trace)
        start_trace_dict = {}
        max_length_dict = {}
        for index, word in match_key_list:
            start_index = index - len(word) + 1
            if start_index in start_trace_dict:
                if start_trace_dict.get(start_index) < len(word):
                    start_trace_dict[start_index] = len(word)
                    max_length_dict[start_index] = (index, word)
            else:
                start_trace_dict[start_index] = len(word)
                max_length_dict[start_index] = (index, word)
            
        sorted_max_length_list = sorted(max_length_dict.items(), key = lambda x:x[0])

        #去掉重合的部分
        result = []
        last_end_index = -1
        for start_index, (end_index, word) in sorted_max_length_list:
            if start_index > last_end_index:
                last_end_index = end_index
                result.append((end_index, word))
        if match_trace:
            return match_list, result
        else:
            return result
        return result

if __name__ == '__main__':       
    
    actree = Ac_mechine()
    actree.add_keys('he')
    actree.add_keys('her')
    actree.add_keys('here')
    actree.build_actree()
    print(actree.match("he here her"))  
    print(actree.match_long("he here her"))  
    print(actree.match("he here her"), True)  
    print(actree.match_long("he here her"), True)  
            
        
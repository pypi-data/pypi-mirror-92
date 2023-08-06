import json

class nested_json_parser:

    def bucket(self,data={},id = 0, parent = 'root',child_of='root',child_of_id=0):
        local_id = id
        if data == {}:
            local_data = self.data
        else:
            local_data = data
        local_dict={}
        local_dict["root_id"] =self.stack[-1][1]
        local_dict["root_name"] =parent
        local_dict["child_of"] = child_of
        local_dict["child_of_id"] = child_of_id
        temp_lst = []
        for key in local_data:
            self.counter += 1
            self.stack.append([key,self.counter])
            if isinstance(local_data[key],(str, int, float)):
                local_dict[key] = local_data[key]
            if isinstance(local_data[key], dict):
                if local_data[key] == {}:
                    local_dict["no item available"] = 'NULL'
                else:
                    self.bucket(local_data[key],local_id+len(self.stack),key,self.stack[-2][0],self.stack[-2][1])
            if isinstance(local_data[key], list):
                for count,lst in enumerate(local_data[key]):
                    self.stack[-1][1] =self.stack[-1][1]+count
                    if isinstance(lst, (str,int, float)):
                        temp ={}
                        temp["root_id"] = local_id+len(self.stack)+count
                        temp["root_name"] = key
                        temp["child_of"] = self.stack[-2][0]
                        temp["child_of_id"] = self.stack[-2][1]
                        temp[key] = lst
                        temp_lst.append(temp)
                        self.output.append(temp)
                    if isinstance(lst, dict):
                        local_id = self.stack[-2][1]
                        self.bucket(lst,local_id+len(self.stack)+count,key,self.stack[-2][0],local_id)
            self.stack.pop()
        self.output.append(local_dict)
        return(self.output)

    def __init__(self,data):
        self.data = data
        self.counter = 0
        self.stack=[['root',0]]
        self.output =[]


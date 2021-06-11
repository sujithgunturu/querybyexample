# Enter your code here. Read input from STDIN. Print output to STDOU


def decode_json(input_, categories, contents):
    i = 0
    key, value, temp = "", "", ""
    ifkey = False
    end_quote = ""
    while i < len(input_):
        if input_[i] == "{":
            ifkey = True
        elif input_[i] == ",":
            if value:
                categories.append(key)
                contents.append(value)
            value = ""
            ifkey = True
        elif input_[i] == "}":
            if value:
                categories.append(key)
                contents.append(value)
            value = ""
            ifkey = True
        elif input_[i] == '\"':
            end_quote = input_.find('\"', i+1)
            temp = input_[i+1:end_quote] 
            
            if ifkey:
                key = temp
            else:
                value = '\"' + temp + '\"'
            i = end_quote
        elif input_[i] == ':':
            ifkey = False
        elif input_[i] == " ":
            return categories, contents
        else:
            if not ifkey:
                value = value + input_[i]
            
        i = i + 1
    return categories, contents   
       
            
                 
                

            
def add_json(input_, entryid, iflist):
    '''
    check global local:
    '''
    global search
    global storage
    storage.append(input_.strip('\n'))
    
    if not iflist:
        categories = []
        contents = []
        categories, contents =  decode_json(input_, categories, contents)
        if lookup == {}:
            search = []
            for j in range(len(categories)):
                lookup[categories[j]]  = j
        
        for j in range(len(categories)):
            if len(search) != len(categories):
                search.append({})
            try:
                search[lookup[categories[j]]][contents[j]].append(entryid)
            except:
                search[lookup[categories[j]]][contents[j]] = [entryid]

    else:
        i  = input_.find('[') + 1
        if search == []:
            search = [{}] #doubt
        value = ""
        while input_[i] != "]":
            if input_[i] == ",":
                try:
                    search[0][value].append(entryid)
                    value = ""
                except:
                    search[0][value] = [entryid]
                    value = ""
            else:
                value = value + input_[i]
            i = i + 1
        try:
            search[0][value].append(entryid)
        except:
            search[0][value] = [entryid]
        
                   
def get_json(input_, iflist, storage):
    global search
    global lookup
    if not iflist:
        if not lookup:
            return
        categories, contents = decode_json(input_, categories=[], contents=[])
        partial_results = [[] for _ in categories]
        
        for j in range(len(categories)):
            lookup_number = lookup[categories[j]]
            
            if search[lookup_number][contents[j]]:
                for t in search[lookup[categories[j]]][contents[j]]:
                    partial_results[j].append(t)
            else:
                return
        
        if partial_results:
            full_results = get_intersection(partial_results)
            for c in full_results:
                if storage[c]:
                    print(storage[c])
        else:
            for c in storage:
                if c != "null":
                    print(c)
            
    else:
        i = input_.find('[') + 1
        partial_results = []
        value = ""
        while input_[i] != "]":
            if input_[i] == ",":
                ###change
                if search[0][value]:
                    partial_results.append(search[0][value])
                else:
                    return 
                value = ""
            else:
                value = value + input_[i]
            i = i + 1 
        if search[0][value]:
            partial_results.append(search[0][value])
        else:
            return
        if partial_results:
            full_results = get_intersection(partial_results)
            for c in full_results:
                if storage[c] != "null":
                    print(storage[c])
        else:
            for c in storage:
                if c!="null":
                    print(c)

        
                       
                    
                
                            
                
def delete_json(input_, iflist, storage):
    global lookup
    global search
    if not iflist:
        if not lookup:
            return
        categories = []
        contents = []
        
        categories, contents = decode_json(input_, categories=[], contents=[])
        partial_results = [[] for _ in categories]
        
        for j in range(len(categories)):
            lookup_number = lookup[categories[j]]
            if search[lookup_number][contents[j]]:
                for t in search[lookup[categories[j]]][contents[j]]:
                    partial_results[j].append(t)
            else:
                return
        if partial_results:
            full_results = get_intersection(partial_results)
            for c in full_results:
                storage[c] = "null"
        else:
            for c in storage:
                c = "null"
    else:
        i = input_.find("[") + 1
        partial_results = []
        value = ""
        while input_[i] != "]":
            if input_[i] == ",":
                if search[0][value]:
                    partial_results.append(search[0][value])
                else:
                    return
                value = ""
            else:
                value = value + input_[i]
            i = i + 1
        if search[0][value]:
            partial_results.append(search[0][value])
        else:
            return
        if partial_results:
            full_results = get_intersection(partial_results)
        else:
            for c in storage:
                c = "null"
                        
    



def get_intersection(sets):
    result = []
    minsize = len(sets[0])
    smallest = 0
    if len(sets) == 1:
        return sets[0]
    else:
        for i in range(1, len(sets)):
            if minsize > len(sets[i]):
                minsize = len(sets[i])
                smallest = i
        temp = list(set(sets[smallest]))
        sets[smallest] = temp
        elements = []
        for c in sets[smallest]:
            elements.append(c)
        for it in elements:
            iffound = True
            for j in range(len(sets)):
                if j!=smallest:
                    if it not in sets[j]:
                        iffound = False
                        break
            if iffound:
                result.append(it)
    return result

    
iflist = False
entryid = 0
storage = []
lookup = {}
search = []
import sys
for line in sys.stdin:
    iflist = False
    inputer = line.find("{")
    line2 = line[inputer:]
    if (line.find("list") >= 0):
        iflist = True
    if line[0] == "a":
        add_json(line2, entryid, iflist)
        entryid += 1
    elif line[0] == "g":
        get_json(line2, iflist, storage)
    elif line[0] == "d":
        delete_json(line2, iflist, storage)
    else:
        print("error in input")
        
            
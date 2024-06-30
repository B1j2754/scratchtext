import json
import os
import tempfile
import shutil
import zipfile
import copy

from lark import Lark, Tree

class ScratchProject():

    def __init__(self, filename):
        self.CUR_ID = 0
        self.variables = dict()
        tmpdir = tempfile.mkdtemp()
        with zipfile.ZipFile(filename, "r") as zip_ref:
            zip_ref.extractall(tmpdir)
        with open(os.path.join(tmpdir, "project.json")) as f:
            self.data = json.loads(f.read())
        self.origin = filename
        shutil.rmtree(tmpdir)

    def generate_id(self, arg=None):
        self.CUR_ID += 1
        if arg:
            return f"scratchtext-{arg}-{self.CUR_ID}"
        else:
            return f"scratchtext-{self.CUR_ID}"

    def variable(self, name):
        name = name
        if name not in self.variables:
            self.variables[name] = self.generate_id(arg="var")
        return self.variables[name]
    
    def normalize(self, input, block_id):
        if isinstance(input, dict):
            return [3,self.add_block(self.current_target, input, block_id),[5,"❤️"]]
        if not input.startswith("$"):
            if not input.replace('.','').isnumeric():
                return [1, [6,input[1:-1]]]
            else:
                return [1, [6,input]]
        else:
            input = input[1:]
            variable_id = self.variable(input)
            return [3, [12, input, variable_id], [6,"❤️"]]

    def generate_block(self, statement, block_id):
        print(f'generating block {statement}')
        opcode = statement["opcode"]

        # body, children, opcode
        for key, value in copy.deepcopy(statement).items():
            if key in ["x","y","text_value","secs","num1","num2","value","steps","degrees","duration","message","times","string1","string2"]:
                statement[key + "og"] = statement[key]
                statement[key] = self.normalize(statement[key], block_id)

        block = {
            "opcode": opcode,
            "parent": None,
            "next": None,
            "inputs": {},
            "fields": {},
            "shadow": False,
            "topLevel": False,
            "x": 0,
            "y": 0
        }

        input_keys = {
            "event_whenflagclicked": [],
            "event_whenthisspriteclicked": [],
            "motion_ifonedgebounce": [],
            "motion_movesteps": ["steps"],
            "motion_turnright": ["degrees"],
            "motion_gotoxy": ["x", "y"],
            "motion_glidesecstoxy": ["secs", "x", "y"],
            "motion_setx": ["x"],
            "motion_sety": ["y"],
            "looks_think": ["message"],
            "looks_say": ["message"],
            "control_repeat": ["times"],
            "control_wait": ["duration"],
            "data_setvariableto": ["value"],
            "operator_join": ["string1", "string2"],
            "operator_add": ["num1", "num2"],
            "looks_show": [],
            "looks_hide": [],
            "operator_add": ["num1","num2"],
            "operator_subtract": ["num1","num2"],
            "operator_divide": ["num1","num2"],
            "operator_mod": ["num1","num2"],
            "operator_multiply": ["num1","num2"],
            "operator_join": ["string1","string2"]
        }

        if opcode in input_keys:
            for key in input_keys[opcode]:
                # print('!!!!', key.upper(), list(statement[key]))
                block["inputs"] = {key.upper(): list(statement[key])}
        
        ## Events
        if opcode == "event_whenflagclicked":
            pass

        elif opcode == "event_whenthisspriteclicked":
            pass

        elif opcode == "event_whenkeypressed":
            block["fields"] = statement["data"]["fields"]

        ## Motion
        elif opcode == "motion_ifonedgebounce":
            pass

        elif opcode == "motion_movesteps":
            block["inputs"] = {
                "STEPS": list(statement["steps"])
            }

        elif opcode == "motion_gotoxy":
            block["inputs"] = {
                "X": list(statement["x"]),
                "Y": list(statement["y"])
            }
            print(list(statement["x"]))

        elif opcode == "motion_turnright":
            block["inputs"] = {
                "DEGREES": list(statement["degrees"])
            }

        elif opcode == "motion_glidesecstoxy":
            block["inputs"] = {
                "SECS": list(statement["secs"]),
                "X": list(statement["x"]),
                "Y": list(statement["y"])
            }
        elif opcode == "motion_setx":
            block["inputs"] = {
                "X": list(statement["x"])
            }
        elif opcode == "motion_sety":
            block["inputs"] = {
                "Y": list(statement["y"])
            }

        ## Looks
        elif opcode == "looks_think":
            block["inputs"] = {
                "MESSAGE": list(statement["message"])
            }
        elif opcode == "looks_say":
            block["inputs"] = {
                "MESSAGE": list(statement["message"])
            }
        elif opcode == "looks_show":
            pass
        elif opcode == "looks_hide":
            pass

        # Control
        elif opcode == "control_repeat":
            block["inputs"] = {
                "TIMES": list(statement["times"])
            }
        
        elif opcode == "control_wait":
            block["inputs"] = {
                "DURATION": list(statement["duration"])
            }

        # Variables
        elif opcode == "data_setvariableto":
            variable = statement["variable"][1:]
            value = statement["value"]
            variable_id = self.variable(variable)
            block["inputs"] = {
                "VALUE": list(statement["value"])
            }
            block["fields"] = {
                "VARIABLE": [variable, variable_id]
            }

        # Operators
        elif opcode == "operator_join":
            block["inputs"] = {
                "STRING1" : list(statement["string1"]),
                "STRING2" : list(statement["string2"])
            }

        elif opcode == "operator_add":
            block["inputs"] = {
                "NUM1": list(statement["num1"]),
                "NUM2": list(statement["num2"])
            }
        
        elif opcode == "operator_subtract":
            block["inputs"] = {
                "NUM1": list(statement["num1"]),
                "NUM2": list(statement["num2"])
            }
        
        elif opcode == "operator_multiply":
            block["inputs"] = {
                "NUM1": list(statement["num1"]),
                "NUM2": list(statement["num2"])
            }
        
        elif opcode == "operator_divide":
            block["inputs"] = {
                "NUM1": list(statement["num1"]),
                "NUM2": list(statement["num2"])
            }

        elif opcode == "operator_mod":
            block["inputs"] = {
                "NUM1": list(statement["num1"]),
                "NUM2": list(statement["num2"])
            }

        # Pen Blocks
        elif opcode == "pen_penUp":
            pass
        
        elif opcode == "pen_penDown":
            pass
        
        elif opcode == "pen_clear":
            pass
        
        return block

    def add_program(self, program):
        for sprite in program:
            for target in self.data["targets"]:
                if target["name"] == sprite:
                    self.add_sprite_scripts(target, program[sprite])
        
        # Add variables
        for target in self.data["targets"]:
            if target["isStage"]:
                if "variables" not in target:
                    target["variables"] = dict()
                for variable in self.variables:
                    variable_id = self.variables[variable]
                    target["variables"][variable_id] = [variable, "0"]

    def add_sprite_scripts(self, target, program):
        script_count = 0
        print("adding program", program)
        self.variables = dict()
        self.current_target = target  # Set the current target
        for script in program:
            self.add_block(target, script, prev=None, script_offset=script_count)
            script_count += 1

    def add_block(self, target, block, prev=None, script_offset=0, first_child=False):
        print("Adding block:", block)
        block_id = self.generate_id()
        scratch_block = self.generate_block(block,block_id)
        print(f"Generated block: {block_id} -> {scratch_block}")

        if prev is None:
            scratch_block["topLevel"] = True
            scratch_block["x"] = 50 + (script_offset * 300)
            scratch_block["y"] = 50
        else:
            prev_block = target["blocks"].get(prev)
            if prev_block:
                if not first_child:
                    prev_block["next"] = block_id
                else:
                    if "inputs" not in prev_block:
                        prev_block["inputs"] = dict()
                    prev_block["inputs"]["SUBSTACK"] = [2, block_id]
                scratch_block["parent"] = prev

        target["blocks"][block_id] = scratch_block
        print(f"Block {block_id} added to target {target['name']} with parent {prev}")

        cprev = block_id  # previous id as we iterate through body of a function
        for child in block.get("body", []):
            cprev = self.add_block(target, child, prev=cprev, script_offset=script_offset)

        first = True
        for child in block.get("children", []):
            cprev = self.add_block(target, child, prev=cprev, script_offset=script_offset, first_child=first)
            first = False

        return block_id


    def write(self, filename):

        # Load old contents
        tmpdir = tempfile.mkdtemp()
        with zipfile.ZipFile(self.origin, "r") as zip_ref:
            zip_ref.extractall(tmpdir)

        # Replace project.json
        with open(os.path.join(tmpdir, "project.json"), "w") as f:
            f.write(json.dumps(self.data))

        zip_ref = zipfile.ZipFile(filename, "w")
        for content_file in os.listdir(tmpdir):
            zip_ref.write(os.path.join(tmpdir, content_file), arcname=content_file)
        zip_ref.close()
        shutil.rmtree(tmpdir)


with open("scratch.lark") as f:
    ScratchParser = Lark(f.read())

def parse(text):
    return parse_tree(ScratchParser.parse(text))

def parse_tree(t):
    if t.data == "start":
        return list(map(parse_tree, t.children))

    if t.data == "expression":
        if len(t.children) == 1:
            return t.children[0].value
    
    operator_map = {
                "add": "operator_add",
                "sub": "operator_subtract",
                "mul": "operator_multiply",
                "div": "operator_divide",
                "mod": "operator_mod"
            }
    
    if t.data in operator_map:
        # Keep winding down the tree to evaluate the expressions
        while isinstance(t.children[0], Tree):
            t.children[0] = parse_tree(t.children[0])
        while isinstance(t.children[1], Tree):
            t.children[1] = parse_tree(t.children[1])

        return {
            "opcode": operator_map[t.data],
            "num1": t.children[0],
            "num2": t.children[1]
        }

    if t.data == "function_definition":
        func = str(t.children[0])
        opcode = "none"
        data = dict()
        skip_children = 1
        if func == "when_flag_clicked":
            opcode = "event_whenflagclicked"
        elif func == "when_clicked":
            opcode = "event_whenthisspriteclicked"
        elif func == "on_key_press":
            opcode = "event_whenkeypressed"
            data = {
                "fields": {"KEY_OPTION": [str(parse_tree(t.children[1])), None]}
            }
            skip_children += 1
        operations = [parse_tree(c) for c in t.children[skip_children:]]
        return {
            "opcode": opcode,
            "body": operations,
            "data": data
        }

    if t.data == "instruction":

        if isinstance(t.children[0], Tree):
            root = t.children[0]
            data = root.data
            if data == "assignment":
                variable = str(root.children[0])
                value = parse_tree(root.children[1])
                return {
                        "opcode": "data_setvariableto",
                        "variable": variable,
                        "value": value
                }

            return None

        instr_type = t.children[0].type
        func = str(t.children[0])

        # Control
        if func == "forever":
            return {
                "opcode": "control_forever",
                "children": [parse_tree(child) for child in t.children[1:]]
            }
        elif func == "repeat":
            return {
                "opcode": "control_repeat",
                "times": parse_tree(t.children[1]),
                "children": [parse_tree(child) for child in t.children[2:]]
            }
        elif func == "wait":
            return {
                "opcode": "control_wait",
                "duration": parse_tree(t.children[1])
            }

        # Motion
        elif func == "edge_bounce":
            return {
                "opcode": "motion_ifonedgebounce"
            }
        elif func == "move":
            return {
                "opcode": "motion_movesteps",
                "steps": parse_tree(t.children[1])
            }
        elif func == "turn":
            return {
                "opcode": "motion_turnright",
                "degrees": parse_tree(t.children[1])
            }
        elif func == "goto" and instr_type == "BINFUNC":
            return {
                "opcode": "motion_gotoxy",
                "x": str(parse_tree(t.children[1])),
                "y": str(parse_tree(t.children[2]))
            }
        elif func == "glide" and instr_type == "TRIFUNC":
            return {
                "opcode": "motion_glidesecstoxy",
                "secs": str(parse_tree(t.children[1])),
                "x": str(parse_tree(t.children[2])),
                "y": str(parse_tree(t.children[3]))
            }
        elif func == "setx":
            return {
                "opcode": "motion_setx",
                "x": str(parse_tree(t.children[1]))
            }
        elif func == "sety":
            return {
                "opcode": "motion_sety",
                "y": str(parse_tree(t.children[1]))
            }

        # Looks
        elif func == "think":
            return {
                "opcode": "looks_think",
                "message": parse_tree(t.children[1])
            }
        elif func == "say":
            return {
                "opcode": "looks_say",
                "message": parse_tree(t.children[1])
            }
        elif func == "show":
            return {
                "opcode": "looks_show"
            }
        elif func == "hide":
            return {
                "opcode": "looks_hide"
            }

        elif func == "join":
            return {
                "opcode": "operator_join",
                "string1": str(parse_tree(t.children[1])),
                "string2": str(parse_tree(t.children[2]))
            }

        elif func == "penUp":
            return {
                "opcode": "pen_penUp"
            }

        elif func == "penDown":
            return {
                "opcode": "pen_penDown"
            }

        elif func == "penClear":
            return {
                "opcode": "pen_clear"
            }
        
    return t
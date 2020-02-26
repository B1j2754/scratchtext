import json
import os
import tempfile
import shutil
import zipfile

class ScratchProject():

    CUR_ID = 0

    def __init__(self, filename):
        tmpdir = tempfile.mkdtemp()
        with zipfile.ZipFile(filename, "r") as zip_ref:
            zip_ref.extractall(tmpdir)
        with open(os.path.join(tmpdir, "project.json")) as f:
            self.data = json.loads(f.read())
        self.origin = filename
        shutil.rmtree(tmpdir)

    @classmethod
    def generate_id(cls):
        ScratchProject.CUR_ID += 1
        return f"scratchtext-{ScratchProject.CUR_ID}"

    @classmethod
    def generate_block(cls, statement):
        opcode = statement["opcode"]

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

        # Events
        if opcode == "event_whenflagclicked":
            pass

        # Motion
        elif opcode == "motion_movesteps":
            block["inputs"] = {
                "STEPS": [
                    1,
                    [4, str(statement["text_value"])]
                ]
            }

        return block

    def add_program(self, program):
        for sprite in program:
            for target in self.data["targets"]:
                if target["name"] == sprite:
                    self.add_sprite_script(target, program[sprite])

    def add_sprite_script(self, target, program):
        script_count = 0
        for script in program:

            # Track previous block
            prev_block_id = None

            # Create blocks
            for statement in script:
                block_id = ScratchProject.generate_id()
                block = ScratchProject.generate_block(statement)


                if prev_block_id is None:
                    block["topLevel"] = True
                    block["x"] = 180
                    block["y"] = 180 + (script_count * 30)
                else:
                    target["blocks"][prev_block_id]["next"] = block_id
                    block["parent"] = prev_block_id

                target["blocks"][block_id] = block
                prev_block_id = block_id

            script_count += 1

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



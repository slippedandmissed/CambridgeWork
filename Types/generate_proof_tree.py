#!/usr/bin/python3.9

from PIL import Image, ImageDraw
from pptree import print_tree
from io import StringIO
import subprocess
import pdf2image
import argparse
import tempfile
import sys
import os
import re

real_stdout = sys.stdout

class Tree:
  def __init__(self, blueprint, rule_name_blueprint=None):
    self.blueprint = blueprint
    self.rule_name_blueprint=rule_name_blueprint
    self.prerequisites = []
  
  def __str__(self):
    sys.stdout = my_stdout = StringIO()
    print_tree(self, childattr="prerequisites", nameattr="blueprint", horizontal=False)
    s = my_stdout.getvalue()
    sys.stdout = real_stdout
    return s
  
  def render(
    self,
    line_padding_vertical,
    line_padding_horizontal,
    prerequisite_padding_horizontal,
    line_thickness,
    rule_name_padding_horizontal
  ):
    my_img = render_markdown(self.blueprint)
    prereq_imgs = list(prereq.render(
      line_padding_vertical=line_padding_vertical,
      line_padding_horizontal=line_padding_horizontal,
      prerequisite_padding_horizontal=prerequisite_padding_horizontal,
      line_thickness=line_thickness,
      rule_name_padding_horizontal=rule_name_padding_horizontal
    ) for prereq in self.prerequisites)
    rule_name_img = None if self.rule_name_blueprint is None else render_markdown(self.rule_name_blueprint)

    all_prereqs_width = sum(map(lambda x: x.width, prereq_imgs)) + (len(prereq_imgs)-1)*prerequisite_padding_horizontal

    img_width = line_padding_horizontal + max(
      my_img.width,
      all_prereqs_width
    )
    if rule_name_img is not None:
      img_width += rule_name_padding_horizontal + rule_name_img.width

    img_height = (max(map(lambda x: x.height, prereq_imgs)) if len(prereq_imgs) > 0 else 0) + my_img.height + line_thickness + line_padding_vertical
    line_end_x = img_width
    line_y = img_height-my_img.height-(line_thickness+line_padding_vertical)//2
    if rule_name_img is not None:
      img_height = max(
        img_height,
        (img_height - line_y) + rule_name_img.height//2
      )
      line_y = img_height-my_img.height-(line_thickness+line_padding_vertical)//2

    img = Image.new("RGB", (img_width, img_height), color=(255, 255, 255))



    if rule_name_img is not None:
      line_end_x -= rule_name_padding_horizontal + rule_name_img.width
      img.paste(rule_name_img, ((line_end_x + rule_name_padding_horizontal), line_y - rule_name_img.height//2))
    
    img.paste(my_img, ((line_end_x-my_img.width)//2, img_height-my_img.height))
    img_draw = ImageDraw.Draw(img)
    img_draw.line(
      [
        (0, line_y),
        (line_end_x, line_y)
      ],
      fill="black",
      width=line_thickness
    )

    current_x = (line_end_x - all_prereqs_width)/2
    for prereq_img in prereq_imgs:
      img.paste(prereq_img, (int(current_x), img.height-my_img.height-line_padding_vertical-line_thickness-prereq_img.height))
      current_x += prereq_img.width + prerequisite_padding_horizontal

    return img

def get_indent(line):
  return len(line)-len(line.lstrip())

def parse_line(lines, idx=0):
    root = lines[idx]
    indent = get_indent(root)
    rule_name = None
    if root.lstrip().startswith("#"):
      result = re.search(r"(\s)*#([^#]*)#\s*(.*)", root)
      root = result.group(1)
      if root is None:
        root = ""
      root += result.group(3)
      rule_name = result.group(2).strip()
    tree = Tree(root.lstrip(), rule_name_blueprint=rule_name)
    idx += 1
    while idx < len(lines) and get_indent(lines[idx]) > indent:
      child, idx = parse_line(lines, idx=idx)
      tree.prerequisites.append(child)
    return tree, idx
  
def render_markdown(text):
  with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as md_fp:
    md_fp.write(text)

  with tempfile.NamedTemporaryFile("w", suffix=".pdf", delete=False) as pdf_fp:
    pass

  subprocess.call(["pandoc", md_fp.name, "-o", pdf_fp.name, "-V", "documentclass=standalone"])

  img = pdf2image.convert_from_path(pdf_fp.name)

  os.unlink(md_fp.name)
  os.unlink(pdf_fp.name)

  return img[0]

if __name__ == "__main__":

  parser = argparse.ArgumentParser()
  parser.add_argument("file", type=str, help="The file to render")
  parser.add_argument("--output", "-o", type=str, help="The file to output")
  parser.add_argument("--line_padding_vertical", type=int, default=20)
  parser.add_argument("--line_padding_horizontal", type=int, default=20)
  parser.add_argument("--prerequisite_padding_horizontal", type=int, default=20)
  parser.add_argument("--line_thickness", type=int, default=2)
  parser.add_argument("--rule_name_padding_horizontal", type=int, default=10)
  parser.add_argument("--margin-vertical", type=int, default=30)
  parser.add_argument("--margin-horizontal", type=int, default=30)
  args = parser.parse_args()

  path = args.file
  output_path = args.output
  if output_path is None:
    parts = path.split(".")
    if len(parts) > 1:
      del parts[-1]
    parts.append("png")
    output_path = ".".join(parts)

  with open(path) as fp:
    lines = [line.rstrip() for line in fp.read().split("\n") if line.rstrip() != ""]
    tree = parse_line(lines)[0]

  tree_im = tree.render(
      line_padding_vertical=args.line_padding_vertical,
      line_padding_horizontal=args.line_padding_horizontal,
      prerequisite_padding_horizontal=args.prerequisite_padding_horizontal,
      line_thickness=args.line_thickness,
      rule_name_padding_horizontal=args.rule_name_padding_horizontal
  )
  im = Image.new("RGB", (tree_im.width+args.margin_horizontal, tree_im.height+args.margin_vertical), (255, 255, 255))
  im.paste(tree_im, (args.margin_horizontal//2, args.margin_vertical//2))
  im.save(output_path)



import bpy
import os
import requests
from icrawler.builtin import GoogleImageCrawler
from PIL import Image

# Step 1: Fetch Image using icrawler
search_term = "rosewood jeddah booking.com"
output_dir = "/path/to/your/downloaded_images"
output_image_path = os.path.join(output_dir, "fetched_image.jpg")

# Create output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Perform the image search and download
crawler = GoogleImageCrawler(storage={"root_dir": output_dir})
crawler.crawl(keyword=search_term, max_num=1)

# The first downloaded image should be the one we want
fetched_image_path = os.path.join(output_dir, "rosewood_jeddah_0.jpg")

# Step 2: Apply Vignette and Text Effects using Blender

# Set up Blender scene
input_image_path = fetched_image_path
output_image_path = "/path/to/your/output_image_with_effects.png"

# Clear existing data in Blender
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Set up the scene
scene = bpy.context.scene
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080

# Load the image into Blender
bpy.ops.image.open(filepath=input_image_path)
img = bpy.data.images.load(input_image_path)

# Set up the background image
bg = bpy.data.objects.new("BackgroundImage", bpy.data.meshes.new("mesh"))
scene.collection.objects.link(bg)
bg.scale = (1.0, 1.0, 1.0)

# Apply Darkening Effect (Night Effect)
bpy.context.scene.use_nodes = True
tree = bpy.context.scene.node_tree
nodes = tree.nodes

# Clear default nodes
for node in nodes:
    nodes.remove(node)

# Create a Render Layers node (this will get the image as input)
render_layer_node = nodes.new(type="CompositorNodeRLayers")

# Create a color balance node for darkening effect
darken_node = nodes.new(type="CompositorNodeColorBalance")
darken_node.inputs[1].default_value = (0.4, 0.4, 0.4, 1)  # Darken by reducing brightness

# Connect the render layer node to the darken node
tree.links.new(render_layer_node.outputs[0], darken_node.inputs[0])

# Apply Vignette Effect
# Vignette can be created using a gradient shader
vignette_node = nodes.new(type="CompositorNodeVignette")
vignette_node.inputs[0].default_value = 0.6  # Vignette strength

# Link the darken node to the vignette effect
tree.links.new(darken_node.outputs[0], vignette_node.inputs[0])

# Add text overlay with silver color
# Create a text object for overlaying
bpy.ops.object.text_add(location=(0, 0, 0))
text_object = bpy.context.object
text_object.data.body = "Best Hotels\nIn\nJeddah"
text_object.data.font = bpy.data.fonts.load("/path/to/your/silver_font.ttf")  # Choose a font
text_object.scale = (0.8, 0.8, 0.8)
text_object.data.materials.append(bpy.data.materials.new(name="SilverMaterial"))
text_object.data.materials[0].diffuse_color = (0.8, 0.8, 0.8, 1)  # Silver color

# Position the text in the center
text_object.location = (0, 0, 0.5)

# Create the final output node
output_node = nodes.new(type="CompositorNodeOutputFile")
output_node.base_path = "/path/to/output/"
output_node.file_slots[0].path = "thumbnail_with_dark_vignette_text.png"

# Link the vignette output to the output node
tree.links.new(vignette_node.outputs[0], output_node.inputs[0])

# Render the scene to the output image
bpy.ops.render.render(write_still=True)

print(f"Thumbnail with darkening, vignette effect, and silver text created: {output_image_path}")

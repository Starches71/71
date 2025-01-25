import bpy
import os

# Define the directory to save output image
output_dir = './output'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Ensure the downloaded image exists and is correct
image_path = './rosewood_jeddah_image.jpg'  # Path to the downloaded image from iCrawler
if not os.path.exists(image_path):
    raise FileNotFoundError(f"Image not found at: {image_path}")

output_image_path = os.path.join(output_dir, 'output_image_with_effects.png')
print(f"Saving image to: {output_image_path}")

# Clear existing data (if any)
bpy.ops.wm.read_factory_settings(use_empty=True)

# Load the image
image = bpy.data.images.load(image_path)

# Create a new scene and camera
scene = bpy.context.scene
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080

# Add the image as a plane in the scene
bpy.ops.object.select_all(action='DESELECT')
bpy.ops.object.select_by_type(type='MESH')
bpy.ops.object.delete(use_global=False)  # Remove default cube

bpy.ops.mesh.primitive_plane_add(size=10)
plane = bpy.context.object
plane.data.materials.append(bpy.data.materials.new(name="ImageMaterial"))
plane.active_material.use_nodes = True

# Apply image texture to the plane
plane.active_material.node_tree.nodes["Principled BSDF"].inputs['Base Color'].default_value = (1, 1, 1, 1)
texture_node = plane.active_material.node_tree.nodes.new('ShaderNodeTexImage')
texture_node.image = image
plane.active_material.node_tree.links.new(texture_node.outputs[0], plane.active_material.node_tree.nodes["Principled BSDF"].inputs['Base Color'])

# Apply vignette effect (a simple one using a mix shader and darkening effect)
vignette_shader = bpy.data.materials.new(name="VignetteShader")
vignette_shader.use_nodes = True
nodes = vignette_shader.node_tree.nodes

# Add a darkening effect to the scene (like a night effect)
night_shader = nodes.new(type="ShaderNodeMixRGB")
night_shader.blend_type = 'MULTIPLY'
night_shader.inputs[2].default_value = (0.1, 0.1, 0.1, 1)  # Darken effect
plane.active_material.node_tree.links.new(night_shader.outputs[0], plane.active_material.node_tree.nodes["Principled BSDF"].inputs['Base Color'])

# Create text and overlay it on the image
bpy.ops.object.text_add(location=(0, 0, 1))
text_obj = bpy.context.object
text_obj.data.body = "Best Hotels\nIn\nJeddah"
text_obj.data.size = 1.5
text_obj.data.align_x = 'CENTER'
text_obj.data.align_y = 'CENTER'

# Set font (make sure the path to your font file is correct)
font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"  # Update this to your font path
text_obj.data.font = bpy.data.fonts.load(font_path)

# Set text color to silver (RGB for silver)
text_obj.data.materials.append(bpy.data.materials.new(name="SilverTextMaterial"))
text_obj.active_material.use_nodes = True
text_obj.active_material.node_tree.nodes["Principled BSDF"].inputs['Base Color'].default_value = (0.75, 0.75, 0.75, 1)  # Silver color

# Render the final image
scene.render.filepath = output_image_path
bpy.ops.render.render(write_still=True)

print(f"Image with effects saved at: {output_image_path}")

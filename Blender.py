import os
from icrawler.builtin import GoogleImageCrawler
import bpy

# Step 1: Download the image using icrawler
def download_image(search_term, output_dir="downloaded_images"):
    os.makedirs(output_dir, exist_ok=True)
    crawler = GoogleImageCrawler(storage={"root_dir": output_dir})
    crawler.crawl(keyword=search_term, max_num=1)
    print("Image downloaded as:", os.path.join(output_dir, "000001.jpg"))
    return os.path.join(output_dir, "000001.jpg")

# Step 2: Apply text using Blender (no animation, simple overlay)
def generate_thumbnail(input_image, output_image, text="BEST HOTELS\n       IN\n     JEDDAH"):
    # Clear previous scenes
    bpy.ops.wm.read_factory_settings(use_empty=True)

    # Load the image into Blender
    bpy.ops.image.open(filepath=input_image)

    # Create a new plane to display the image
    bpy.ops.mesh.primitive_plane_add(size=10, enter_editmode=False, align='WORLD', location=(0, 0, 0))
    plane = bpy.context.active_object
    plane.data.uv_textures.new()

    # Apply the image texture to the plane
    material = bpy.data.materials.new("Material")
    material.use_nodes = True
    bsdf = material.node_tree.nodes["Principled BSDF"]
    texture_image = bpy.data.images.load(input_image)
    texture_node = material.node_tree.nodes.new("ShaderNodeTexImage")
    texture_node.image = texture_image
    material.node_tree.links.new(bsdf.inputs['Base Color'], texture_node.outputs['Color'])
    plane.data.materials.append(material)

    # Add text to the scene
    bpy.ops.object.text_add(location=(0, 0, 1))
    text_obj = bpy.context.object
    text_obj.data.body = text
    text_obj.data.size = 2
    text_obj.data.align_x = 'CENTER'
    text_obj.data.align_y = 'CENTER'

    # Adjust the font size and positioning
    text_obj.location = (0, 0, 1.5)

    # Set up the camera
    bpy.ops.object.camera_add(location=(0, -15, 5))
    camera = bpy.context.object
    camera.rotation_euler = (1.2, 0, 0)
    bpy.context.scene.camera = camera

    # Set up rendering (output format and resolution)
    bpy.context.scene.render.resolution_x = 1920
    bpy.context.scene.render.resolution_y = 1080
    bpy.context.scene.render.image_settings.file_format = 'PNG'

    # Render the image
    bpy.context.scene.render.filepath = output_image
    bpy.ops.render.render(write_still=True)

    print("Thumbnail generated successfully:", output_image)

if __name__ == "__main__":
    # Step 1: Download an image
    search_query = "Rosewood Jeddah hotel booking.com"
    input_image = download_image(search_query)

    # Step 2: Generate the thumbnail with text overlay in Blender
    output_image = "thumbnail_with_text.png"
    generate_thumbnail(input_image, output_image)

import trimesh
import numpy as np
import pyrender
import math
from PIL import Image
import io
import argparse

parser = argparse.ArgumentParser(description='Create a rotating GIF from a GLB file')
parser.add_argument('glb_file', type=str, help='The path to the GLB file')
parser.add_argument('output_file', type=str, help='The path to the output GIF file')
parser.add_argument('--num_frames', type=int, default=60, help='The number of frames in the GIF')
parser.add_argument('--resolution', type=int, nargs=2, default=[800, 600], help='The resolution of the GIF')
args = parser.parse_args()

def create_rotating_gif(glb_file, output_file, num_frames=60, resolution=(800, 600)):
    # Load the GLB file
    scene = trimesh.load(glb_file)
    
    # Calculate bounds manually
    if isinstance(scene, trimesh.Scene):
        bounds = np.array([mesh.bounds for mesh in scene.geometry.values()])
    else:
        bounds = scene.bounds.reshape((1, 2, 3))
    
    bounds = np.array([bounds[:, 0, :].min(axis=0), bounds[:, 1, :].max(axis=0)])
    
    # Convert trimesh scene to pyrender scene
    py_scene = pyrender.Scene.from_trimesh_scene(scene)
    
    # Compute scene center and scale
    center = (bounds[0] + bounds[1]) / 2
    scale = np.max(bounds[1] - bounds[0])
    
    # Set up camera with a narrower field of view for more zoom
    camera = pyrender.PerspectiveCamera(yfov=np.pi / 4.0, aspectRatio=resolution[0]/resolution[1])
    
    # Position camera
    camera_pose = np.eye(4)
    camera_pose[:3, 3] = center + np.array([0, 0, scale * 1.4])  # Adjusted distance for zoom
    camera_node = py_scene.add(camera, pose=camera_pose)
    
    # Set up main light
    main_light = pyrender.DirectionalLight(color=[1.0, 1.0, 1.0], intensity=3.0)
    main_light_node = py_scene.add(main_light, pose=camera_pose)
    
    # Add a second light from behind
    back_light_pose = np.eye(4)
    back_light_pose[:3, 3] = center - np.array([0, 0, scale * 1.4])
    back_light = pyrender.DirectionalLight(color=[1.0, 1.0, 1.0], intensity=2.0)
    py_scene.add(back_light, pose=back_light_pose)
    
    # Set up renderer
    r = pyrender.OffscreenRenderer(resolution[0], resolution[1])
    
    # Create a list to store the frames
    frames = []
    
    # Calculate rotation angle for each frame
    angle_step = 2 * math.pi / num_frames
    
    for i in range(num_frames):
        # Calculate rotation
        angle = i * angle_step
        rotation = trimesh.transformations.rotation_matrix(angle, [0, 1, 0], point=center)
        
        # Apply rotation to camera and main light
        rotated_camera_pose = np.dot(rotation, camera_pose)
        py_scene.set_pose(camera_node, rotated_camera_pose)
        py_scene.set_pose(main_light_node, rotated_camera_pose)
        
        # Render the scene
        color, _ = r.render(py_scene)
        
        # Convert to PIL Image and append to frames
        image = Image.fromarray(color)
        frames.append(image)
    
    # Save the frames as a GIF
    frames[0].save(
        output_file,
        save_all=True,
        append_images=frames[1:],
        duration=100,  # Fixed duration for each frame
        loop=0
    )
    
    print(f"GIF saved as {output_file}")

# Usage
glb_file = args.glb_file
output_file = args.output_file
create_rotating_gif(glb_file, output_file, num_frames=args.num_frames, resolution=tuple(args.resolution))

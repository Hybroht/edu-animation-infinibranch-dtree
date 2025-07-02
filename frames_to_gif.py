from PIL import Image
import glob

frames = [Image.open(image) for image in sorted(glob.glob("frames/frame_*.png"))]
frames[0].save('output.gif', save_all=True, append_images=frames[1:], optimize=False, duration=40, loop=0)

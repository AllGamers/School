from PIL import Image
import threading
import glob, os


class MyThreadWithArgs(threading.Thread):

    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, *, daemon=True):
        super().__init__(group=group, target=target, name=name,
                         daemon=daemon)
        self.args = args

    def run(self):
        job_thread(self.args[0],self.args[1])


def job_thread(arch,form):
    orig_image = Image.open(arch+form)
    width, height = orig_image.size
    mode = orig_image.mode
    orig_pixel_map = orig_image.load()

    new_image_r = Image.new(mode, (width,height))
    new_pixel_map_r=new_image_r.load()

    for i in range(width):
        for j in range(height):
            orig_pixel = orig_pixel_map[i,j]

            new_r = 255
            new_g = orig_pixel[1]
            new_b = orig_pixel[2]

            new_pixel=(new_r,new_g,new_b)
            new_pixel_map_r[i,j] = new_pixel
            

    #new_image_r.show()
    new_image_r.save(arch+'R'+form)

    new_image_g = Image.new(mode, (width,height))
    new_pixel_map_g=new_image_g.load()

    for i in range(width):
        for j in range(height):
            orig_pixel = orig_pixel_map[i,j]

            new_r = orig_pixel[0]
            new_g = 255
            new_b = orig_pixel[2]

            new_pixel=(new_r,new_g,new_b)
            new_pixel_map_g[i,j] = new_pixel
            
    #new_image_g.show()
    new_image_g.save(arch+'G'+form)

    new_image_b = Image.new(mode, (width,height))
    new_pixel_map_b=new_image_b.load()

    for i in range(width):
        for j in range(height):
            orig_pixel = orig_pixel_map[i,j]

            new_r = orig_pixel[0]
            new_g = orig_pixel[1]
            new_b = 255

            new_pixel=(new_r,new_g,new_b)
            new_pixel_map_b[i,j] = new_pixel
        
    #new_path_b.show()
    new_image_b.save(arch+'B'+form)

def archivosElegibles():
    #os.chdir("/home/dw-allgamers/Escritorio/redes 2/")
    for file in glob.glob("*.jpg"):
        t=MyThreadWithArgs(args=(os.path.splitext(file)[0],os.path.splitext(file)[1]))
        t.start()

    #main_thread = threading.main_thread()
    #for t in threading.enumerate():
    #    if t is main_thread:
    #        continue
    #    t.join()

    for file in glob.glob("*.png"):
        t=MyThreadWithArgs(args=(os.path.splitext(file)[0],os.path.splitext(file)[1]))
        t.start()

    #main_thread = threading.main_thread()
    #for t in threading.enumerate():
    #    if t is main_thread:
    #        continue
    #    t.join()
    
    for file in glob.glob("*.jpeg"):
        t=MyThreadWithArgs(args=(os.path.splitext(file)[0],os.path.splitext(file)[1]))
        t.start()

    main_thread = threading.main_thread()
    for t in threading.enumerate():
        if t is main_thread:
            continue
        t.join()


archivosElegibles()
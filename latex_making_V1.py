from subprocess import call
import os
from PIL import Image





main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir,'data')
tex_files_dir = os.path.join(data_dir,'raw_tex')
indicia_dir = os.path.join(data_dir,'indicias')
pdf_dir = os.path.join(main_dir,'outputs','PDF')
junk_dir = os.path.join(main_dir,'junk')



def write_preamble(f,outputname):
    """Sets up the preamble of the latex document."""

    #sets pdf file name
    f.write(r"%& -job-name="+outputname)
    f.write('\n')
    f.write('\n')
    f.write(r"\documentclass[landscape]{article}")
    f.write('\n')
    #suppresses most of the LaTeX output
    f.write(r"\batchmode")
    f.write('\n')
    f.write(r"\usepackage{graphicx}")
    f.write('\n')
    f.write(r"\usepackage{tikz}")
    f.write('\n')
    f.write(r"\usetikzlibrary{calc}")
    f.write('\n')
    #tells LaTeX where the pictures are
    f.write(r"\graphicspath{{data/indicias/}}")
    f.write('\n')
    #turns off page numbers
    f.write(r"\pagenumbering{gobble}")
    f.write('\n')
    f.write(r"\begin{document}")
    f.write('\n')
    f.write('\n')

def insert_one_picture(f,image,pos):
    """'Private Function'
    Inserts One Picture at a corner of your choice
    f is the file handle to which you are writing
    """
    
    fullpath = os.path.join(indicia_dir,image)

    #this is from the PIL library.  I need to grab the sizes of
    #the images because LaTeX can be...douchy...about displaying images
    
    img = Image.open(fullpath)
    width,height = img.size

    f.write(r"\begin{tikzpicture}[remember picture, overlay]")
    f.write('\n')
    f.write(r"\node[anchor="+pos+r"]")
    f.write('\n')
    f.write(r"at (current page."+pos+r")")
    f.write('\n')
    f.write(r"{\includegraphics[width="+str(width)
            +r"pt,height="+str(height)
            +r"pt]{"+image+"}};")
    f.write('\n')
    f.write(r"\end{tikzpicture}")
    f.write('\n')

    
def add_pics(f,imagename,logo=None):
    """
    'Public' function
    Adds header images to each page
    Give name of indicia file and extension, but not dir path.
    Also adds logo, if required

    #f is the file to which you are writing
    """

    if not logo:
        insert_one_picture(f,imagename,'north east')
        f.write('\n\n')
    else:
        insert_one_picture(f,imagename,'north east')
        insert_one_picture(f,logo,'north west')
        f.write('\n\n')

def address_preamble(f):
    """Writes the part that defines the beginning of each address page."""

    #vertical centering
    f.write(r"\vspace*{\fill}")
    f.write('\n')
    #horizontal centering
    f.write(r"\begin{centering}")
    f.write('\n')
    #font size
    f.write(r"\begin{Large}")
    f.write('\n')
    
def address_bottom_shit(f,ii,num_copies,job_id):
    """Writes that part that closes up each address page"""

    #This closes the text controls.  Should probably be
    #variables and linked to the preamble function

    f.write(r"\end{Large}")
    f.write('\n')
    f.write(r"\end{centering}")
    f.write('\n')
    f.write(r"\vspace*{\fill}")
    f.write('\n')


    #Add the page number count and the copy count
    f.write(r"\begin{tikzpicture}[remember picture,overlay]")
    f.write('\n')
    f.write(r"\node[anchor=south west]")
    f.write('\n')
    f.write(r"at (current page.south west)")
    f.write('\n')
    f.write(r"{P"+str(ii)+'   '+"C"+num_copies+r"};")
    f.write('\n')
    f.write(r"\end{tikzpicture}")
    f.write('\n')
      
    #add the job id 
    f.write(r"\begin{tikzpicture}[remember picture,overlay]")
    f.write('\n')
    f.write(r"\node[anchor=south east]")
    f.write('\n')
    f.write(r"at (current page.south east)")
    f.write('\n')
    f.write(r"{"+str(job_id)+r"};")
    f.write('\n')
    f.write(r"\end{tikzpicture}")
    f.write('\n')
    f.write(r"\newpage")
    f.write('\n')
    f.write('\n')

    
def make_an_address_page(f,ii,line,job_id):
    """Call all the functions in order required to create one address page."""


    address_preamble(f)
    num_copies = line.pop()
    ##This assumes NumCopies is the last thing in the csv,
    #which is sort of guaranteed.
    #The Reformat addresses function will put NumCopies
    #at the end if it exists, but it doesn't have to exist

    ##It also assumes its the string of a plain integer, which is
    #technically not guaranteed
    
    for item in line:
        if item!='':
            f.write(item)
            f.write(r"\\")
            f.write('\n')

    address_bottom_shit(f,ii,num_copies,job_id)
    

def start_page(f):

    #This is the page at the beginning of the carrier section
    #currently it takes no inputs because I don't sort based
    #on carriers yet

    f.write(r"\begin{large}")
    f.write('\n')
    f.write(r"Carrier Start Sheet")
    f.write('\n')
    f.write(r"\end{large}")
    f.write('\n')
    f.write(r"\newpage")
    f.write('\n')
    f.write('\n')

def bulk_page(f,num):

    #This is the page at the beginning
    #of the bulk page section
    
    f.write(r"\begin{large}")
    f.write('\n')
    f.write(r"Bulk Copies Start Sheet\\")
    f.write('\n')
    f.write(r"Number: "+str(num))
    f.write('\n')
    f.write(r"\end{large}")
    f.write('\n')
    f.write(r"\newpage")
    f.write('\n')
    f.write('\n')

def non_bulk_page(f,num):

    #This is the page at the beginning
    #of the single page section

    f.write(r"\begin{large}")
    f.write('\n')
    f.write(r"Single Copies Start Sheet\\")
    f.write('\n')
    f.write(r"Number: "+str(num))
    f.write('\n')
    f.write(r"\end{large}")
    f.write('\n')
    f.write(r"\newpage")
    f.write('\n')
    f.write('\n')    

def end_page(f):

    #This page goes at the end of each carrier's section
    
    f.write(r"\begin{large}")
    f.write('\n')
    f.write(r"Carrier End Sheet")
    f.write('\n')
    f.write(r"\end{large}")
    f.write('\n')
    f.write(r"\newpage")
    f.write('\n')
    f.write('\n')    

def end_doc(f):

    #the last line of the tex doc
    f.write(r"\end{document}")

    
    
def create_document(filename):

    #calls pdf latex from the command line with
    #appropriate output shuffling arguments
    
    code = call(['pdflatex',
             '-output-directory='+pdf_dir,
             '-aux-directory='+junk_dir,
             os.path.join(tex_files_dir,filename)])
    





    



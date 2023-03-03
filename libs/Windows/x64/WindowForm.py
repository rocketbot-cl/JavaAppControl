import JABHandle
import clr
from time import sleep

#Add a reference for the 'System' namespace
clr.AddReference('System.IO')
clr.AddReference('System.Drawing')
clr.AddReference('System.Reflection')
clr.AddReference('System.Threading')
clr.AddReference('System.Windows.Forms')

# Import those namespace just like a regular python library
import System
import System.IO
import System.Reflection
import System.Windows.Forms
from System.Threading import ApartmentState, Thread, ThreadStart

# create our InteropExplorer Application Class Object
class InteropExplorer(System.Windows.Forms.Form):

    def __init__(self):
        
        # Define Control Container
        self.components = System.ComponentModel.Container()

        # Define the caption text
        self.Text = "Interop Explorer"

        # Define the color of our form.
        self.BackgroundColor = System.Drawing.Color.FromArgb(238,238,238)

        # Define the size of my form
        self.ClientSize = System.Drawing.Size(400,200)

        # Grab the caption height
        caption_hight = System.Windows.Forms.SystemInformation.CaptionHeight

        # Define the minimum size of my Form using the MinimunSize Property
        self.MinimumSize = System.Drawing.Size(392, (117 + caption_hight))

        """
            DEFINE THE LOAD BUTTON
        """
        
        #Create a button object
        self.LoadFileButton = System.Windows.Forms.Button()

        # Define the location of our button - POINTS
        self.LoadFileButton.Location = System.Drawing.Point(150, 10)

        # Define the size of our button - POINTS
        self.LoadFileButton.Size = System.Drawing.Size(156, 154)

        # Define the Style of our button
        self.LoadFileButton.FlatStyle = System.Windows.Forms.FlatStyle.Flat
        # self.LoadFileButton.FlatAppearance.BorderSize = 0

        """ 
        BIND EVENTS TO CONTROL
        """
        self.LoadFileButton.MouseClick += self.LoadFileButton_mouse_enter

        """
            ADD CONTROLS TO OUR FORM
        """

        self.Controls.Add(self.LoadFileButton)

    def LoadFileButton_mouse_enter(self, sender, args):
        #hwnd = JABHandle.getHandle("Calculator PH")
        #hwnd = JABHandle.getHandle("Mineria de Datos")
        hwnd = JABHandle.getHandle("Texty - Text Editor")
        print("Handle: " + str(hwnd))
        JABHandle.explorer(hwnd)
    
    def dispose(self):
        """
            Dispose of Form and Component Container
        """
        # Dispose of components
        self.components.Dispose()
        System.Windows.Forms.Form.Dispose(self)


    def run(self):
        """
            Start our Form Object
        """

        # Run  the InteropExplorer
        System.Windows.Application.Run(self)


def main_from_thread():

    #initialize the form
    interop_form = InteropExplorer()

    # Print some info on the ocnsole
    print("A new instance of the InteropExplorer has been created")

    #Define our new Windows.Forms.Application object
    win_form_app = System.Windows.Forms.Application

    # Run our Interop Explorer
    win_form_app.Run(interop_form)

if __name__ == "__main__":

    #run the main message thread 
    main_from_thread()


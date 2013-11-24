# Copyright (c) 2013 phrack. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

from canvas_manager import CanvasManager
import os
from PIL import Image, ImageTk
from tag_editor_popup import TagEditorPopup
from target_pickler import TargetPickler
import Tkinter, tkFileDialog, ttk

CURSOR = 0
RECTANGLE = 1
OVAL = 2
TRIANGLE = 3

# AQT constants - ouchie
AQT3 = 10
AQT4 = 11
AQT5 = 12

CANVAS_BACKGROUND = (1,)

class TargetEditor():
    def save_target(self):
        target_file = tkFileDialog.asksaveasfilename(
            defaultextension=".target",
            filetypes=[("ShootOFF Target", ".target")],
            initialdir="targets/",
            title="Save ShootOFF Target",
            parent=self._window)

        if (target_file and not os.path.isfile(target_file)):
            self._notify_new_target(target_file)

        if target_file:
            target_pickler = TargetPickler()
            target_pickler.save(target_file, self._regions,
                self._target_canvas)

    def color_selected(self, event):
        if (self._selected_region is not None and
            self._selected_region != CANVAS_BACKGROUND):               

            self._target_canvas.itemconfig(self._selected_region,
                fill=self._fill_color_combo.get())

    def bring_forward(self):
        if (self._selected_region is not None and
            self._selected_region != CANVAS_BACKGROUND):
            
            below = self._target_canvas.find_above(self._selected_region)
            
            if len(below) > 0:
                self._target_canvas.tag_raise(self._selected_region,
                    below)

                # we have to change the order in the regions list
                # as well so the z order is maintained during pickling
                self.reverse_regions(below, self._selected_region)

    def send_backward(self):
        if (self._selected_region is not None and
            self._selected_region != CANVAS_BACKGROUND):
            
            above = self._target_canvas.find_below(self._selected_region)

            if len(above) > 0  and above != CANVAS_BACKGROUND:
                self._target_canvas.tag_lower(self._selected_region,
                    above)

                # we have to change the order in the regions list
                # as well so the z order is maintained during pickling
                self.reverse_regions(above, self._selected_region)

    def reverse_regions(self, region1, region2):
        r1 = self._regions.index(region1[0])
        r2 = self._regions.index(region2[0])

        self._regions[r2], self._regions[r1] = self._regions[r1], self._regions[r2]

    def canvas_click(self, event):
        if self._radio_selection.get() != CURSOR:
            # This will make it so that mouse move event
            # won't delete the current cursor shape and will
            # make a new one, thus leaving the current shape 
            # as a region
            self._regions.append(self._cursor_shape)
            self._cursor_shape = None
        else:
            old_region = self._selected_region
            self._selected_region = event.widget.find_closest(
                event.x, event.y)  

            self._canvas_manager.selection_update_listener(old_region,
                self._selected_region)

            if self._selected_region != CANVAS_BACKGROUND:
                self._fill_color_combo.configure(state="readonly") 
                self._fill_color_combo.set(
                    event.widget.itemcget(self._selected_region, "fill"))

                self._tags_button.configure(state=Tkinter.NORMAL)

                if self._tag_popup_state.get()==True:
                    self.toggle_tag_editor()
            else:
                self._fill_color_combo.configure(state=Tkinter.DISABLED)  
                self._tags_button.configure(state=Tkinter.DISABLED)  

                if self._tag_popup_state.get()==True:
                    self._tag_popup_state.set(False)
                    self.toggle_tag_editor()

    def canvas_mouse_move(self, event):
        if self._cursor_shape is not None:
            self._target_canvas.delete(self._cursor_shape)
        
        if self._radio_selection.get() == CURSOR:
            self._cursor_shape = None

        initial_size = 30
        AQT_scale = 2.5 # ouchie

        if self._radio_selection.get() == RECTANGLE:        
            self._cursor_shape = self._target_canvas.create_rectangle(
                event.x - initial_size,
                event.y - initial_size,
                event.x + initial_size,
                event.y + initial_size, 
                fill="black", stipple="gray25", tags=("_shape:rectangle"))

        elif self._radio_selection.get() == OVAL:        
            self._cursor_shape = self._target_canvas.create_oval(
                event.x - initial_size,
                event.y - initial_size,
                event.x + initial_size,
                event.y + initial_size, 
                fill="black", stipple="gray25", tags=("_shape:oval"))

        elif self._radio_selection.get() == TRIANGLE:        
            self._cursor_shape = self._target_canvas.create_polygon(
                event.x,
                event.y - initial_size,
                event.x + initial_size,
                event.y + initial_size,
                event.x - initial_size,
                event.y + initial_size, 
                event.x,
                event.y - initial_size,
                fill="black", outline="black", stipple="gray25",
                tags=("_shape:triangle"))
            
        # AQT target shapes - ouchie
        elif self._radio_selection.get() == AQT3:        
            self._cursor_shape = self._target_canvas.create_polygon(
                event.x+15.083*AQT_scale,event.y+13.12*AQT_scale,
                event.x+15.083*AQT_scale,event.y+-0.147*AQT_scale,
                event.x+14.277*AQT_scale,event.y+-2.508*AQT_scale,
                event.x+13.149*AQT_scale,event.y+-4.115*AQT_scale,
                event.x+11.841*AQT_scale,event.y+-5.257*AQT_scale,
                event.x+10.557*AQT_scale,event.y+-6.064*AQT_scale,
                event.x+8.689*AQT_scale,event.y+-6.811*AQT_scale,
                event.x+7.539*AQT_scale,event.y+-8.439*AQT_scale,
                event.x+7.076*AQT_scale,event.y+-9.978*AQT_scale,
                event.x+6.104*AQT_scale,event.y+-11.577*AQT_scale,
                event.x+4.82*AQT_scale,event.y+-12.829*AQT_scale,
                event.x+3.43*AQT_scale,event.y+-13.788*AQT_scale,
                event.x+1.757*AQT_scale,event.y+-14.386*AQT_scale,
                event.x+0.083*AQT_scale,event.y+-14.55*AQT_scale,
                event.x+-1.59*AQT_scale,event.y+-14.386*AQT_scale,
                event.x+-3.263*AQT_scale,event.y+-13.788*AQT_scale,
                event.x+-4.653*AQT_scale,event.y+-12.829*AQT_scale,
                event.x+-5.938*AQT_scale,event.y+-11.577*AQT_scale,
                event.x+-6.909*AQT_scale,event.y+-9.978*AQT_scale,
                event.x+-7.372*AQT_scale,event.y+-8.439*AQT_scale,
                event.x+-8.522*AQT_scale,event.y+-6.811*AQT_scale,
                event.x+-10.39*AQT_scale,event.y+-6.064*AQT_scale,
                event.x+-11.674*AQT_scale,event.y+-5.257*AQT_scale,
                event.x+-12.982*AQT_scale,event.y+-4.115*AQT_scale,
                event.x+-14.11*AQT_scale,event.y+-2.508*AQT_scale,
                event.x+-14.917*AQT_scale,event.y+-0.147*AQT_scale,
                event.x+-14.917*AQT_scale,event.y+13.12*AQT_scale,
                fill="white", outline="black",
                tags=("_shape:aqt3"))

        elif self._radio_selection.get() == AQT4:        
            self._cursor_shape = self._target_canvas.create_polygon(
                event.x+11.66*AQT_scale,event.y+5.51*AQT_scale,
                event.x+11.595*AQT_scale,event.y+0.689*AQT_scale,
                event.x+11.1*AQT_scale,event.y+-1.084*AQT_scale,
                event.x+9.832*AQT_scale,event.y+-2.441*AQT_scale,
                event.x+7.677*AQT_scale,event.y+-3.322*AQT_scale,
                event.x+5.821*AQT_scale,event.y+-4.709*AQT_scale,
                event.x+4.715*AQT_scale,event.y+-6.497*AQT_scale,
                event.x+4.267*AQT_scale,event.y+-8.135*AQT_scale,
                event.x+3.669*AQT_scale,event.y+-9.41*AQT_scale,
                event.x+2.534*AQT_scale,event.y+-10.553*AQT_scale,
                event.x+1.436*AQT_scale,event.y+-11.091*AQT_scale,
                event.x+0.083*AQT_scale,event.y+-11.323*AQT_scale,
                event.x+-1.269*AQT_scale,event.y+-11.091*AQT_scale,
                event.x+-2.367*AQT_scale,event.y+-10.553*AQT_scale,
                event.x+-3.502*AQT_scale,event.y+-9.41*AQT_scale,
                event.x+-4.1*AQT_scale,event.y+-8.135*AQT_scale,
                event.x+-4.548*AQT_scale,event.y+-6.497*AQT_scale,
                event.x+-5.654*AQT_scale,event.y+-4.709*AQT_scale,
                event.x+-7.51*AQT_scale,event.y+-3.322*AQT_scale,
                event.x+-9.665*AQT_scale,event.y+-2.441*AQT_scale,
                event.x+-10.933*AQT_scale,event.y+-1.084*AQT_scale,
                event.x+-11.428*AQT_scale,event.y+0.689*AQT_scale,
                event.x+-11.493*AQT_scale,event.y+5.51*AQT_scale,
                fill="black", outline="white",
                tags=("_shape:aqt4"))
            
        elif self._radio_selection.get() == AQT5:        
            self._cursor_shape = self._target_canvas.create_polygon(
                event.x+7.893*AQT_scale,event.y+3.418*AQT_scale,
                event.x+7.893*AQT_scale,event.y+1.147*AQT_scale,
                event.x+7.255*AQT_scale,event.y+0.331*AQT_scale,
                event.x+5.622*AQT_scale,event.y+-0.247*AQT_scale,
                event.x+4.187*AQT_scale,event.y+-1.124*AQT_scale,
                event.x+2.833*AQT_scale,event.y+-2.339*AQT_scale,
                event.x+1.917*AQT_scale,event.y+-3.594*AQT_scale,
                event.x+1.219*AQT_scale,event.y+-5.048*AQT_scale,
                event.x+0.9*AQT_scale,event.y+-6.223*AQT_scale,
                event.x+0.801*AQT_scale,event.y+-7.1*AQT_scale,
                event.x+0.521*AQT_scale,event.y+-7.558*AQT_scale,
                event.x+0.083*AQT_scale,event.y+-7.617*AQT_scale,
                event.x+-0.354*AQT_scale,event.y+-7.558*AQT_scale,
                event.x+-0.634*AQT_scale,event.y+-7.1*AQT_scale,
                event.x+-0.733*AQT_scale,event.y+-6.223*AQT_scale,
                event.x+-1.052*AQT_scale,event.y+-5.048*AQT_scale,
                event.x+-1.75*AQT_scale,event.y+-3.594*AQT_scale,
                event.x+-2.666*AQT_scale,event.y+-2.339*AQT_scale,
                event.x+-4.02*AQT_scale,event.y+-1.124*AQT_scale,
                event.x+-5.455*AQT_scale,event.y+-0.247*AQT_scale,
                event.x+-7.088*AQT_scale,event.y+0.331*AQT_scale,
                event.x+-7.726*AQT_scale,event.y+1.147*AQT_scale,
                event.x+-7.726*AQT_scale,event.y+3.418*AQT_scale,
                fill="black", outline="white",
                tags=("_shape:aqt5"))

    def canvas_delete_region(self, event):
        if (self._selected_region is not None and
            self._selected_region != CANVAS_BACKGROUND):
            
            for shape in self._selected_region:
                self._regions.remove(shape)
            event.widget.delete(self._selected_region)
            self._selected_region = None

    def toggle_tag_editor(self):
        if self._tag_popup_state.get()==True:
            x = (self._tags_button.winfo_x() + 
                (self._tags_button.winfo_width() / 2))
            y = (self._tags_button.winfo_y() +
                (self._tags_button.winfo_height() * 1.5))

            self._tag_editor.show(
                self._target_canvas.gettags(self._selected_region), x, y)
        else:
            self._tag_editor.hide()

    def update_tags(self, new_tag_list):
        # delete all of the non-internal tags
        for tag in self._target_canvas.gettags(self._selected_region):
            if not tag.startswith("_"):
                self._target_canvas.dtag(self._selected_region,
                   tag)

        # add all tags in the new tag list        
        tags = self._target_canvas.gettags(self._selected_region)
        self._target_canvas.itemconfig(self._selected_region, 
            tags=tags + new_tag_list)

    def build_gui(self, parent, webcam_image):
        # Create the main window
        self._window = Tkinter.Toplevel(parent)
        self._window.transient(parent)
        self._window.title("Target Editor")

        self._frame = ttk.Frame(self._window)
        self._frame.pack(padx=15, pady=15)

        self.create_toolbar(self._frame)
 
        # Create tags popup frame
        self._tag_editor = TagEditorPopup(self._window, self.update_tags)

        # Create the canvas the target will be drawn on
        # and show the webcam frame in it
        self._webcam_image = webcam_image

        self._target_canvas = Tkinter.Canvas(self._frame, 
            width=webcam_image.width(), height=webcam_image.height()) 
        self._target_canvas.create_image(0, 0, image=self._webcam_image,
            anchor=Tkinter.NW, tags=("background"))
        self._target_canvas.pack()

        self._target_canvas.bind('<ButtonPress-1>', self.canvas_click)
        self._target_canvas.bind('<Motion>', self.canvas_mouse_move)
        self._target_canvas.bind('<Delete>', self.canvas_delete_region)

        self._canvas_manager = CanvasManager(self._target_canvas)

        # Align this window with it's parent otherwise it ends up all kinds of
        # crazy places when multiple monitors are used
        parent_x = parent.winfo_rootx()
        parent_y = parent.winfo_rooty()

        self._window.geometry("+%d+%d" % (parent_x+20, parent_y+20))

    def create_toolbar(self, parent):
       # Create the toolbar
        toolbar = Tkinter.Frame(parent, bd=1, relief=Tkinter.RAISED)
        self._radio_selection = Tkinter.IntVar()
        self._radio_selection.set(CURSOR)

        # Save button
        self._save_icon = Image.open("images/gnome_media_floppy.png")
        self.create_toolbar_button(toolbar, self._save_icon, 
            self.save_target)
        
        # cursor button
        self._cursor_icon = Image.open("images/cursor.png")
        self.create_radio_button(toolbar, self._cursor_icon, CURSOR)

        # rectangle button
        self._rectangle_icon = Image.open("images/rectangle.png")
        self.create_radio_button(toolbar, self._rectangle_icon, RECTANGLE)

        # oval button
        self._oval_icon = Image.open("images/oval.png")
        self.create_radio_button(toolbar, self._oval_icon, OVAL)

        # triangle button
        self._triangle_icon = Image.open("images/triangle.png")
        self.create_radio_button(toolbar, self._triangle_icon, TRIANGLE)

        # AQT3 button
        self._triangle_icon = Image.open("images/AQT3.png")
        self.create_radio_button(toolbar, self._triangle_icon, AQT3)

        # AQT4 button
        self._triangle_icon = Image.open("images/AQT4.png")
        self.create_radio_button(toolbar, self._triangle_icon, AQT4)
        
        # AQT5 button
        self._triangle_icon = Image.open("images/AQT5.png")
        self.create_radio_button(toolbar, self._triangle_icon, AQT5)
        
        # bring forward button
        self._bring_forward_icon = Image.open("images/bring_forward.png")
        self.create_toolbar_button(toolbar, self._bring_forward_icon, 
            self.bring_forward)

        # send backward button
        self._send_backward_icon = Image.open("images/send_backward.png")
        self.create_toolbar_button(toolbar, self._send_backward_icon, 
            self.send_backward)

        # show tags button
        tags_icon = ImageTk.PhotoImage(Image.open("images/tags.png"))  

        self._tag_popup_state = Tkinter.IntVar()
        self._tags_button = Tkinter.Checkbutton(toolbar,
            image=tags_icon, indicatoron=False, variable=self._tag_popup_state,
            command=self.toggle_tag_editor, state=Tkinter.DISABLED)
        self._tags_button.image = tags_icon
        self._tags_button.pack(side=Tkinter.LEFT, padx=2, pady=2)

        # color chooser
        self._fill_color_combo = ttk.Combobox(toolbar,
            values=["black", "blue", "green", "orange", "red", "white"],
            state="readonly")
        self._fill_color_combo.set("black")
        self._fill_color_combo.bind("<<ComboboxSelected>>", self.color_selected)
        self._fill_color_combo.configure(state=Tkinter.DISABLED)
        self._fill_color_combo.pack(side=Tkinter.LEFT, padx=2, pady=2)

        toolbar.pack(fill=Tkinter.X)

    def create_radio_button(self, parent, image, selected_value):
        icon = ImageTk.PhotoImage(image)  

        button = Tkinter.Radiobutton(parent, image=icon,              
            indicatoron=False, variable=self._radio_selection,
            value=selected_value)
        button.image = icon
        button.pack(side=Tkinter.LEFT, padx=2, pady=2)

    def create_toolbar_button(self, parent, image, command, enabled=True):
        icon = ImageTk.PhotoImage(image)  

        button = Tkinter.Button(parent, image=icon, relief=Tkinter.RAISED, command=command)

        if not enabled:
            button.configure(state=Tkinter.DISABLED)

        button.image = icon
        button.pack(side=Tkinter.LEFT, padx=2, pady=2)

    # target is set when we are editing a target,
    # otherwise we are creating a new target

    # notifynewfunc is a callback that can be set to see
    # when a new target is saved (e.g. the save button is
    # hit AND results in a new file). The callback takes
    # one parameter (the targets file name)
    def __init__(self, parent, webcam_image, target=None,
        notifynewfunc=None):

        self._cursor_shape = None
        self._selected_region = None
        self._regions = []
        self.build_gui(parent, webcam_image)

        if target is not None:
            target_pickler = TargetPickler()
            (region_object, self._regions) = target_pickler.load(
                target, self._target_canvas)

        self._notify_new_target = notifynewfunc

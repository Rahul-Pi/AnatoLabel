import tkinter as tk
from tkinter import filedialog, messagebox
import json
import os
from anatomial_config import COLOR_MAP, body_regions, region_groups

BASE_DIM = 1080  # original image size for normalization

# Path to the base image (ensure Tool_example.png is in the same directory)
IMAGE_PATH = os.path.join(os.path.dirname(__file__), 'Tool_exampl.png')

# invert mapping for quick lookup
region_to_group = {r: g for g, regs in region_groups.items() for r in regs}

def point_in_poly(x, y, poly):
    """Ray casting algorithm to test if a point is inside a polygon."""
    num = len(poly)
    j = num - 1
    inside = False
    for i in range(num):
        xi, yi = poly[i]
        xj, yj = poly[j]
        if ((yi > y) != (yj > y)) and (x < (xj - xi) * (y - yi) / (yj - yi) + xi):
            inside = not inside
        j = i
    return inside

class AnatoLabel:
    def __init__(self, master):
        self.master = master
        master.title("AnatoLabel")

        self.annotations = {}
        self.current_annotations = {}  # mapping label to AIS level
        self.annotation_items = {}  # track canvas items per label

        self.setup_ui()
        self.load_image()

    def setup_ui(self):
        toolbar = tk.Frame(self.master)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        tk.Label(toolbar, text="Case #: ").pack(side=tk.LEFT)
        self.case_entry = tk.Entry(toolbar, width=10)
        self.case_entry.pack(side=tk.LEFT)

        tk.Button(toolbar, text="Import Dataset", command=self.import_dataset).pack(side=tk.LEFT, padx=5)
        tk.Button(toolbar, text="Report", command=self.show_report).pack(side=tk.LEFT, padx=5)

        # main content area with canvas on left and annotation list on right
        content = tk.Frame(self.master)
        content.pack(fill=tk.BOTH, expand=True)

        # Canvas frame
        canvas_frame = tk.Frame(content)
        canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.canvas = tk.Canvas(canvas_frame, cursor="tcross")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Annotation list frame
        list_frame = tk.Frame(content, bd=1, relief=tk.SUNKEN)
        list_frame.pack(side=tk.RIGHT, fill=tk.Y)
        tk.Label(list_frame, text="Annotated Parts:").pack(pady=(5,0))
        self.listbox = tk.Listbox(list_frame)
        self.listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Bind mouse and keyboard
        self.canvas.bind("<Button-1>", self.on_click)
        self.master.bind("<Control-s>", self.save_annotations)
        self.master.bind("<Control-n>", self.new_case)
        # after entering case number, press Enter to move focus away
        self.case_entry.bind('<Return>', lambda e: self.canvas.focus_set())

    def load_image(self):
        self.image = tk.PhotoImage(file=IMAGE_PATH)
        self.canvas.config(width=self.image.width(), height=self.image.height())
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image)
        # compute scale and scaled coordinate maps
        self.scale = self.image.width() / BASE_DIM
        self.scaled_regions = {
            label: [(x * self.scale, y * self.scale) for x, y in poly]
            for label, poly in body_regions.items()
        }

    def on_click(self, event):
        case_no = self.case_entry.get().strip()
        if not case_no:
            messagebox.showwarning("Input required", "Please enter case number.")
            return
        x, y = event.x, event.y
        # use scaled polygons
        for region, poly in self.scaled_regions.items():
            if point_in_poly(x, y, poly):
                label = region_to_group.get(region, region)
                # If already annotated, toggle off (remove)
                if label in self.current_annotations:
                    # remove highlighted polygons
                    for iid in self.annotation_items.pop(label, []):
                        self.canvas.delete(iid)
                    # remove from data and listbox
                    level = self.current_annotations.pop(label, None)
                    for idx, itm in enumerate(self.listbox.get(0, tk.END)):
                        if itm.startswith(label + ":"):
                            self.listbox.delete(idx)
                            break
                    return
                # Prompt user for AIS level
                level_window = tk.Toplevel(self.master)
                level_window.title(f"Select AIS level for {label}")
                selected_level = tk.IntVar(value=1)

                def confirm_level(event=None):
                    lvl = selected_level.get()
                    level_window.grab_release() # Release grab before destroying
                    level_window.destroy()
                    # proceed with annotation using lvl
                    self.add_annotation(label, lvl)

                def cancel_level():
                    level_window.grab_release() # Release grab before destroying
                    level_window.destroy()

                # Radiobuttons for levels 1-6
                for i in range(1, 7):
                    rb = tk.Radiobutton(level_window, text=str(i), variable=selected_level, value=i)
                    rb.pack(side=tk.LEFT)
                    # bind number key
                    level_window.bind(str(i), lambda e, v=i: selected_level.set(v))

                confirm_btn = tk.Button(level_window, text="Confirm", command=confirm_level)
                confirm_btn.pack(side=tk.LEFT)
                level_window.bind('<Return>', confirm_level)
                level_window.bind('<Escape>', lambda e: cancel_level())
                level_window.protocol("WM_DELETE_WINDOW", cancel_level)
                
                # Ensure the new window gets focus and is modal
                level_window.focus_set() # Give focus to the new window
                level_window.grab_set() # Make the window modal
                
                return

    def add_annotation(self, label, level):
        """Helper to add annotation with AIS level and color."""
        # highlight all associated regions with level color
        item_ids = []
        for r in region_groups.get(label, [label]):
            pts = self.scaled_regions.get(r)
            if not pts:
                continue
            flat = [coord for pt in pts for coord in pt]
            color = COLOR_MAP.get(level, '#B76E79')
            iid = self.canvas.create_polygon(flat, outline='red', fill=color, width=2, splinesteps=20)
            item_ids.append(iid)
        self.annotation_items[label] = item_ids
        # record annotation
        self.current_annotations[label] = level
        # update listbox entry
        self.listbox.insert(tk.END, f"{label}: AIS{level}")

    def save_annotations(self, event=None):
        case_no = self.case_entry.get().strip()
        if not case_no:
            messagebox.showwarning("Input required", "Please enter case number.")
            return
        # Save mapping of labels to AIS levels
        self.annotations[case_no] = self.current_annotations.copy()
        with open('annotations.json', 'w') as f:
            json.dump(self.annotations, f, indent=2)
        messagebox.showinfo("Saved", f"Annotations saved for case {case_no}.")

    def new_case(self, event=None):
        self.current_annotations.clear()  # clear label->level mapping
        self.canvas.delete("all")
        self.load_image()
        self.case_entry.delete(0, tk.END)
        # clear annotation listbox
        self.listbox.delete(0, tk.END)
        # reset undo/redo
        self.annotation_items.clear()

    def import_dataset(self):
        path = filedialog.askopenfilename(filetypes=[('JSON', '*.json')])
        if not path:
            return
        with open(path, 'r') as f:
            data = json.load(f)
        self.annotations.update(data)
        messagebox.showinfo("Imported", f"Loaded {len(data)} cases.")

    def show_report(self):
        # create report window with canvas and case-list panel
        report_win = tk.Toplevel(self.master)
        report_win.title("Injury Report")
        content = tk.Frame(report_win)
        content.pack(fill=tk.BOTH, expand=True)
        # canvas on left
        canvas_frame = tk.Frame(content)
        canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        canv = tk.Canvas(canvas_frame, cursor="tcross")
        canv.pack(fill=tk.BOTH, expand=True)
        # case list on right
        list_frame = tk.Frame(content, bd=1, relief=tk.SUNKEN)
        list_frame.pack(side=tk.RIGHT, fill=tk.Y)
        tk.Label(list_frame, text="Cases:").pack(pady=(5,0))
        report_listbox = tk.Listbox(list_frame)
        report_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # draw base image
        img = tk.PhotoImage(file=IMAGE_PATH)
        canv.config(width=img.width(), height=img.height())
        canv.create_image(0, 0, anchor=tk.NW, image=img)
        report_win.image = img  # prevent GC

        # build case map and counts
        case_map = {}
        for case, parts in self.annotations.items():
            for p in parts:
                case_map.setdefault(p, []).append(case)
        if not case_map:
            return
        max_count = max(len(v) for v in case_map.values())

        # shade each body part by intensity
        for part, cases in case_map.items():
            poly = self.scaled_regions.get(part)
            if not poly:
                continue
            # compute color intensity (red spectrum)
            intensity = int(255 * len(cases) / max_count)
            # lighter for fewer, darker for more
            r = 255
            g = b = 255 - intensity
            color = f"#{r:02x}{g:02x}{b:02x}"
            flat = [coord for pt in poly for coord in pt]
            canv.create_polygon(flat, outline='black', fill=color, tags=(part,))

        # on click, show cases for a part
        def on_report_click(event):
            x, y = event.x, event.y
            # identify clicked item
            items = canv.find_overlapping(x, y, x, y)
            for iid in items:
                tags = canv.gettags(iid)
                for tag in tags:
                    if tag in case_map:
                        report_listbox.delete(0, tk.END)
                        for c in case_map[tag]:
                            report_listbox.insert(tk.END, c)
                        return
        canv.bind('<Button-1>', on_report_click)

    def undo(self, event=None):
        if not self.undo_stack:
            return
        action, label, level = self.undo_stack.pop()
        if action == 'add':
            # remove highlights
            for iid in self.annotation_items.pop(label, []):
                self.canvas.delete(iid)
            # remove annotation
            self.current_annotations.pop(label, None)
            # remove from listbox
            items = list(self.listbox.get(0, tk.END))
            for idx, itm in enumerate(items):
                if itm.startswith(label + ":"):
                    self.listbox.delete(idx)
                    break
            # record for redo
            self.redo_stack.append(('add', label, level))

    def redo(self, event=None):
        if not self.redo_stack:
            return
        action, label, level = self.redo_stack.pop()
        if action == 'add':
            # re-add annotation with saved AIS level
            item_ids = []
            for r in region_groups.get(label, [label]):
                pts = self.scaled_regions.get(r)
                if not pts: continue
                flat = [coord for pt in pts for coord in pt]
                color = COLOR_MAP.get(level, '#B76E79')
                iid = self.canvas.create_polygon(flat, outline='red', fill=color, width=2, splinesteps=20)
                item_ids.append(iid)
            self.annotation_items[label] = item_ids
            self.current_annotations[label] = level
            self.listbox.insert(tk.END, f"{label}: AIS{level}")
            self.undo_stack.append(('add', label, level))

if __name__ == '__main__':
    root = tk.Tk()
    app = AnatoLabel(root)
    root.mainloop()
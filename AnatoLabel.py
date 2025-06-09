import tkinter as tk
from tkinter import filedialog, messagebox
import json
import os
BASE_DIM = 1080  # original image size for normalization

# Path to the base image (ensure Tool_example.png is in the same directory)
IMAGE_PATH = os.path.join(os.path.dirname(__file__), 'Tool_exampl.png')

# Define body part regions as polygons. Coordinates are placeholders and need tuning.
body_regions = {
    'head': [(235,70),(250,45),(280,33),(310,45),(325,70),(322,35),(305,20),(280,10),(255,20),(238,34.957),(235,70)],
    'face': [(235,70),(250,45),(280,33),(310,45),(325,70),(310,130),(280,150),(250,130),(235,70)],
    'head_back': [(760,105),(790,115),(820,105),(840,80),(840,40),(820,20),(790,10),(760,20),(740,40),(740,80),(760,105)],
    'shoulder_left': [(375,290),(350,200),(292,200),(312,160),(390,195),(415,215),(425,240),(425,290),(375,290)],
    'shoulder_b_left': [(745,205),(755,230),(750,290),(732,305),(715,285),(695,270),(650,270),(660,215),(753,165),(775,178),(790,185),(745,205)],
    'neck': [(248, 160), (268, 200), (292, 200), (312, 160), (310, 130), (280, 150), (250, 130), (248, 160)],
    'neck_b_right': [(827,165),(805,178),(805,110),(820,105),(820,150),(827,165)],
    'neck_b_left': [(760,105),(775,110), (775,178),(753,165),(760,150), (760,105)],
    'cervical_spine': [(775,178), (775,110), (790,115), (805,110), (805,178), (790,185), (775,178)],
    'shoulder_right': [(248,160),(268,200),(210,200),(185,290),(135,290),(135,240),(145,215),(170,195),(248,160)],
    'shoulder_b_right': [(827,165),(805,178),(790,185),(835,205),(825,230),(830,290),(848,305),(865,285),(885,270),(930,270),(920,215),(827,165)],
    'arm_left': [(425,290),(375,290),(380,365),(425,350),(425,290)],
    'arm_b_left': [(650,270),(695,270),(700,315),(690,365),(645,350),(650,270)],
    'arm_right': [(185,290),(135,290),(135,350),(180,365),(185,290)],
    'arm_b_right': [(930,270),(885,270),(880,315),(890,365),(935,350),(930,270)],
    'elbow_left': [(380,365),(425,350),(425,365),(437,400),(384,407),(380,365)],
    'elbow_b_left': [(645,350),(690,365),(685,407),(630,400),(644.973,365),(645,350)],
    'elbow_right': [(135,350),(180,365),(176,407),(123,400),(135,365),(135,350)],
    'elbow_b_right': [(890,365),(935,350),(935,365),(950,400),(895,407),(890,365)],
    'forearm_left': [(384,407),(437,400),(449,495),(410,505),(384,407)],
    'forearm_b_left': [(630,400),(685,407),(655,505),(616,495),(630,400)],
    'forearm_right': [(123,400),(176,407),(150,505),(111,495),(123,400)],
    'forearm_b_right': [(895,407),(950,400),(964,495),(925,505),(895,407)],
    'sternum': [(270,225),(268,200),(292,200),(290,225),(290,280),(280,310),(270,280),(270,225)],
    'chest_b_right': [(835,205),(825,230),(830,290),(848,305),(865,285),(885,270),(880,315),(865,385),(830,395),(790,380),(805,365),(805,191.667),(835,205)],
    'chest_b_left': [(745,205),(755,230),(750,290),(732,305),(715,285),(695,270),(700,315),(715,385),(750,395),(790,380),(775,365),(775,191.667),(745,205)],
    'thoracic_spine': [(790,185),(775,191.667),(775,365),(790,380),(805,365),(805,191.667),(790,185)],
    'chest_left': [(375,290),(350,200),(292,200),(290,225),(290,280),(280,310),(345,390),(375,290)],
    'chest_right': [(270,280),(270,225),(268,200),(210,200),(185,290),(215,390),(280,310),(270,280)],
    'abdomen': [(345,390),(350,450),(330,470),(330,490),(280,505),(230,490),(230,470),(210,450),(215,390),(280,310),(345,390)],
    'lumbar_spine': [(790,495),(775,480),(775,385.625),(790,380),(805,385.625),(805,480),(790,495)],
    'back_left': [(735,435),(750,440),(765,450),(775,480),(775,385.625),(750,395),(715,385),(710,445),(735,435)],
    'back_right': [(845,435),(830,440),(815,450),(805,480),(805,385.625),(830,395),(865,385),(870,445),(845,435)],
    'pelvis_right': [(280,550),(255,497.5),(230,490),(230,470),(210,450),(195,540),(235,535),(280,550)],
    'pelvis_left': [(280,550),(305,497.5),(330,490),(330,470),(350,450),(365,540),(325,535),(280,550)],
    'pelvis_b_right': [(845,435),(830,440),(815,450),(805,480),(790,495),(790,545),(805,565),(830,570),(860,560),(880,530),(870,445),(845,435)],
    'pelvis_b_left': [(735,435),(750,440),(765,450),(775,480),(790,495),(790,545),(775,565),(750,570),(720,560),(700,530),(710,445),(735,435)],
    'groin': [(280,550),(305,497.5),(280,505),(255,497.5),(280,550)],
    'thigh_b_right': [(860,705),(800,705),(790,545),(805,565),(830,570),(860,560),(880,530),(875,620),(860,705)],
    'thigh_b_left': [(720,705),(780,705),(790,545),(775,565),(750,570),(720,560),(700,530),(705,620),(720,705)],
    'thigh_right': [(280,550),(273,625),(270,705),(240,690),(212,705),(195,620),(195,540),(235,535),(280,550)],
    'thigh_left': [(280,550),(287,625),(290,705),(320,690),(348,705),(365,620),(365,540),(325,535),(280,550)],
    'knee_b_right': [(860,705),(800,705),(797,730),(805,760),(860,755),(860,705)],
    'knee_b_left': [(720,705),(780,705),(783,730),(775,760),(720,755),(720,705)],   
    'knee_left': [(290,755),(290,705),(320,690),(348,705),(348,755),(320,780),(290,755)],
    'knee_right': [(270,755),(270,705),(240,690),(212,705),(212,750),(240,780),(270,755)],
    'calf_b_right': [(838,910),(820,890),(800,895),(797,815),(805,760),(860,755),(865,825),(838,910)],
    'calf_b_left': [(742,910),(760,890),(780,895),(783,815),(775,760),(720,755),(715,825),(742,910)],
    'calf_left': [(290,755),(285,815),(289,917),(323,917),(350,820),(348,755),(320,780),(290,755)],
    'calf_right': [(270,755),(275,815.001),(271,917),(237,917),(225,870),(210,820),(212,750),(240,780),(270,755)],
    'ankle_b_right': [(838,910),(820,890),(800,895),(800,910),(820,925),(840,960),(838,910)],
    'ankle_b_left': [(742,910),(760,890),(780,895),(780,910),(760,925),(740,960),(742,910)],
    'ankle_left': [(284,945),(289,917),(323,917),(323,945),(305,940),(284,945)],
    'ankle_right': [(276,945),(271,917),(237,917),(237,945),(255,940),(276,945)],
    'feet_b_left': [(740,978),(737,992),(728,1003),(732,1019),(768,1045),(785,1035),(787,1012),(785,973),(789,958),(787,943),(780,910),(760,925),(740,960)],
    'feet_b_right': [(840,978),(843,992),(852,1003),(848,1019),(814,1045),(795,1035),(793,1012),(795,973),(791,958),(793,943),(800,910),(820,925),(840,960)],
    'feet_right': [(276,945),(277,960),(267,975),(267,1010),(269,1025),(257,1040),(240,1045),(219,1030),(205,1005),(209,992),(219,988),(237,945),(255,940)],
    'feet_left': [(284,945),(283,960),(293,975),(293,1010),(291,1025),(303,1040),(320,1045),(341,1030),(355,1005),(351,992),(341,988),(323,945),(305,940)],
    'wrist_b_right': [(925,505),(964,495),(973,520),(933,530),(925,505)],
    'wrist_b_left': [(616,495),(655,505),(647,530),(607,520),(616,495)],
    'wrist_l': [(410,505),(449,495),(460,520),(415,530),(410,505)],
    'wrist_r': [(111,495),(150,505),(145,530),(100,520),(111,495)],
    'hand_b_right': [(995,522),(973,520),(933,530),(940,575),(940,600),(955,630),(995,635),(1010,620),(1010,595),(1025,570),(1015,542),(995,522)],
    'hand_b_left': [(585,522),(607,520),(647,530),(640,575),(640,600),(625,630),(585,635),(570,620),(570,595),(555,570),(565,542),(585,522)],
    'hand_l': [(485,522),(460,520),(415,530),(430,575),(430,600),(445,630),(485,635),(500,620),(500,595),(515,570),(505,542),(485,522)],
    'hand_r': [(75,522),(100,520),(145,530),(130,575),(130,600),(115,630),(75,635),(60,620),(60,595),(45,570),(55,542),(75,522)],
    # TODO: Add other body parts with their polygon coordinates
}

# Define groups: symmetric front/back regions share one label
region_groups = {
    'shoulder_left': ['shoulder_left', 'shoulder_b_left'],
    'shoulder_right': ['shoulder_right', 'shoulder_b_right'],
    'head': ['head', 'head_back'],
    'neck': ['neck', 'neck_b_right', 'neck_b_left'],
    'arm_left': ['arm_left', 'arm_b_left'],
    'arm_right': ['arm_right', 'arm_b_right'],
    'elbow_left': ['elbow_left', 'elbow_b_left'],
    'elbow_right': ['elbow_right', 'elbow_b_right'],
    'forearm_left': ['forearm_left', 'forearm_b_left'],
    'forearm_right': ['forearm_right', 'forearm_b_right'],
    'chest_left': ['chest_left', 'chest_b_left'],
    'chest_right': ['chest_right', 'chest_b_right'],
    'pelvis_left': ['pelvis_left', 'pelvis_b_left'],
    'pelvis_right': ['pelvis_right', 'pelvis_b_right'],
    'thigh_left': ['thigh_left', 'thigh_b_left'],
    'thigh_right': ['thigh_right', 'thigh_b_right'],
    'knee_left': ['knee_left', 'knee_b_left'],
    'knee_right': ['knee_right', 'knee_b_right'],
    'calf_left': ['calf_left', 'calf_b_left'],
    'calf_right': ['calf_right', 'calf_b_right'],
    'ankle_left': ['ankle_left', 'ankle_b_left'],
    'ankle_right': ['ankle_right', 'ankle_b_right'],
    'feet_left': ['feet_left', 'feet_b_left'],
    'feet_right': ['feet_right', 'feet_b_right'],
    'wrist_left': ['wrist_l', 'wrist_b_left'],
    'wrist_right': ['wrist_r', 'wrist_b_right'],
    'hand_left': ['hand_l', 'hand_b_left'],
    'hand_right': ['hand_r', 'hand_b_right'],
    # TODO: add other symmetric groups
}
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
        self.current_annotations = set()
        self.annotation_items = {}  # track canvas items per label
        self.undo_stack = []
        self.redo_stack = []

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
        # bind undo/redo
        self.master.bind("<Control-z>", self.undo)
        self.master.bind("<Control-y>", self.redo)

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
                # map region to canonical label
                label = region_to_group.get(region, region)
                # toggle: if already selected, deselect
                if label in self.current_annotations:
                    # remove highlights
                    for iid in self.annotation_items.pop(label, []):
                        self.canvas.delete(iid)
                    # remove from annotations set
                    self.current_annotations.discard(label)
                    # remove from listbox
                    items = list(self.listbox.get(0, tk.END))
                    if label in items:
                        idx = items.index(label)
                        self.listbox.delete(idx)
                    return
                # highlight all associated regions
                item_ids = []
                for r in region_groups.get(label, [label]):
                    pts = self.scaled_regions.get(r)
                    if not pts: continue
                    flat = [coord for pt in pts for coord in pt]
                    iid = self.canvas.create_polygon(flat, outline='red', fill='#B76E79', width=2, splinesteps=20)
                    item_ids.append(iid)
                self.annotation_items[label] = item_ids
                self.current_annotations.add(label)
                # record action for undo
                self.undo_stack.append(('add', label))
                self.redo_stack.clear()
                # update listbox
                self.listbox.insert(tk.END, label)
                break

    def save_annotations(self, event=None):
        case_no = self.case_entry.get().strip()
        if not case_no:
            messagebox.showwarning("Input required", "Please enter case number.")
            return
        self.annotations[case_no] = list(self.current_annotations)
        with open('annotations.json', 'w') as f:
            json.dump(self.annotations, f, indent=2)
        messagebox.showinfo("Saved", f"Annotations saved for case {case_no}.")

    def new_case(self, event=None):
        self.current_annotations.clear()
        self.canvas.delete("all")
        self.load_image()
        self.case_entry.delete(0, tk.END)
        # clear annotation listbox
        self.listbox.delete(0, tk.END)
        # reset undo/redo
        self.undo_stack.clear()
        self.redo_stack.clear()
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
        action, label = self.undo_stack.pop()
        if action == 'add':
            # remove highlights
            for iid in self.annotation_items.pop(label, []):
                self.canvas.delete(iid)
            # remove annotation
            self.current_annotations.discard(label)
            # remove from listbox
            items = list(self.listbox.get(0, tk.END))
            if label in items:
                idx = items.index(label)
                self.listbox.delete(idx)
            # record for redo
            self.redo_stack.append(('add', label))

    def redo(self, event=None):
        if not self.redo_stack:
            return
        action, label = self.redo_stack.pop()
        if action == 'add':
            # re-add highlights
            item_ids = []
            for r in region_groups.get(label, [label]):
                pts = body_regions.get(r)
                if not pts: continue
                flat = [coord for pt in pts for coord in pt]
                iid = self.canvas.create_polygon(flat, outline='red', fill='', width=2)
                item_ids.append(iid)
            self.annotation_items[label] = item_ids
            self.current_annotations.add(label)
            self.listbox.insert(tk.END, label)
            self.undo_stack.append(('add', label))

if __name__ == '__main__':
    root = tk.Tk()
    app = AnatoLabel(root)
    root.mainloop()

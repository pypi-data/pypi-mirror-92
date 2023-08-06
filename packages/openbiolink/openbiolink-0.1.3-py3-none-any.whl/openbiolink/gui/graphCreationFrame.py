import tkinter as tk
from tkinter import messagebox, ttk

from openbiolink import utils
from openbiolink.graph_creation.metadata_db_file import DbMetadata
from openbiolink.graph_creation.metadata_edge.edgeOntoMetadata import EdgeOntoMetadata
from openbiolink.graph_creation.metadata_edge.edgeRegularMetadata import EdgeRegularMetadata
from openbiolink.gui import gui as gui


class GraphCreationFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.info_text = ""
        self.db_cls_list = [x for x in utils.get_leaf_subclasses(DbMetadata)]
        self.edge_metadata_cls_list = [x for x in utils.get_leaf_subclasses(EdgeRegularMetadata)] + [
            x for x in utils.get_leaf_subclasses(EdgeOntoMetadata)
        ]
        self.db_cls_list.sort(key=lambda x: x.NAME)
        self.edge_metadata_cls_list.sort(key=lambda x: x.NAME)
        self.selected_dbs = None
        self.selected_meta_edges = None

        titles_panel = tk.Frame(self)
        self.info = tk.Button(titles_panel, text=" help ", command=lambda: gui.show_info_box(self.info_text))
        self.title = tk.Label(titles_panel, text="(1) Graph Creation", font=controller.title_font)

        self.actions_el = self._create_action_el(self)
        select_panel = tk.Frame(self)
        self.select_el = self._create_select_db_meta_edges_el(select_panel)

        options_panel = tk.Frame(self)
        self.graph_prop_el = self._create_graph_prop_el(options_panel)
        self.output_format_el = self._create_output_format_el(options_panel)

        buttons_panel = tk.Frame(self)
        next_button = tk.Button(buttons_panel, text="Next", command=lambda: self.next_page(), height=1, width=15)
        prev_button = tk.Button(
            buttons_panel, text="Back", command=lambda: self.controller.show_previous_frame(), height=1, width=15
        )

        titles_panel.pack(side="top", fill="x", pady=10)
        self.title.pack(side="left", pady=10, padx=15)
        self.info.pack(side="right", fill="x", pady=5, padx=15)
        self.actions_el.pack(side="top", fill="both", padx=15, pady=5, expand=True)
        select_panel.pack(side="top", fill="both", padx=10, pady=5, expand=True)
        self.select_el.pack(side="top", fill="both", padx=5, pady=10, expand=True)
        options_panel.pack(side="top", fill="both", padx=5, pady=5, expand=True)
        self.graph_prop_el.pack(side="left", fill="both", padx=10, expand=True)
        self.output_format_el.pack(side="left", fill="both", padx=10, expand=True)

        ttk.Separator(self, orient="horizontal").pack(side="top", fill="x", pady=(15, 0), padx=10, anchor="s")
        buttons_panel.pack(side="bottom", padx=15, fill="x")
        prev_button.pack(side="left", anchor="w", pady=(5, 10))
        next_button.pack(side="right", anchor="e", pady=(5, 10))

    def _create_action_el(self, parent):
        el = tk.LabelFrame(parent, text="Actions")
        self.download = tk.BooleanVar(value=True)
        dl_box = tk.Checkbutton(el, text="perform download", variable=self.download)
        self.create_infiles = tk.BooleanVar(value=True)
        create_in_box = tk.Checkbutton(el, text="create infiles", variable=self.create_infiles)
        self.create_graph = tk.BooleanVar(value=True)
        create_graph_box = tk.Checkbutton(
            el, text="create graph", variable=self.create_graph, command=self.toggl_cg_elements
        )
        dl_box.pack(side="left", padx=5, anchor="w")
        create_in_box.pack(side="left", padx=5, anchor="w")
        create_graph_box.pack(side="left", padx=5, anchor="w")
        return el

    def _create_select_db_meta_edges_el(self, parent):
        el = tk.LabelFrame(parent, text="Customize Graph")
        self.select_choices = ["Default Graph", "Use only subset of Source Databases", "Use only subset of Meta edges"]
        self.select = tk.StringVar(value=self.select_choices[0])
        select_menu = tk.OptionMenu(el, self.select, *self.select_choices, command=self.toggl_select_buttons)
        select_menu.config(width=32)
        self.select_db_button = tk.Button(el, text="select data bases...", command=self.select_dbs_popup)
        self.select_meta_edge_button = tk.Button(el, text="select meta edges...", command=self.select_mes_popup)
        select_menu.pack(side="left", padx=5, anchor="w")
        return el

    def select_dbs_popup(self):
        select_popup = tk.Toplevel()
        select_popup.wm_title("Select Source Databases")
        select_popup.wm_geometry("400x400")
        label = tk.Label(select_popup, text="Data Base Type - Data Base - Data Base File")
        filterPanel = tk.Frame(select_popup)
        select_all_button = tk.Button(filterPanel, text="select all", command=self.select_all_dbs)
        select_none_button = tk.Button(filterPanel, text="select none", command=self.unselect_all_dbs)
        frame = tk.Frame(select_popup)
        scrollbar = tk.Scrollbar(frame)
        self.db_selection = tk.Listbox(frame, selectmode="multiple", exportselection=0, yscrollcommand=scrollbar.set)
        for i, source_db_cls in enumerate(self.db_cls_list):
            self.db_selection.insert(i, source_db_cls.NAME)
            if source_db_cls in self.selected_dbs:
                self.db_selection.selection_set(i)

        scrollbar.config(command=self.db_selection.yview)
        ok_button = ttk.Button(select_popup, text="Okay", command=lambda: self.safe_select_dbs_and_quit(select_popup))

        label.pack(side="top", anchor="w", pady=10, padx=5)
        filterPanel.pack(side="top")
        select_all_button.pack(side="left")
        select_none_button.pack(side="left")
        frame.pack(side="top", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.db_selection.pack(fill="both", padx=10, expand=True)
        ok_button.pack(side="bottom")

    def select_all_dbs(self):
        for i, _ in enumerate(self.db_cls_list):
            self.db_selection.selection_set(i)

    def unselect_all_dbs(self):
        self.db_selection.selection_clear(0, len(self.db_cls_list) - 1)

    def safe_select_dbs_and_quit(self, pop_up):
        self.selected_dbs = [self.db_cls_list[i] for i in self.db_selection.curselection()]
        pop_up.destroy()

    def select_mes_popup(self):
        select_popup = tk.Toplevel()
        select_popup.wm_title("Select Meta Edges")
        select_popup.wm_geometry("400x400")
        label = tk.Label(select_popup, text="Connection Type - Meta Edge Type")
        filterPanel = tk.Frame(select_popup)
        select_all_button = tk.Button(filterPanel, text="select all", command=self.select_all_mes)
        select_none_button = tk.Button(filterPanel, text="select none", command=self.unselect_all_mes)
        frame = tk.Frame(select_popup)
        scrollbar = tk.Scrollbar(frame)

        self.me_selection = tk.Listbox(frame, selectmode="multiple", exportselection=0, yscrollcommand=scrollbar.set)
        for i, source_me_cls in enumerate(self.edge_metadata_cls_list):
            self.me_selection.insert(i, source_me_cls.NAME)
            if source_me_cls in self.selected_meta_edges:
                self.me_selection.selection_set(i)
        scrollbar.config(command=self.me_selection.yview)
        ok_button = ttk.Button(select_popup, text="Okay", command=lambda: self.safe_select_mes_and_quit(select_popup))

        label.pack(side="top", anchor="w", pady=10, padx=5)
        filterPanel.pack(side="top")
        select_all_button.pack(side="left")
        select_none_button.pack(side="left")
        frame.pack(side="top", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.me_selection.pack(fill="both", padx=10, expand=True)
        ok_button.pack(side="bottom")

    def safe_select_mes_and_quit(self, pop_up):
        self.selected_meta_edges = [self.edge_metadata_cls_list[i] for i in self.me_selection.curselection()]
        pop_up.destroy()

    def select_all_mes(self):
        for i, _ in enumerate(self.edge_metadata_cls_list):
            self.me_selection.selection_set(i)

    def unselect_all_mes(self):
        self.me_selection.selection_clear(0, len(self.edge_metadata_cls_list) - 1)

    def toggl_select_buttons(self, select_choice):
        if select_choice == self.select_choices[0]:
            self.selected_dbs = None
            self.selected_meta_edges = None
            self.select_db_button.pack_forget()
            self.select_meta_edge_button.pack_forget()
        elif select_choice == self.select_choices[1]:
            self.selected_dbs = self.db_cls_list.copy()
            self.selected_meta_edges = None
            self.select_db_button.pack(side="right", padx=5, anchor="w")
            self.select_meta_edge_button.pack_forget()
            self.select_dbs_popup()
        elif select_choice == self.select_choices[2]:
            self.selected_dbs = None
            self.selected_meta_edges = self.edge_metadata_cls_list.copy()
            self.select_db_button.pack_forget()
            self.select_meta_edge_button.pack(side="right", padx=5, anchor="w")
            self.select_mes_popup()

    def _create_graph_prop_el(self, parent):
        el = tk.LabelFrame(parent, text="Graph Properties")
        # quality
        self.qual = tk.StringVar(value="hq")
        hq_box = tk.Radiobutton(el, text="high quality", variable=self.qual, value="hq")
        mq_box = tk.Radiobutton(el, text="medium quality", variable=self.qual, value="mq")
        lq_box = tk.Radiobutton(el, text="low quality", variable=self.qual, value="lq")
        none_box = tk.Radiobutton(el, text="no quality cutoff", variable=self.qual, value="nq")
        # undirected
        self.undir = tk.BooleanVar()
        undirected_box = tk.Radiobutton(el, text="undirected", variable=self.undir, value=True)
        directed_box = tk.Radiobutton(el, text="directed", variable=self.undir, value=False)
        # packing
        none_box.pack(side="top", padx=5, anchor="w")
        hq_box.pack(side="top", padx=5, anchor="w")
        mq_box.pack(side="top", padx=5, anchor="w")
        lq_box.pack(side="top", padx=5, anchor="w")
        ttk.Separator(el, orient="horizontal").pack(side="top", fill="x", pady=2, padx=5, anchor="w")
        directed_box.pack(side="top", pady=2, padx=5, anchor="w")
        undirected_box.pack(side="top", pady=2, padx=5, anchor="w")
        return el

    def _create_output_format_el(self, parent):
        el = tk.LabelFrame(parent, text="Output Format")

        # output format selection
        format_selection = tk.Frame(el)
        choices = {"TSV", "RDF-N3", "PICKLE", "BEL"}
        self.format = tk.StringVar(format_selection)
        self.format.set("TSV")

        def change_dropdown(*args):
            fmt = self.format.get()
            if fmt == "TSV":
                forget_packing()
                self.single_sep = tk.StringVar(value=None)
                self.multi_sep = tk.StringVar(value=None)
                # packing
                separator1.pack(side="top", fill="x", pady=5, padx=5, anchor="w")
                single_out_file_box.pack(side="top", padx=5, anchor="w")
                multi_out_file_box.pack(side="top", padx=5, anchor="w")
                separator2.pack(side="top", fill="x", pady=5, padx=5, anchor="w")
                sep_frame.pack(side="top", padx=5, anchor="w")
                sep_label.pack(side="left", padx=5, anchor="w")
                sep_value.pack(side="left", anchor="w")
                sep_info.pack(side="left", anchor="w")
                no_qscore_box.pack(side="top", padx=5, anchor="w")
            elif fmt in ["RDF-N3", "PICKLE", "BEL"]:
                forget_packing()
                self.single_sep = tk.StringVar(value=None)
                self.multi_sep = tk.StringVar(value=None)
                # packing
                warning.pack(side="top", fill="x", pady=5, padx=5, anchor="w")
                separator1.pack(side="top", fill="x", pady=5, padx=5, anchor="w")
                single_out_file_box.pack(side="top", padx=5, anchor="w")
                multi_out_file_box.pack(side="top", padx=5, anchor="w")
                separator2.pack(side="top", fill="x", pady=5, padx=5, anchor="w")
                no_qscore_box.pack(side="top", padx=5, anchor="w")
            else:
                raise ValueError(f"Invalid format: {fmt}")

        self.format.trace("w", change_dropdown)
        format_selector_label = tk.Label(format_selection, text="Format:")
        format_selector = tk.OptionMenu(format_selection, self.format, *choices)

        def forget_packing():
            warning.pack_forget()
            separator1.pack_forget()
            single_out_file_box.pack_forget()
            multi_out_file_box.pack_forget()
            separator2.pack_forget()
            sep_frame.pack_forget()
            sep_label.pack_forget()
            sep_value.pack_forget()
            sep_info.pack_forget()
            no_qscore_box.pack_forget()

        self.output_file_cardinality = tk.IntVar(value=1)
        single_out_file_box = tk.Radiobutton(el, text="single file", variable=self.output_file_cardinality, value=1)
        multi_out_file_box = tk.Radiobutton(
            el, text="multiple files (one/type)", variable=self.output_file_cardinality, value=2
        )

        # seperator of file/s
        self.sep = tk.StringVar(value=None)
        sep_frame = tk.Frame(el)
        sep_label = tk.Label(sep_frame, text="separator:")
        sep_info = tk.Label(sep_frame, text="Defaults to tab.", font=self.controller.info_font)
        sep_value = tk.Entry(sep_frame, textvariable=self.sep, width=5)

        # qscore
        self.no_qscore = tk.BooleanVar(value=False)
        no_qscore_box = tk.Checkbutton(el, text="without quality score", variable=self.no_qscore)

        separator1 = ttk.Separator(el, orient="horizontal")
        separator2 = ttk.Separator(el, orient="horizontal")

        warning = tk.Label(
            el,
            text="Warning, currently only N3 graph creation is supported.\n You can not perform a split or evaluation.",
        )

        # packing
        format_selection.pack(side="top", padx=5, anchor="w")
        format_selector_label.pack(side="left", padx=5, anchor="w")
        format_selector.pack(side="left", padx=5, anchor="w")
        change_dropdown(None)
        return el

    def toggl_cg_elements(self):
        if self.graph_prop_el.winfo_ismapped():
            self.select_el.pack_forget()
            self.graph_prop_el.pack_forget()
            self.output_format_el.pack_forget()
        else:
            self.select_el.pack(side="top", fill="both", padx=5, expand=True)
            self.graph_prop_el.pack(side="left", fill="both", padx=10, expand=True)
            self.output_format_el.pack(side="left", fill="both", padx=10, expand=True)

    def next_page(self):
        self.controller.ARGS_LIST_GRAPH_CREATION = []
        if self.format == "TSV":
            if self.sep.get() == "":
                messagebox.showerror("ERROR", "Please provide a separator for desired output file")
                return
        self.controller.ARGS_LIST_GRAPH_CREATION.append("generate")
        if self.format.get() != "TSV":
            self.controller.ARGS_LIST_GRAPH_CREATION.extend(["--output-format", self.format.get()])
        if self.undir.get():
            self.controller.ARGS_LIST_GRAPH_CREATION.append("--undirected")
        if self.qual.get() != "hq":
            self.controller.ARGS_LIST_GRAPH_CREATION.extend(["--qual", self.qual.get()])
        if not self.download.get():
            self.controller.ARGS_LIST_GRAPH_CREATION.append("--no-download")
        if not self.create_infiles.get():
            self.controller.ARGS_LIST_GRAPH_CREATION.append("--no-input")
        if not self.create_graph.get():
            self.controller.ARGS_LIST_GRAPH_CREATION.append("--no-create")
        if self.output_file_cardinality.get() == 2:
            self.controller.ARGS_LIST_GRAPH_CREATION.append("--output-multi-file")
        if self.sep.get():
            self.controller.ARGS_LIST_GRAPH_CREATION.extend(["--output-sep", self.sep.get()])
        if self.no_qscore.get():
            self.controller.ARGS_LIST_GRAPH_CREATION.append("--no-qscore")
        if self.selected_dbs:
            for x in self.selected_dbs:
                self.controller.ARGS_LIST_GRAPH_CREATION.extend(["--dbs", x.__module__ + "." + x.__name__])
        if self.selected_meta_edges:
            for x in self.selected_meta_edges:
                self.controller.ARGS_LIST_GRAPH_CREATION.extend(["--mes", x.__module__ + "." + x.__name__])

        self.controller.show_next_frame()

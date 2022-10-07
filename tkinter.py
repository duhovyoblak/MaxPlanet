     

 

 


        self.over_bar_state_txt.grid(row = 1, column = 0, sticky='we')

 


 

    #--------------------------------------------------------------------------

    def setStrState(self, value):

       

        self.str_state.set(value)

       

        if   self.str_state.get() == 'ON'      : self.over_bar_state_txt.configure( background = 'lightgreen')

        elif self.str_state.get() == 'WORKING' : self.over_bar_state_txt.configure( background = 'yellow'    )

        elif self.str_state.get() == 'SHUTDOWN': self.over_bar_state_txt.configure( background = 'orange'    )

        elif self.str_state.get() == 'OFF'     : self.over_bar_state_txt.configure( background = 'red'       )

        else                                   : self.over_bar_state_txt.configure( background = 'blue'      )

        

    #--------------------------------------------------------------------------

    def state_menu(self, event):

 

       

    #--------------------------------------------------------------------------

    def stateOn(self):

       

        resp = dwm_api.mode_start(self.url, self.user)

        self.status(f"{resp['msg']}")

        self.tabMonRefresh()

   



#==========================================================================

    # Tab Monitor

        #----------------------------------------------------------------------

        # Lavy stlpec - TreeView

        #----------------------------------------------------------------------

        self.tree_mon = ttk.Treeview(frm)

        self.tree_mon.heading('#0', text='Monitor2', anchor='w')

       

        # Pridam scrollbar Y

       yscrl = ttk.Scrollbar(frm, orient=tk.VERTICAL, command=self.tree_mon.yview)

        self.tree_mon.configure(yscroll=yscrl.set)

        yscrl.grid(row=0, column=0, rowspan=9, sticky='nse')

 

        # Zobrazim treeview

        self.tree_mon.grid(row=0, column=0, rowspan=9, sticky='nswe')

       

        #----------------------------------------------------------------------

        # Pravy stlpec

        #----------------------------------------------------------------------

        # Button debug

        self.str_debug = tk.StringVar(value=1)

        spin_debug = ttk.Spinbox(frm, from_=0, to=7, textvariable=self.str_debug, wrap=True, width=5)

        spin_debug.grid(row=0, column=7)

 

        btn_debug = ttk.Button(frm, text='Set DEBUG', command=self.setDebug)

        btn_debug.grid(row=0, column=9, sticky='we')

       

        #----------------------------------------------------------------------

        # Button import

        btn_import = ttk.Button(frm, text='Import metadata', command=self.metaImport)

        btn_import.grid(row=2, column=9, sticky='we')

       

        #----------------------------------------------------------------------

        # Spolocne parametre last, next days

        #----------------------------------------------------------------------

        lf = ttk.LabelFrame(frm, text='Common parameters')

        lf.grid(row=3, rowspan=6, column=2, columnspan=7, sticky='wens', pady=20, padx=20)

       

        lf.columnconfigure(0, weight=4)

        lf.columnconfigure(1, weight=1)

        lf.columnconfigure(2, weight=1)

        lf.columnconfigure(3, weight=1)

        lf.columnconfigure(4, weight=4)

        lf.rowconfigure   (0, weight=1)

 

        lbl_last = ttk.Label(lf, relief=tk.FLAT, text='For last' )

        lbl_last.grid(row=0, column=0, sticky='e')

 

        self.str_last = tk.StringVar(value=5)

        spin_last = ttk.Spinbox(lf, from_=1, to=600, textvariable=self.str_last, wrap=True, width=5)

        spin_last.grid(row=0, column=1)

 

        lbl_next = ttk.Label(lf, relief=tk.FLAT, text='days and for next' )

        lbl_next.grid(row=0, column=2)

 

        self.str_next = tk.StringVar(value=2)

        str_next = ttk.Spinbox(lf, from_=1, to=30, textvariable=self.str_next, wrap=True, width=5)

        str_next.grid(row=0, column=3)

 

        lbl_next2 = ttk.Label(lf, relief=tk.FLAT, text='days' )

        lbl_next2.grid(row=0, column=4, sticky='w')

 

        #----------------------------------------------------------------------

        # Button migrate

        btn_migrate = ttk.Button(frm, text='Migrate metadata', command=self.metaMigrate)

        btn_migrate.grid(row=3, column=9, sticky='we')

       

        #----------------------------------------------------------------------

        # Button load metadata

        btn_load = ttk.Button(frm, text='Re/Load metadata', command=self.metaLoad)

        btn_load.grid(row=4, column=9, sticky='we')

       

        #----------------------------------------------------------------------

        # Button end forced etl

        btn_end_forced = ttk.Button(frm, text='End forced ETLs', command=self.endForced)

        btn_end_forced.grid(row=5, column=9, sticky='we')

       

        #----------------------------------------------------------------------

        # Button end orphaned etl

        btn_end_orph_etl = ttk.Button(frm, text='End orphaned ETLs', command=self.endOrphaned)

        btn_end_orph_etl.grid(row=6, column=9, sticky='we')

       

        #----------------------------------------------------------------------

        # Button end orphaned step

        btn_end_orph_step = ttk.Button(frm, text='End orphaned steps', command=self.endSteps)

        btn_end_orph_step.grid(row=7, column=9, sticky='we')

       

        #----------------------------------------------------------------------

        # Recovery etls

        btn_recovery = ttk.Button(frm, text='Recovery ETLs', command=self.recovery)

        btn_recovery.grid(row=8, column=9, sticky='we')

 

        self.tabMonRefresh()

 

    #--------------------------------------------------------------------------

    def setDebug(self):

       

        resp = dwm_api.admin_debug(self.url, self.user, self.str_debug.get())

        self.status(f"{resp['msg']}")

        self.refresh()

 

    #--------------------------------------------------------------------------

    def metaMigrate(self):

       

        resp = dwm_api.admin_migrate(self.url, self.user,  days=self.str_last.get(), delInt=1)

        self.status(f"{resp['msg']}")

        self.refresh()

 

    #--------------------------------------------------------------------------

    def metaImport(self):

       



    #--------------------------------------------------------------------------

    def metaLoad(self):

       

        resp = dwm_api.admin_load(self.url, self.user,  days=self.str_last.get())

        self.status(f"{resp['msg']}")

        self.refresh()

 

    #--------------------------------------------------------------------------

    def endForced(self):

       

        resp = dwm_api.admin_end_forced(self.url, self.user)

        self.status(f"{resp['msg']}")

        self.refresh()

 

    #--------------------------------------------------------------------------

    def endOrphaned(self):

       

        resp = dwm_api.admin_end_orphans(self.url, self.user)

        self.status(f"{resp['msg']}")

        self.refresh()

 

    #--------------------------------------------------------------------------

    def endSteps(self):

       

        resp = dwm_api.admin_end_steps(self.url, self.user)

        self.status(f"{resp['msg']}")

        self.refresh()

 

    #--------------------------------------------------------------------------

    def recovery(self):

       

        resp = dwm_api.admin_recovery(self.url, self.user, last=self.str_last.get(), nxt=self.str_next.get())

        self.status(f"{resp['msg']}")

        self.refresh()

 

    #--------------------------------------------------------------------------

    def tabMonRefresh(self):

       

        #----------------------------------------------------------------------

        # treeView

        #----------------------------------------------------------------------

        self.treeClear(self.tree_mon)

        info = dwm_api.mon_info(self.url)

        self.datToTree(info['dat'], self.tree_mon)

       

        #----------------------------------------------------------------------

        # Status labels

        #----------------------------------------------------------------------

        self.setStrState( info['dat']['config']['state'] )

        self.setStrMode ( info['dat']['config']['mode' ] )

 



#==========================================================================

    # Tab Services

    #--------------------------------------------------------------------------

    def tabSrvShow(self):

       

        #----------------------------------------------------------------------

        # Vytvorim frame a skonfigurujem grid

        #----------------------------------------------------------------------

        frm = ttk.Frame(self.tabs)

        frm.columnconfigure(0, weight=10)

        frm.columnconfigure(1, weight=1)

        frm.columnconfigure(2, weight=1)

        frm.columnconfigure(3, weight=1)

        frm.columnconfigure(4, weight=1)

       

        frm.rowconfigure   (0, weight=1)

        frm.rowconfigure   (1, weight=1)

        frm.rowconfigure   (2, weight=1)

        frm.rowconfigure   (3, weight=5)

        frm.rowconfigure   (4, weight=5)

 

        # Vlozim frame do Tabs       

        self.tabs.add(frm,    text='Services'   )

 

        #----------------------------------------------------------------------

        # Lavy stlpec - TreeView

        #----------------------------------------------------------------------

        self.tree_srv = ttk.Treeview(frm)

        self.tree_srv.heading('#0', text='Services', anchor='w')

       

        # Pridam scrollbar Y

        yscrl = ttk.Scrollbar(frm, orient=tk.VERTICAL, command=self.tree_srv.yview)

        self.tree_srv.configure(yscroll=yscrl.set)

        yscrl.grid(row=0, column=0, rowspan=5, sticky='nse')

 

        # Zobrazim treeview

        self.tree_srv.grid(row=0, column=0, rowspan=5, sticky='nswe')

       

        #----------------------------------------------------------------------

        # Pravy stlpec

        #----------------------------------------------------------------------

        self.str_srv = tk.StringVar()

 

        self.cb_srv  = ttk.Combobox(frm, textvariable=self.str_srv, width=20)

        self.cb_srv.grid(row=1, column=2)

 

        #----------------------------------------------------------------------

        # Btn Service stop

        btn_srv_stop = ttk.Button(frm, text='Service stop', command=self.srvStop)

        btn_srv_stop.grid(row=0, column=3, sticky='wes')

       

        #----------------------------------------------------------------------

        # Btn Service start

        btn_srv_start = ttk.Button(frm, text='Service start', command=self.srvStart)

        btn_srv_start.grid(row=2, column=3, sticky='wen')

 

        self.tabSrvRefresh()

 

    #--------------------------------------------------------------------------

    def srvStop(self):

       

        self.str_status_bar.set(f'I will stop service {self.str_srv.get()}')

 

    #--------------------------------------------------------------------------

    def srvStart(self):

       

        self.str_status_bar.set(f'I will start service {self.str_srv.get()}')

 

    #--------------------------------------------------------------------------

    def tabSrvRefresh(self):

       

        #----------------------------------------------------------------------

        # treeView

        #----------------------------------------------------------------------

        self.treeClear(self.tree_srv)

        info = dwm_api.srv_info(self.url)

        self.datToTree(info['dat'], self.tree_srv)

       

        #----------------------------------------------------------------------

        # combo box

        #----------------------------------------------------------------------

        self.cb_srv['values'] = list(info['dat'].keys())

        self.cb_srv.set(self.cb_srv['values'][0])

       

    #==========================================================================

    # Tab Connections

    #--------------------------------------------------------------------------

    def tabConShow(self):

       

        #----------------------------------------------------------------------

        # Vytvorim frame a skonfigurujem grid

        #----------------------------------------------------------------------

        frm = ttk.Frame(self.tabs)

        frm.columnconfigure(0, weight=10)

        frm.columnconfigure(1, weight=1)

        frm.columnconfigure(2, weight=1)

        frm.columnconfigure(3, weight=1)

        frm.columnconfigure(4, weight=1)

       

        frm.rowconfigure   (0, weight=1)

        frm.rowconfigure   (1, weight=1)

        frm.rowconfigure   (2, weight=1)

        frm.rowconfigure   (3, weight=5)

        frm.rowconfigure   (4, weight=5)

 

        # Vlozim frame do Tabs       

        self.tabs.add(frm,    text='Conections'   )

 

        #----------------------------------------------------------------------

        # Lavy stlpec - TreeView

        #----------------------------------------------------------------------

        self.tree_con = ttk.Treeview(frm)

        self.tree_con.heading('#0', text='Conections', anchor='w')

       

        # Pridam scrollbar Y

        yscrl = ttk.Scrollbar(frm, orient=tk.VERTICAL, command=self.tree_con.yview)

        self.tree_con.configure(yscroll=yscrl.set)

        yscrl.grid(row=0, column=0, rowspan=5, sticky='nse')

 

        # Zobrazim treeview

        self.tree_con.grid(row=0, column=0, rowspan=5, sticky='nswe')

       

        #----------------------------------------------------------------------

        # Pravy stlpec

        #----------------------------------------------------------------------

        self.tabConRefresh()

 

    #--------------------------------------------------------------------------

    def tabConRefresh(self):

       

        #----------------------------------------------------------------------

        # treeView

        #----------------------------------------------------------------------

        self.treeClear(self.tree_con)

        info = dwm_api.con_info(self.url)

        self.datToTree(info['dat'], self.tree_con)

       

 

 

 


 





 

 
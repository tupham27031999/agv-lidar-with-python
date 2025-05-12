
def tach_du_lieu(input):
    name_1 = ""
    name_2 = ""
    next_name = 0
    for i in list(input):
        if next_name == 1:
            name_2 = name_2 + i
        if i == "_":
            next_name = 1
        if i == 0:
            name_1 = name_1 + i
    return name_1,name_2
def gan_du_lieu(number):
    list_out = []
    for i in range(0,number):
        list_out.append("NA")
    return list_out
class edit_root:
    def __init__(self):
        self.name_root = "NA"
        self.w = "NA"
        self.h = "NA"
        self.x = "NA"
        self.y = "NA"
        self.bg = "NA"
        self.columnconfigure = "NA"
        self.rowconfigure = "NA"
        self.title = "NA"
        self.value_close = "NA"
        self.new_root = 1
        self.geometry = "NA"
        self.thuoc_frame = "NA"
        
        if str(self.x) != "" and str(self.y) != "":
            self.geometry = str(self.w) + "x" + str(self.h) +"+"+str(self.x)+"+"+str(self.y)
        else:
            self.geometry = str(self.w) + "x" + str(self.h)
        self.dic_root = {"name window":self.name_root,"w":self.w,"h":self.h,"x":self.x,"y":self.y,"geometry":self.geometry,"bg":self.bg
                         ,"columnconfigure":self.columnconfigure,"rowconfigure":self.rowconfigure,"title":self.title,"protocol":self.value_close,"new root":self.new_root,
                         "thuoc frame":self.thuoc_frame}
        
        self.tt_root = [["thuoc_frame",self.dic_root["thuoc frame"]],["geometry",self.dic_root["geometry"]],["bg",self.dic_root["bg"]],["columnconfigure",self.dic_root["columnconfigure"]]
                        ,["rowconfigure",self.dic_root["rowconfigure"]],["title",self.dic_root["title"]],["protocol",self.dic_root["protocol"]]
                        ,["new_root",self.dic_root["new root"]]]
    def update_value(self,name="NA",value = "NA"): # input = "name_value"
        if value != "NA":
            try:
                if name == "columnconfigure" and value != "NA":
                    try:
                        value_new = []
                        ds_value = str(value).split("_")
                        for i in range(0,len(ds_value)):
                            value_new.append(int(ds_value[i]))
                        self.dic_root[name] = value_new
                    except:
                        print("sai fomat root[columnconfigure] "+ str(value))
                if name == "rowconfigure" and value != "NA":
                    try:
                        value_new = []
                        ds_value = str(value).split("_")
                        for i in range(0,len(ds_value)):
                            value_new.append(int(ds_value[i]))
                        self.dic_root[name] = value_new
                    except:
                        print("sai fomat root[columnconfigure] "+ str(value))
                if (name != "columnconfigure" and name != "rowconfigure") or value == "NA":
                    self.dic_root[name] = value
                if str(self.dic_root["x"]) != "NA" and str(self.dic_root["y"]) != "NA":
                    self.geometry = str(self.dic_root["w"]) + "x" + str(self.dic_root["h"]) +"+"+str(self.dic_root["x"])+"+"+str(self.dic_root["y"])
                else:
                    if str(self.dic_root["w"]) != "NA" and str(self.dic_root["h"]) != "NA":
                        self.geometry = str(self.dic_root["w"]) + "x" + str(self.dic_root["h"])
                self.dic_root["geometry"] = self.geometry
            except:
                print("không tồn tại dữ liệu root "+ str(name))
        self.tt_root = [["thuoc_frame",self.dic_root["thuoc frame"]],["geometry",self.dic_root["geometry"]],["bg",self.dic_root["bg"]],["columnconfigure",self.dic_root["columnconfigure"]]
                        ,["rowconfigure",self.dic_root["rowconfigure"]],["title",self.dic_root["title"]],["protocol",self.dic_root["protocol"]]
                        ,["new_root",self.dic_root["new root"]]]
        return self.dic_root["name window"],self.tt_root
class menu:
    def __init__(self):
        self.name_window = "NA"
        self.thuoc_root = "NA"
        self.thuoc_frame = "NA"
        self.loai = "NA"
        self.value_cmd = "NA"
        self.new_item = "NA"
        self.add_const_value = "NA"
        self.text = "NA"
        self.font = "NA"
        self.dict = {"name window":self.name_window,"thuoc root":self.thuoc_root,"thuoc frame":self.thuoc_frame,"loai":self.loai,"value cmd":self.value_cmd
                     ,"new item":self.new_item,"add const value":self.add_const_value,"text":self.text}
        self.tt = [["name_window",self.dict["name window"]],["thuoc_root",self.dict["thuoc root"]],["thuoc_frame",self.dict["thuoc frame"]],["loai",self.dict["loai"]]
                   ,["value_cmd",self.dict["value cmd"]],["new_item",self.dict["new item"]],["add_const_value",self.dict["add const value"]],["text",self.dict["text"]]]
    def update_value(self,name="NA",value = "NA"): # input = "name_value"
        if value != "NA":
            try:
                self.dict[name] = value
            except:
                print("không tồn tại dữ liệu label "+ str(name))
        self.tt = [["name_window",self.dict["name window"]],["thuoc_root",self.dict["thuoc root"]],["thuoc_frame",self.dict["thuoc frame"]],["loai",self.dict["loai"]]
                   ,["value_cmd",self.dict["value cmd"]],["new_item",self.dict["new item"]],["add_const_value",self.dict["add const value"]],["text",self.dict["text"]]]
        return self.tt
class edit_label:
    def __init__(self):
        self.ten_label = "NA"
        self.thuoc_fame = "NA"
        self.font="NA"
        self.font_size="NA"
        self.net_chu="NA"
        self.column="NA"
        self.row="NA"
        self.ipadx="NA"
        self.ipady="NA"
        self.padx_gird="NA"
        self.pady_gird="NA"
        self.rowspan="NA"
        self.columnspan="NA"
        self.sticky="NA"
        self.activebackground="NA"
        self.activeforeground="NA"
        self.anchor="NA"
        self.background="NA"
        self.bd="NA"
        self.bg="NA"
        self.bitmap="NA"
        self.border="NA"
        self.borderwidth="NA"
        self.compound="NA"
        self.cursor="NA"
        self.disabledforeground="NA"
        self.fg="NA"
        self.foreground="NA"
        self.height="NA"
        self.highlightbackground="NA"
        self.highlightcolor="NA"
        self.highlightthickness="NA"
        self.image="NA"
        self.justify="NA"
        self.padx="NA"
        self.pady="NA"
        self.relief="NA"
        self.state="NA"
        self.takefocus="NA"
        self.text="NA"
        self.textvariable="NA"
        self.underline="NA"
        self.width="NA"
        self.wraplength="NA"
        self.dic_label = {"name window":self.ten_label,"thuoc frame":self.thuoc_fame,"font":self.font,"font size":self.font_size,"net chu":self.net_chu
                          ,"column":self.column,"row":self.row,"ipadx":self.ipadx,"ipady":self.ipady,"padx grid":self.padx_gird
                          ,"pady gird":self.pady_gird,"rowspan":self.rowspan,"columnspan":self.columnspan,"sticky":self.sticky
                          ,"activebackground":self.activebackground,"activeforeground":self.activeforeground,"anchor":self.anchor,"background":self.background
                          ,"bd":self.bd,"bg":self.bg,"bitmap":self.bitmap,"border":self.border,"borderwidth":self.borderwidth,"compound":self.compound
                          ,"cursor":self.cursor,"disabledforeground":self.disabledforeground,"fg":self.fg,"foreground":self.foreground,"height":self.height
                          ,"highlightbackground":self.highlightbackground,"highlightcolor":self.highlightcolor,"highlightthickness":self.highlightthickness
                          ,"image":self.image,"justify":self.justify,"padx":self.padx,"pady":self.pady,"relief":self.relief,"state":self.state
                          ,"takefocus":self.takefocus,"text":self.text,"textvariable":self.textvariable,"underline":self.underline,"width":self.width
                          ,"wraplength":self.wraplength}
        
        self.tt_label_1 = [["thuoc_frame",self.dic_label["thuoc frame"]],["font",self.dic_label["font"]],["font_size_int",self.dic_label["font size"]],["net_chu",self.dic_label["net chu"]]]
        self.tt_label_2 = [["column_int",self.dic_label["column"]],["row_int",self.dic_label["row"]],["ipadx_int",self.dic_label["ipadx"]],["ipady_int",self.dic_label["ipady"]]
                           ,["padx_grid_int",self.dic_label["padx grid"]],["pady_int",self.dic_label["pady gird"]],["rowspan_int",self.dic_label["rowspan"]]
                           ,["columnspan_int",self.dic_label["columnspan"]],["sticky",self.dic_label["sticky"]]]
        self.tt_label_3 = [["activebackground",self.dic_label["activebackground"]],["activeforeground",self.dic_label["activeforeground"]],["anchor",self.dic_label["anchor"]]
                           ,["background",self.dic_label["background"]],["bd",self.dic_label["bd"]],["bg",self.dic_label["bg"]],["bitmap",self.dic_label["bitmap"]]
                           ,["border",self.dic_label["border"]],["borderwidth_int",self.dic_label["borderwidth"]],["compound",self.dic_label["compound"]]
                           ,["cursor",self.dic_label["cursor"]],["disabledforeground",self.dic_label["disabledforeground"]],["fg",self.dic_label["fg"]]
                           ,["foreground",self.dic_label["foreground"]],["height",self.dic_label["height"]],["highlightbackground",self.dic_label["highlightbackground"]]
                           ,["highlightcolor",self.dic_label["highlightcolor"]],["highlightthickness",self.dic_label["highlightthickness"]]
                           ,["image",self.dic_label["image"]],["justify",self.dic_label["justify"]],["padx_int",self.dic_label["padx"]],["pady_int",self.dic_label["pady"]]
                           ,["relief",self.dic_label["relief"]],["state",self.dic_label["state"]],["takefocus_int",self.dic_label["takefocus"]],["text",self.dic_label["text"]]
                           ,["textvariable",self.dic_label["textvariable"]],["underline",self.dic_label["underline"]],["width_int",self.dic_label["width"]]
                           ,["wraplength_int",self.dic_label["wraplength"]]]
    def update_value(self,name="NA",value = "NA"): # input = "name_value"
        if value != "NA":
            try:
                self.dic_label[name] = value
            except:
                print("không tồn tại dữ liệu label "+ str(name))
        self.tt_label_1 = [["thuoc_frame",self.dic_label["thuoc frame"]],["font",self.dic_label["font"]],["font_size_int",self.dic_label["font size"]]
                            ,["net_chu",self.dic_label["net chu"]]]
        self.tt_label_2 = [["column_int",self.dic_label["column"]],["row_int",self.dic_label["row"]],["ipadx_int",self.dic_label["ipadx"]],["ipady_int",self.dic_label["ipady"]]
                        ,["padx_grid_int",self.dic_label["padx grid"]],["pady_int",self.dic_label["pady gird"]],["rowspan_int",self.dic_label["rowspan"]]
                        ,["columnspan_int",self.dic_label["columnspan"]],["sticky",self.dic_label["sticky"]]]
        self.tt_label_3 = [["activebackground",self.dic_label["activebackground"]],["activeforeground",self.dic_label["activeforeground"]],["anchor",self.dic_label["anchor"]]
                        ,["background",self.dic_label["background"]],["bd",self.dic_label["bd"]],["bg",self.dic_label["bg"]],["bitmap",self.dic_label["bitmap"]]
                        ,["border",self.dic_label["border"]],["borderwidth",self.dic_label["borderwidth"]],["compound",self.dic_label["compound"]]
                        ,["cursor",self.dic_label["cursor"]],["disabledforeground",self.dic_label["disabledforeground"]],["fg",self.dic_label["fg"]]
                        ,["foreground",self.dic_label["foreground"]],["height",self.dic_label["height"]],["highlightbackground",self.dic_label["highlightbackground"]]
                        ,["highlightcolor",self.dic_label["highlightcolor"]],["highlightthickness",self.dic_label["highlightthickness"]]
                        ,["image",self.dic_label["image"]],["justify",self.dic_label["justify"]],["padx_int",self.dic_label["padx"]],["pady_int",self.dic_label["pady"]]
                        ,["relief",self.dic_label["relief"]],["state",self.dic_label["state"]],["takefocus_int",self.dic_label["takefocus"]],["text",self.dic_label["text"]]
                        ,["textvariable",self.dic_label["textvariable"]],["underline",self.dic_label["underline"]],["width_int",self.dic_label["width"]]
                        ,["wraplength_int",self.dic_label["wraplength"]]]
        return self.dic_label["name window"],self.tt_label_1,self.tt_label_2,self.tt_label_3
class edit_button:
    def __init__(self):
        self.ten_button,self.thuoc_fame,self.font,self.font_size,self.net_chu,self.column,self.row,self.ipadx,self.ipady,self.padx_grid,self.pady_grid = gan_du_lieu(11)
        self.rowspan,self.columnspan,self.sticky,self.activebackground,self.activeforeground,self.anchor,self.background,self.bd,self.bg,self.bitmap = gan_du_lieu(10)
        self.border,self.borderwidth,self.command,self.compound,self.cursor,self.default,self.disabledforeground,self.fg,self.foreground,self.height = gan_du_lieu(10)
        self.highlightcolor,self.highlightthickness,self.image,self.justify,self.name,self.overrelief,self.padx,self.pady,self.relief,self.repeatdelay = gan_du_lieu(10)
        self.repeatinterval,self.state,self.takefocus,self.text,self.textvariable,self.underline,self.width,self.wraplength,self.highlightbackground = gan_du_lieu(9)
        self.dic_button_1 = {"name window":self.ten_button,"thuoc frame":self.thuoc_fame,"font":self.font,"font size":self.font_size,"net chu":self.net_chu,"column":self.column
                             ,"row":self.row,"ipadx":self.ipadx,"ipady":self.ipady,"padx gird":self.padx_grid,"pady gird":self.pady_grid
                             ,"rowspan":self.rowspan,"columnspan":self.columnspan,"sticky":self.sticky,"activebackground":self.activebackground
                             ,"activeforeground":self.activeforeground,"anchor":self.anchor,"background":self.background,"bd":self.bd,"bg":self.bg
                             ,"bitmap":self.bitmap,"border":self.border,"borderwidth":self.borderwidth,"command":self.command,"compound":self.compound
                             ,"cursor":self.cursor,"default":self.default,"disabledforeground":self.disabledforeground,"fg":self.fg,"foreground":self.foreground
                             ,"height":self.height,"highlightbackground":self.highlightbackground,"highlightcolor":self.highlightcolor
                             ,"highlightthickness":self.highlightthickness,"image":self.image,"justify":self.justify,"name":self.name,"overrelief":self.overrelief
                             ,"padx":self.padx,"pady":self.pady,"relief":self.relief,"state":self.state,"takefocus":self.takefocus,"text":self.text
                             ,"textvariable":self.textvariable,"repeatinterval":self.repeatinterval,"underline":self.underline,"width":self.width,"wraplength":self.wraplength}
        self.tt_button_1 = [["thuoc_frame",self.dic_button_1["thuoc frame"]],["font",self.dic_button_1["font"]],["font_size",self.dic_button_1["font size"]]
                            ,["net_chu",self.dic_button_1["net chu"]]]
        self.tt_button_2 = [["column",self.dic_button_1["column"]],["row_int",self.dic_button_1["row"]],["ipadx_int",self.dic_button_1["ipadx"]]
                            ,["ipady_int",self.dic_button_1["ipady"]],["padx_int",self.dic_button_1["padx gird"]],["pady_int",self.dic_button_1["pady gird"]]
                            ,["rowspan_int",self.dic_button_1["rowspan"]],["columnspan_int",self.dic_button_1["columnspan"]],["sticky",self.dic_button_1["sticky"]]]
        self.tt_button_3 = [["activebackground",self.dic_button_1["activebackground"]],["activeforeground",self.dic_button_1["activeforeground"]]
                            ,["anchor",self.dic_button_1["anchor"]],["background",self.dic_button_1["background"]],["bd",self.dic_button_1["bd"]]
                            ,["bg",self.dic_button_1["bg"]],["bitmap",self.dic_button_1["bitmap"]],["border",self.dic_button_1["border"]]
                            ,["borderwidth_int",self.dic_button_1["borderwidth"]],["command",self.dic_button_1["command"]],["compound",self.dic_button_1["compound"]]
                            ,["cursor",self.dic_button_1["cursor"]],["default",self.dic_button_1["default"]],["disabledforeground",self.dic_button_1["disabledforeground"]]
                            ,["fg",self.dic_button_1["fg"]],["foreground",self.dic_button_1["foreground"]],["height_int",self.dic_button_1["height"]]
                            ,["highlightbackground",self.dic_button_1["highlightbackground"]],["highlightcolor",self.dic_button_1["highlightcolor"]]
                            ,["highlightthickness_int",self.dic_button_1["highlightthickness"]],["image",self.dic_button_1["image"]],["justify",self.dic_button_1["justify"]]
                            ,["name",self.dic_button_1["name"]],["overrelief",self.dic_button_1["overrelief"]],["padx_int",self.dic_button_1["padx"]]
                            ,["pady_int",self.dic_button_1["pady"]],["relief",self.dic_button_1["relief"]],["state",self.dic_button_1["state"]]
                            ,["takefocus_int",self.dic_button_1["takefocus"]],["text",self.dic_button_1["text"]],["textvariable",self.dic_button_1["textvariable"]]
                            ,["repeatinterval",self.dic_button_1["repeatinterval"]],["underline",self.dic_button_1["underline"]],["width_int",self.dic_button_1["width"]]
                            ,["wraplength_int",self.dic_button_1["wraplength"]]]
    def update_value(self,name="NA",value = "NA"): # input = "name_value"
        if value != "NA":
            try:
                self.dic_button_1[name] = value
            except:
                print("không tồn tại dữ liệu button "+ str(name))
        self.tt_button_1 = [["thuoc_frame",self.dic_button_1["thuoc frame"]],["font",self.dic_button_1["font"]],["font_size",self.dic_button_1["font size"]]
                            ,["net_chu",self.dic_button_1["net chu"]]]
        self.tt_button_2 = [["column",self.dic_button_1["column"]],["row_int",self.dic_button_1["row"]],["ipadx_int",self.dic_button_1["ipadx"]]
                            ,["ipady_int",self.dic_button_1["ipady"]],["padx_int",self.dic_button_1["padx gird"]],["pady_int",self.dic_button_1["pady gird"]]
                            ,["rowspan_int",self.dic_button_1["rowspan"]],["columnspan_int",self.dic_button_1["columnspan"]],["sticky",self.dic_button_1["sticky"]]]
        self.tt_button_3 = [["activebackground",self.dic_button_1["activebackground"]],["activeforeground",self.dic_button_1["activeforeground"]]
                            ,["anchor",self.dic_button_1["anchor"]],["background",self.dic_button_1["background"]],["bd",self.dic_button_1["bd"]]
                            ,["bg",self.dic_button_1["bg"]],["bitmap",self.dic_button_1["bitmap"]],["border",self.dic_button_1["border"]]
                            ,["borderwidth_int",self.dic_button_1["borderwidth"]],["command",self.dic_button_1["command"]],["compound",self.dic_button_1["compound"]]
                            ,["cursor",self.dic_button_1["cursor"]],["default",self.dic_button_1["default"]],["disabledforeground",self.dic_button_1["disabledforeground"]]
                            ,["fg",self.dic_button_1["fg"]],["foreground",self.dic_button_1["foreground"]],["height_int",self.dic_button_1["height"]]
                            ,["highlightbackground",self.dic_button_1["highlightbackground"]],["highlightcolor",self.dic_button_1["highlightcolor"]]
                            ,["highlightthickness_int",self.dic_button_1["highlightthickness"]],["image",self.dic_button_1["image"]],["justify",self.dic_button_1["justify"]]
                            ,["name",self.dic_button_1["name"]],["overrelief",self.dic_button_1["overrelief"]],["padx_int",self.dic_button_1["padx"]]
                            ,["pady_int",self.dic_button_1["pady"]],["relief",self.dic_button_1["relief"]],["state",self.dic_button_1["state"]]
                            ,["takefocus_int",self.dic_button_1["takefocus"]],["text",self.dic_button_1["text"]],["textvariable",self.dic_button_1["textvariable"]]
                            ,["repeatinterval",self.dic_button_1["repeatinterval"]],["underline",self.dic_button_1["underline"]],["width_int",self.dic_button_1["width"]]
                            ,["wraplength_int",self.dic_button_1["wraplength"]]]
        return self.dic_button_1["name window"],self.tt_button_1,self.tt_button_2,self.tt_button_3

class edit_entry:
    def __init__(self):
        self.ten_entry,self.thuoc_fame,self.font,self.font_size,self.net_chu,self.column,self.row,self.ipadx,self.ipady,self.padx_grid,self.pady_grid = gan_du_lieu(11)
        self.rowspan,self.columnspan,self.sticky,self.background,self.bd,self.bg,self.border,self.borderwidth,self.cursor,self.disabledbackground = gan_du_lieu(10)
        self.exportselection,self.fg,self.foreground,self.highlightbackground,self.highlightcolor,self.highlightthickness,self.insertbackground = gan_du_lieu(7)
        self.insertborderwidth,self.insertofftime,self.insertontime,self.insertwidth,self.invalidcommand,self.invcmd,self.justify,self.name,self.readonlybackground = gan_du_lieu(9)
        self.relief,self.selectbackground,self.selectborderwidth,self.selectforeground,self.show,self.state,self.takefocus,self.textvariable,self.validate = gan_du_lieu(9)
        self.validatecommand,self.vcmd,self.width,self.xscrollcommand,self.disabledforeground = gan_du_lieu(5)

        self.dic_entry = {"name window":self.ten_entry,"thuoc frame":self.thuoc_fame,"font":self.font,"font size":self.font_size,"net chu":self.net_chu,"column":self.column
                          ,"row":self.row,"ipadx":self.ipadx,"ipady":self.ipady,"padx grid":self.padx_grid,"pady grid":self.pady_grid,"rowspan":self.rowspan
                          ,"columnspan":self.columnspan,"sticky":self.sticky,"background":self.background,"bd":self.bd,"bg":self.bg,"border":self.border
                          ,"borderwidth":self.borderwidth,"cursor":self.cursor,"disabledbackground":self.disabledbackground,"exportselection":self.exportselection
                          ,"fg":self.fg,"foreground":self.foreground,"highlightbackground":self.highlightbackground,"highlightcolor":self.highlightcolor
                          ,"highlightthickness":self.highlightthickness,"insertbackground":self.insertbackground,"insertborderwidth":self.insertborderwidth
                          ,"insertofftime":self.insertofftime,"insertontime":self.insertontime,"insertwidth":self.insertwidth,"invalidcommand":self.invalidcommand
                          ,"invcmd":self.invcmd,"justify":self.justify,"name":self.name,"readonlybackground":self.readonlybackground,"relief":self.relief
                          ,"selectbackground":self.selectbackground,"selectborderwidth":self.selectborderwidth,"selectforeground":self.selectforeground
                          ,"show":self.show,"state":self.state,"takefocus":self.takefocus,"textvariable":self.textvariable,"validate":self.validate
                          ,"validatecommand":self.validatecommand,"vcmd":self.vcmd,"width":self.width,"xscrollcommand":self.xscrollcommand
                          ,"disabledforeground":self.disabledforeground}
        
        self.tt_entry_1 = [["thuoc_frame",self.dic_entry["thuoc frame"]],["font",self.dic_entry["font"]],["font_size",self.dic_entry["font size"]],["net_chu",self.dic_entry["net chu"]]]
        self.tt_entry_2 = [["column_int",self.dic_entry["column"]],["row_int",self.dic_entry["row"]],["ipadx_int",self.dic_entry["ipadx"]],["ipady_int",self.dic_entry["ipady"]]
                    ,["padx_int",self.dic_entry["padx grid"]],["pady_int",self.dic_entry["pady grid"]],["rowspan_int",self.dic_entry["rowspan"]]
                    ,["columnspan_int",self.dic_entry["columnspan"]],["sticky",self.dic_entry["sticky"]]]
        self.tt_entry_3 = [["background",self.dic_entry["background"]],["disabledbackground",self.dic_entry["disabledbackground"]]
                    ,["insertbackground",self.dic_entry["insertbackground"]],["background",self.dic_entry["background"]],["bd",self.dic_entry["bd"]],["bg",self.dic_entry["bg"]]
                    ,["exportselection",self.dic_entry["exportselection"]],["border",self.dic_entry["border"]],["borderwidth_int",self.dic_entry["borderwidth"]]
                    ,["insertborderwidth",self.dic_entry["insertborderwidth"]],["selectbackground",self.dic_entry["selectbackground"]],["cursor",self.dic_entry["cursor"]]
                    ,["readonlybackground",self.dic_entry["readonlybackground"]],["disabledforeground",self.dic_entry["disabledforeground"]]
                    ,["fg",self.dic_entry["fg"]],["foreground",self.dic_entry["foreground"]],["invalidcommand",self.dic_entry["invalidcommand"]]
                    ,["highlightbackground",self.dic_entry["highlightbackground"]],["highlightcolor",self.dic_entry["highlightcolor"]]
                    ,["highlightthickness_int",self.dic_entry["highlightthickness"]],["insertwidth",self.dic_entry["insertwidth"]]
                    ,["justify",self.dic_entry["justify"]],["name",self.dic_entry["name"]],["validatecommand",self.dic_entry["validatecommand"]]
                    ,["insertofftime_int",self.dic_entry["insertofftime"]],["insertontime_int",self.dic_entry["insertontime"]],["relief",self.dic_entry["relief"]]
                    ,["state",self.dic_entry["state"]],["takefocus_int",self.dic_entry["takefocus"]],["invcmd",self.dic_entry["invcmd"]]
                    ,["textvariable",self.dic_entry["textvariable"]],["xscrollcommand",self.dic_entry["xscrollcommand"]],["selectforeground",self.dic_entry["selectforeground"]]
                    ,["width_int",self.dic_entry["width"]],["selectborderwidth_int",self.dic_entry["selectborderwidth"]],["show",self.dic_entry["show"]]
                    ,["validate",self.dic_entry["validate"]],["vcmd",self.dic_entry["vcmd"]]]
    def update_value(self,name="NA",value = "NA"): # input = "name_value"
        if value != "NA":
            try:
                self.dic_entry[name] = value
            except:
                print("không tồn tại dữ liệu entry "+ str(name))
        self.tt_entry_1 = [["thuoc_frame",self.dic_entry["thuoc frame"]],["font",self.dic_entry["font"]],["font_size",self.dic_entry["font size"]],["net_chu",self.dic_entry["net chu"]]]
        self.tt_entry_2 = [["column_int",self.dic_entry["column"]],["row_int",self.dic_entry["row"]],["ipadx_int",self.dic_entry["ipadx"]],["ipady_int",self.dic_entry["ipady"]]
                    ,["padx_int",self.dic_entry["padx grid"]],["pady_int",self.dic_entry["pady grid"]],["rowspan_int",self.dic_entry["rowspan"]]
                    ,["columnspan_int",self.dic_entry["columnspan"]],["sticky",self.dic_entry["sticky"]]]
        self.tt_entry_3 = [["background",self.dic_entry["background"]],["disabledbackground",self.dic_entry["disabledbackground"]]
                    ,["insertbackground",self.dic_entry["insertbackground"]],["background",self.dic_entry["background"]],["bd",self.dic_entry["bd"]],["bg",self.dic_entry["bg"]]
                    ,["exportselection",self.dic_entry["exportselection"]],["border",self.dic_entry["border"]],["borderwidth_int",self.dic_entry["borderwidth"]]
                    ,["insertborderwidth",self.dic_entry["insertborderwidth"]],["selectbackground",self.dic_entry["selectbackground"]],["cursor",self.dic_entry["cursor"]]
                    ,["readonlybackground",self.dic_entry["readonlybackground"]],["disabledforeground",self.dic_entry["disabledforeground"]]
                    ,["fg",self.dic_entry["fg"]],["foreground",self.dic_entry["foreground"]],["invalidcommand",self.dic_entry["invalidcommand"]]
                    ,["highlightbackground",self.dic_entry["highlightbackground"]],["highlightcolor",self.dic_entry["highlightcolor"]]
                    ,["highlightthickness_int",self.dic_entry["highlightthickness"]],["insertwidth",self.dic_entry["insertwidth"]]
                    ,["justify",self.dic_entry["justify"]],["name",self.dic_entry["name"]],["validatecommand",self.dic_entry["validatecommand"]]
                    ,["insertofftime_int",self.dic_entry["insertofftime"]],["insertontime_int",self.dic_entry["insertontime"]],["relief",self.dic_entry["relief"]]
                    ,["state",self.dic_entry["state"]],["takefocus_int",self.dic_entry["takefocus"]],["invcmd",self.dic_entry["invcmd"]]
                    ,["textvariable",self.dic_entry["textvariable"]],["xscrollcommand",self.dic_entry["xscrollcommand"]],["selectforeground",self.dic_entry["selectforeground"]]
                    ,["width_int",self.dic_entry["width"]],["selectborderwidth_int",self.dic_entry["selectborderwidth"]],["show",self.dic_entry["show"]]
                    ,["validate",self.dic_entry["validate"]],["vcmd",self.dic_entry["vcmd"]]]
        return self.dic_entry["name window"],self.tt_entry_1,self.tt_entry_2,self.tt_entry_3

class edit_radiobutton:
    def __init__(self):
        self.ten_radiobutton,self.thuoc_fame,self.font,self.font_size,self.net_chu,self.column,self.row,self.ipadx = gan_du_lieu(8)
        self.ipady,self.padx_grid,self.pady_grid,self.rowspan,self.columnspan,self.sticky = gan_du_lieu(6)
        self.classs,self.command,self.compound,self.cursor,self.image,self.name,self.padding,self.state,self.style = gan_du_lieu(9)
        self.takefocus,self.text,self.textvariable,self.underline,self.value,self.variable,self.width = gan_du_lieu(7)

        self.dic_radiobutton ={"name window":self.ten_radiobutton,"thuoc frame":self.thuoc_fame,"font":self.font,"font size":self.font_size,"net chu":self.net_chu
                               ,"column":self.column,"row":self.row,"ipadx":self.ipadx,"ipady":self.ipady,"padx grid":self.padx_grid,"pady grid":self.pady_grid
                               ,"rowspan":self.rowspan,"columnspan":self.columnspan,"sticky":self.sticky,"classs":self.classs,"command":self.command
                               ,"compound":self.compound,"cursor":self.cursor,"image":self.image,"name":self.name,"padding":self.padding,"state":self.state
                               ,"style":self.style,"takefocus":self.takefocus,"text":self.text,"textvariable":self.textvariable,"underline":self.underline
                               ,"value":self.value,"variable":self.variable,"width":self.width}
        self.tt_radiobutton_1 = [["thuoc_frame",self.dic_radiobutton["thuoc frame"]],["font",self.dic_radiobutton["font"]],["font_size",self.dic_radiobutton["font size"]]
                        ,["net_chu",self.dic_radiobutton["net chu"]]]
        
        self.tt_radiobutton_2 = [["column_int",self.dic_radiobutton["column"]],["row_int",self.dic_radiobutton["row"]],["ipadx_int",self.dic_radiobutton["ipadx"]]
                            ,["ipady_int",self.dic_radiobutton["ipady"]],["padx_int",self.dic_radiobutton["padx grid"]],["pady_int",self.dic_radiobutton["pady grid"]]
                            ,["rowspan_int",self.dic_radiobutton["rowspan"]],["columnspan_int",self.dic_radiobutton["columnspan"]],["sticky",self.dic_radiobutton["sticky"]]]
        
        self.tt_radiobutton_3 = [["classs",self.dic_radiobutton["classs"]],["padding",self.dic_radiobutton["padding"]],["style",self.dic_radiobutton["style"]]
                            ,["command",self.dic_radiobutton["command"]],["compound",self.dic_radiobutton["compound"]],["cursor",self.dic_radiobutton["cursor"]]
                            ,["image",self.dic_radiobutton["image"]],["name",self.dic_radiobutton["name"]],["state",self.dic_radiobutton["state"]]
                            ,["takefocus_int",self.dic_radiobutton["takefocus"]],["text",self.dic_radiobutton["text"]],["textvariable",self.dic_radiobutton["textvariable"]]
                            ,["underline",self.dic_radiobutton["underline"]],["width_int",self.dic_radiobutton["width"]],["value_int",self.dic_radiobutton["value"]]
                            ,["variable",self.dic_radiobutton["variable"]]]

    def update_value(self,name="NA",value = "NA"): # input = "name_value"
        if value != "NA":
            try:
                self.dic_radiobutton[name] = value
            except:
                print("không tồn tại dữ liệu radiobutton "+ str(name))
        self.tt_radiobutton_1 = [["thuoc_frame",self.dic_radiobutton["thuoc frame"]],["font",self.dic_radiobutton["font"]],["font_size",self.dic_radiobutton["font size"]]
                        ,["net_chu",self.dic_radiobutton["net chu"]]]
        
        self.tt_radiobutton_2 = [["column_int",self.dic_radiobutton["column"]],["row_int",self.dic_radiobutton["row"]],["ipadx_int",self.dic_radiobutton["ipadx"]]
                            ,["ipady_int",self.dic_radiobutton["ipady"]],["padx_int",self.dic_radiobutton["padx grid"]],["pady_gird_int",self.dic_radiobutton["pady grid"]]
                            ,["rowspan_int",self.dic_radiobutton["rowspan"]],["columnspan_int",self.dic_radiobutton["columnspan"]],["sticky",self.dic_radiobutton["sticky"]]]
        
        self.tt_radiobutton_3 = [["classs",self.dic_radiobutton["classs"]],["padding",self.dic_radiobutton["padding"]],["style",self.dic_radiobutton["style"]]
                            ,["command",self.dic_radiobutton["command"]],["compound",self.dic_radiobutton["compound"]],["cursor",self.dic_radiobutton["cursor"]]
                            ,["image",self.dic_radiobutton["image"]],["name",self.dic_radiobutton["name"]],["state",self.dic_radiobutton["state"]]
                            ,["takefocus_int",self.dic_radiobutton["takefocus"]],["text",self.dic_radiobutton["text"]],["textvariable",self.dic_radiobutton["textvariable"]]
                            ,["underline",self.dic_radiobutton["underline"]],["width_int",self.dic_radiobutton["width"]],["value_int",self.dic_radiobutton["value"]]
                            ,["variable",self.dic_radiobutton["variable"]]]

        return self.dic_radiobutton["name window"],self.tt_radiobutton_1,self.tt_radiobutton_2,self.tt_radiobutton_3

class edit_checkbutton:
    def __init__(self):
        self.ten_checkbutton,self.thuoc_fame,self.font,self.font_size,self.net_chu,self.column,self.row,self.ipadx,self.ipady,self.padx_grid,self.pady_grid = gan_du_lieu(11)
        self.rowspan,self.columnspan,self.sticky,self.activebackground,self.activeforeground,self.anchor,self.background,self.bd,self.bg,self.bitmap = gan_du_lieu(10)
        self.border,self.borderwidth,self.command,self.compound,self.cursor,self.disabledforeground,self.fg,self.foreground,self.height,self.offrelief = gan_du_lieu(10)
        self.highlightcolor,self.highlightthickness,self.image,self.justify,self.name,self.overrelief,self.padx,self.pady,self.relief,self.repeatdelay = gan_du_lieu(10)
        self.repeatinterval,self.state,self.takefocus,self.text,self.textvariable,self.underline,self.width,self.wraplength,self.highlightbackground,self.indicatoron = gan_du_lieu(10)
        self.offvalue,self.onvalue,self.selectcolor,self.selectimage,self.tristateimage,self.tristatevalue,self.offrelief,self.variable=gan_du_lieu(8)
        self.checkbutton = {"name window":self.ten_checkbutton,"thuoc frame":self.thuoc_fame,"font":self.font,"font size":self.font_size,"net chu":self.net_chu
                             ,"column":self.column
                             ,"row":self.row,"ipadx":self.ipadx,"ipady":self.ipady,"padx gird":self.padx_grid,"pady gird":self.pady_grid
                             ,"rowspan":self.rowspan,"columnspan":self.columnspan,"sticky":self.sticky,"activebackground":self.activebackground
                             ,"activeforeground":self.activeforeground,"anchor":self.anchor,"background":self.background,"bd":self.bd,"bg":self.bg
                             ,"bitmap":self.bitmap,"border":self.border,"borderwidth":self.borderwidth,"command":self.command,"compound":self.compound
                             ,"cursor":self.cursor,"disabledforeground":self.disabledforeground,"fg":self.fg,"foreground":self.foreground
                             ,"height":self.height,"highlightbackground":self.highlightbackground,"highlightcolor":self.highlightcolor
                             ,"highlightthickness":self.highlightthickness,"image":self.image,"justify":self.justify,"name":self.name,"overrelief":self.overrelief
                             ,"padx":self.padx,"pady":self.pady,"relief":self.relief,"state":self.state,"takefocus":self.takefocus,"text":self.text,"indicatoron":self.indicatoron 
                             ,"textvariable":self.textvariable,"repeatinterval":self.repeatinterval,"underline":self.underline,"width":self.width,"wraplength":self.wraplength
                             ,"offvalue":self.offvalue,"onvalue":self.onvalue,"selectcolor":self.selectcolor,"selectimage":self.selectimage,"tristatevalue":self.tristatevalue
                             ,"tristatevalue":self.tristatevalue,"offrelief":self.offrelief,"variable":self.variable}
        self.tt_checkbutton_1 = [["thuoc_frame",self.checkbutton["thuoc frame"]],["font",self.checkbutton["font"]],["font_size",self.checkbutton["font size"]]
                        ,["net_chu",self.checkbutton["net chu"]]]
        self.tt_checkbutton_2 = [["column",self.checkbutton["column"]],["row_int",self.checkbutton["row"]],["ipadx_int",self.checkbutton["ipadx"]]
                            ,["ipady_int",self.checkbutton["ipady"]],["padx_int",self.checkbutton["padx gird"]],["pady_int",self.checkbutton["pady gird"]]
                            ,["rowspan_int",self.checkbutton["rowspan"]],["columnspan_int",self.checkbutton["columnspan"]],["sticky",self.checkbutton["sticky"]]]
        self.tt_checkbutton_3 = [["activebackground",self.checkbutton["activebackground"]],["activeforeground",self.checkbutton["activeforeground"]]
                            ,["anchor",self.checkbutton["anchor"]],["background",self.checkbutton["background"]],["bd",self.checkbutton["bd"]]
                            ,["bg",self.checkbutton["bg"]],["bitmap",self.checkbutton["bitmap"]],["border",self.checkbutton["border"]]
                            ,["borderwidth_int",self.checkbutton["borderwidth"]],["command",self.checkbutton["command"]],["compound",self.checkbutton["compound"]]
                            ,["cursor",self.checkbutton["cursor"]],["disabledforeground",self.checkbutton["disabledforeground"]]
                            ,["fg",self.checkbutton["fg"]],["foreground",self.checkbutton["foreground"]],["height_int",self.checkbutton["height"]]
                            ,["highlightbackground",self.checkbutton["highlightbackground"]],["highlightcolor",self.checkbutton["highlightcolor"]]
                            ,["highlightthickness_int",self.checkbutton["highlightthickness"]],["image",self.checkbutton["image"]],["justify",self.checkbutton["justify"]]
                            ,["name",self.checkbutton["name"]],["overrelief",self.checkbutton["overrelief"]],["padx_int",self.checkbutton["padx"]]
                            ,["pady_int",self.checkbutton["pady"]],["relief",self.checkbutton["relief"]],["state",self.checkbutton["state"]]
                            ,["takefocus_int",self.checkbutton["takefocus"]],["text",self.checkbutton["text"]],["textvariable",self.checkbutton["textvariable"]]
                            ,["repeatinterval",self.checkbutton["repeatinterval"]],["underline",self.checkbutton["underline"]],["width_int",self.checkbutton["width"]]
                            ,["wraplength_int",self.checkbutton["wraplength"]],["indicatoron",self.checkbutton["indicatoron"]],["offrelief",self.checkbutton["offrelief"]]
                            ,["offvalue",self.checkbutton["offvalue"]],["onvalue",self.checkbutton["onvalue"]],["selectcolor",self.checkbutton["selectcolor"]]
                            ,["selectimage",self.checkbutton["selectimage"]],["tristatevalue",self.checkbutton["tristatevalue"]],["variable",self.checkbutton["variable"]]
                            ,["tristatevalue",self.checkbutton["tristatevalue"]]]
    def update_value(self,name="NA",value = "NA"): # input = "name_value"
        if value != "NA":
            try:
                self.checkbutton[name] = value
            except:
                print("không tồn tại dữ liệu checkbutton "+ str(name))
        self.tt_checkbutton_1 = [["thuoc_frame",self.checkbutton["thuoc frame"]],["font",self.checkbutton["font"]],["font_size",self.checkbutton["font size"]]
                        ,["net_chu",self.checkbutton["net chu"]]]
        self.tt_checkbutton_2 = [["column",self.checkbutton["column"]],["row_int",self.checkbutton["row"]],["ipadx_int",self.checkbutton["ipadx"]]
                            ,["ipady_int",self.checkbutton["ipady"]],["padx_int",self.checkbutton["padx gird"]],["pady_int",self.checkbutton["pady gird"]]
                            ,["rowspan_int",self.checkbutton["rowspan"]],["columnspan_int",self.checkbutton["columnspan"]],["sticky",self.checkbutton["sticky"]]]
        
        self.tt_checkbutton_3 = [["activebackground",self.checkbutton["activebackground"]],["activeforeground",self.checkbutton["activeforeground"]]
                            ,["anchor",self.checkbutton["anchor"]],["background",self.checkbutton["background"]],["bd",self.checkbutton["bd"]]
                            ,["bg",self.checkbutton["bg"]],["bitmap",self.checkbutton["bitmap"]],["border",self.checkbutton["border"]]
                            ,["borderwidth_int",self.checkbutton["borderwidth"]],["command",self.checkbutton["command"]],["compound",self.checkbutton["compound"]]
                            ,["cursor",self.checkbutton["cursor"]],["disabledforeground",self.checkbutton["disabledforeground"]]
                            ,["fg",self.checkbutton["fg"]],["foreground",self.checkbutton["foreground"]],["height_int",self.checkbutton["height"]]
                            ,["highlightbackground",self.checkbutton["highlightbackground"]],["highlightcolor",self.checkbutton["highlightcolor"]]
                            ,["highlightthickness_int",self.checkbutton["highlightthickness"]],["image",self.checkbutton["image"]],["justify",self.checkbutton["justify"]]
                            ,["name",self.checkbutton["name"]],["overrelief",self.checkbutton["overrelief"]],["padx_int",self.checkbutton["padx"]]
                            ,["pady_int",self.checkbutton["pady"]],["relief",self.checkbutton["relief"]],["state",self.checkbutton["state"]]
                            ,["takefocus_int",self.checkbutton["takefocus"]],["text",self.checkbutton["text"]],["textvariable",self.checkbutton["textvariable"]]
                            ,["repeatinterval",self.checkbutton["repeatinterval"]],["underline",self.checkbutton["underline"]],["width_int",self.checkbutton["width"]]
                            ,["wraplength_int",self.checkbutton["wraplength"]],["indicatoron",self.checkbutton["indicatoron"]],["offrelief",self.checkbutton["offrelief"]]
                            ,["offvalue",self.checkbutton["offvalue"]],["onvalue",self.checkbutton["onvalue"]],["selectcolor",self.checkbutton["selectcolor"]]
                            ,["selectimage",self.checkbutton["selectimage"]],["tristatevalue",self.checkbutton["tristatevalue"]],["variable",self.checkbutton["variable"]]
                            ,["tristatevalue",self.checkbutton["tristatevalue"]]]
        return self.checkbutton["name window"],self.tt_checkbutton_1,self.tt_checkbutton_2,self.tt_checkbutton_3

class edit_frame:
    def __init__(self):
        self.ten_frame,self.thuoc_fame,self.columnconfigure,self.rowconfigure,self.column,self.row,self.ipadx,self.ipady,self.padx_grid,self.pady_grid = gan_du_lieu(10)
        self.rowspan,self.columnspan,self.sticky,self.background,self.bd,self.bg,self.border,self.borderwidth,self.classs,self.colormap = gan_du_lieu(10)
        self.container,self.cursor,self.height,self.highlightbackground,self.highlightcolor,self.highlightthickness,self.name,self.padx = gan_du_lieu(8)
        self.pady,self.relief,self.takefocus,self.visual,self.width = gan_du_lieu(5)

        self.dic_frame = {"name window":self.ten_frame,"thuoc frame":self.thuoc_fame,"columnconfigure":self.columnconfigure,"rowconfigure":self.rowconfigure
                          ,"column":self.column,"row":self.row,"ipadx":self.ipadx,"ipady":self.ipady,"padx grid":self.padx_grid,"pady grid":self.pady_grid
                          ,"rowspan":self.rowspan,"columnspan":self.columnspan,"sticky":self.sticky,"background":self.background,"bd":self.bd,"bg":self.bg
                          ,"border":self.border,"borderwidth":self.borderwidth,"classs":self.classs,"colormap":self.colormap,"container":self.container
                          ,"cursor":self.cursor,"height":self.height,"highlightbackground":self.highlightbackground,"highlightcolor":self.highlightcolor
                          ,"highlightthickness":self.highlightthickness,"name":self.name,"padx":self.padx,"pady":self.pady,"relief":self.relief,"takefocus":self.takefocus
                          ,"visual":self.visual,"width":self.width}

        self.tt_frame_1 = [["thuoc_frame",self.dic_frame["thuoc frame"]],["columnconfigure",self.dic_frame["columnconfigure"]],["rowconfigure",self.dic_frame["rowconfigure"]]]
        self.tt_frame_2 = [["column_int",self.dic_frame["column"]],["row_int",self.dic_frame["row"]],["ipadx_int",self.dic_frame["ipadx"]],["ipady_int",self.dic_frame["ipady"]]
                    ,["padx_int",self.dic_frame["padx grid"]],["pady_int",self.dic_frame["pady grid"]],["rowspan_int",self.dic_frame["rowspan"]]
                    ,["columnspan_int",self.dic_frame["columnspan"]],["sticky",self.dic_frame["sticky"]]]
        self.tt_frame_3 = [["classs",self.dic_frame["classs"]],["colormap",self.dic_frame["colormap"]],["container",self.dic_frame["container"]]
                    ,["background",self.dic_frame["background"]],["bd",self.dic_frame["bd"]],["bg",self.dic_frame["bg"]],["border",self.dic_frame["border"]]
                    ,["borderwidth_int",self.dic_frame["borderwidth"]],["visual",self.dic_frame["visual"]],["cursor",self.dic_frame["cursor"]]
                    ,["height_int",self.dic_frame["height"]],["highlightbackground",self.dic_frame["highlightbackground"]]
                    ,["highlightcolor",self.dic_frame["highlightcolor"]],["highlightthickness_int",self.dic_frame["highlightthickness"]],["name",self.dic_frame["name"]]
                    ,["padx_int",self.dic_frame["padx"]],["pady_int",self.dic_frame["pady"]],["relief",self.dic_frame["relief"]]
                    ,["takefocus_int",self.dic_frame["takefocus"]],["width_int",self.dic_frame['width']]]
        
    def update_value(self,name="NA",value = "NA"): # input = "name_value"
        if value != "NA":
            try:
                if name == "columnconfigure" and value != "NA":
                    try:
                        value_new = []
                        ds_value = str(value).split("_")
                        for i in range(0,len(ds_value)):
                            value_new.append(int(ds_value[i]))
                        self.dic_frame[name] = value_new
                    except:
                        print("sai fomat root[columnconfigure] "+ str(value))
                if name == "rowconfigure" and value != "NA":
                    try:
                        value_new = []
                        ds_value = str(value).split("_")
                        for i in range(0,len(ds_value)):
                            value_new.append(int(ds_value[i]))
                        self.dic_frame[name] = value_new
                    except:
                        print("sai fomat root[columnconfigure] "+ str(value))
                if (name != "columnconfigure" and name != "rowconfigure") or value == "NA":
                    self.dic_frame[name] = value
                # self.dic_frame[name] = value
            except:
                print("không tồn tại dữ liệu frame "+ str(name))
        # if self.dic_frame["name window"] != "NA" and self.dic_frame["thuoc fame"] != "NA":
        self.tt_frame_1 = [["thuoc_frame",self.dic_frame["thuoc frame"]],["columnconfigure",self.dic_frame["columnconfigure"]],["rowconfigure",self.dic_frame["rowconfigure"]]]
        self.tt_frame_2 = [["column_int",self.dic_frame["column"]],["row_int",self.dic_frame["row"]],["ipadx_int",self.dic_frame["ipadx"]],["ipady_int",self.dic_frame["ipady"]]
                    ,["padx_int",self.dic_frame["padx grid"]],["pady_int",self.dic_frame["pady grid"]],["rowspan_int",self.dic_frame["rowspan"]]
                    ,["columnspan_int",self.dic_frame["columnspan"]],["sticky",self.dic_frame["sticky"]]]
        self.tt_frame_3 = [["classs",self.dic_frame["classs"]],["colormap",self.dic_frame["colormap"]],["container",self.dic_frame["container"]]
                    ,["background",self.dic_frame["background"]],["bd",self.dic_frame["bd"]],["bg",self.dic_frame["bg"]],["border",self.dic_frame["border"]]
                    ,["borderwidth_int",self.dic_frame["borderwidth"]],["visual",self.dic_frame["visual"]],["cursor",self.dic_frame["cursor"]]
                    ,["height_int",self.dic_frame["height"]],["highlightbackground",self.dic_frame["highlightbackground"]]
                    ,["highlightcolor",self.dic_frame["highlightcolor"]],["highlightthickness_int",self.dic_frame["highlightthickness"]],["name",self.dic_frame["name"]]
                    ,["padx_int",self.dic_frame["padx"]],["pady_int",self.dic_frame["pady"]],["relief",self.dic_frame["relief"]]
                    ,["takefocus_int",self.dic_frame["takefocus"]],["width_int",self.dic_frame['width']]]
        return self.dic_frame["name window"],self.tt_frame_1,self.tt_frame_2,self.tt_frame_3

class edit_canvas:
    def __init__(self):
        self.ten_canvas,self.thuoc_fame,self.name_scrollbar,self.name_img,self.column_scrollbar,self.row_scrollbar,self.sticky_scrollbar,self.sticky2 = gan_du_lieu(8)
        self.column,self.row,self.ipadx,self.ipady,self.padx_grid,self.pady_grid,self.rowspan,self.columnspan,self.sticky = gan_du_lieu(9)
        self.background,self.bd,self.bg,self.border,self.borderwidth,self.closeenough,self.confine,self.cursor,self.height,self.highlightbackground = gan_du_lieu(10)
        self.highlightcolor,self.highlightthickness,self.insertbackground,self.insertborderwidth,self.insertofftime,self.insertontime,self.insertwidth = gan_du_lieu(7)
        self.name,self.offset,self.relief,self.scrollregion,self.selectbackground,self.selectborderwidth,self.selectforeground,self.state,self.takefocus = gan_du_lieu(9)
        self.width_canvas,self.xscrollcommand,self.xscrollincrement,self.yscrollcommand,self.yscrollincrement = gan_du_lieu(5)
        self.font_button,self.fontsize_button,self.width_button1,self.width_button2,self.bg_button1,self.bg_button2,self.width_text = gan_du_lieu(7)
        self.new_canvas,self.remove_button,self.update_button = [1,0,0]

        self.dic_canvas = {"name window":self.ten_canvas,"thuoc frame":self.thuoc_fame,"name scrollbar":self.name_scrollbar,"name img":self.name_img
                           ,"column scrollbar":self.column_scrollbar,"row scrollbar":self.row_scrollbar,"sticky scrollbar":self.sticky_scrollbar
                           ,"sticky2":self.sticky2,"column":self.column,"row":self.row,"ipadx":self.ipadx,"ipady":self.ipady,"padx grid":self.padx_grid
                           ,"pady grid":self.pady_grid,"rowspan":self.rowspan,"columnspan":self.columnspan,"sticky":self.sticky,"background":self.background
                           ,"bd":self.bd,"bg":self.bg,"border":self.border,"borderwidth":self.borderwidth,"closeenough":self.closeenough,"confine":self.confine
                           ,"cursor":self.cursor,"height":self.height,"highlightbackground":self.highlightbackground,"highlightcolor":self.highlightcolor
                           ,"highlightthickness":self.highlightthickness,"insertbackground":self.insertbackground,"insertborderwidth":self.insertborderwidth
                           ,"insertofftime":self.insertofftime,"insertontime":self.insertontime,"insertwidth":self.insertwidth,"name":self.name
                           ,"offset":self.offset,"relief":self.relief,"scrollregion":self.scrollregion,"selectbackground":self.selectbackground
                           ,"selectborderwidth":self.selectborderwidth,"selectforeground":self.selectforeground,"state":self.state,"takefocus":self.takefocus
                           ,"width canvas":self.width_canvas,"xscrollcommand":self.xscrollcommand,"xscrollincrement":self.xscrollincrement,"yscrollcommand":self.yscrollcommand
                           ,"yscrollincrement":self.yscrollincrement,"font button":self.font_button,"fontsize button":self.fontsize_button,"width button1":self.width_button1
                           ,"width button2":self.width_button2,"bg button1":self.bg_button1,"bg button2":self.bg_button2,"width text":self.width_text,"new canvas":self.new_canvas
                           ,"remove button":self.remove_button,"update button":self.update_button}

        self.tt_canvas_1 = [["thuoc_frame",self.dic_canvas["thuoc frame"]],["name_img",self.dic_canvas["name img"]],["name_scrollbar",self.dic_canvas["name scrollbar"]]
                            ,["sticky2",self.dic_canvas["sticky2"]],["width_text_int",self.dic_canvas["width text"]]]
        self.tt_canvas_2 = [["column_int",self.dic_canvas["column"]],["row_int",self.dic_canvas["row"]],["ipadx_int",self.dic_canvas["ipadx"]]
                            ,["ipady_int",self.dic_canvas["ipady"]],["padx_int",self.dic_canvas["padx grid"]],["pady_int",self.dic_canvas["pady grid"]]
                            ,["rowspan_int",self.dic_canvas["rowspan"]],["columnspan_int",self.dic_canvas["columnspan"]],["sticky",self.dic_canvas["sticky"]]]
        self.tt_canvas_3 = [["background",self.dic_canvas["background"]],["closeenough",self.dic_canvas["closeenough"]],["insertbackground",self.dic_canvas["insertbackground"]]
                            ,["background",self.dic_canvas["background"]],["bd",self.dic_canvas["bd"]],["bg",self.dic_canvas["bg"]],["confine",self.dic_canvas["confine"]]
                            ,["border",self.dic_canvas["border"]],["borderwidth_int",self.dic_canvas["borderwidth"]],["insertborderwidth",self.dic_canvas["insertborderwidth"]]
                            ,["selectbackground",self.dic_canvas["selectbackground"]],["cursor",self.dic_canvas["cursor"]],["yscrollcommand",self.dic_canvas["yscrollcommand"]]
                            ,["yscrollincrement",self.dic_canvas["yscrollincrement"]],["offset",self.dic_canvas["offset"]],["scrollregion",self.dic_canvas["scrollregion"]]
                            ,["height_int",self.dic_canvas["height"]],["highlightbackground",self.dic_canvas["highlightbackground"]]
                            ,["highlightcolor",self.dic_canvas["highlightcolor"]],["highlightthickness_int",self.dic_canvas["highlightthickness"]]
                            ,["insertwidth",self.dic_canvas["insertwidth"]],["name",self.dic_canvas["name"]],["xscrollincrement",self.dic_canvas["xscrollincrement"]]
                            ,["insertofftime_int",self.dic_canvas["insertofftime"]],["insertontime_int",self.dic_canvas["insertontime"]],["relief",self.dic_canvas["relief"]]
                            ,["state",self.dic_canvas["state"]],["takefocus_int",self.dic_canvas["takefocus"]],["xscrollcommand",self.dic_canvas["xscrollcommand"]]
                            ,["selectforeground",self.dic_canvas["selectforeground"]],["width_int",self.dic_canvas["width canvas"]]
                            ,["selectborderwidth_int",self.dic_canvas["selectborderwidth"]]]
        self.tt_scrollbar = [["column",self.dic_canvas["column scrollbar"]],["row",self.dic_canvas["row scrollbar"]]
                            ,["sticky",self.dic_canvas["sticky scrollbar"]]]
        self.tt_button = [["font_button",self.dic_canvas["font button"]],["fontsize_button",self.dic_canvas["fontsize button"]],["width_button1",self.dic_canvas["width button1"]]          
                        ,["width_button2",self.dic_canvas["width button2"]],["bg_button1",self.dic_canvas["bg button1"]],["bg_button2",self.dic_canvas["bg button2"]]]
        
    def update_value(self,name="NA",value = "NA"): # input = "name_value"
        if value != "NA":
            try:
                self.dic_canvas[name] = value
            except:
                print("không tồn tại dữ liệu canvas "+ str(name))
        if self.dic_canvas["name window"] != "NA" and self.dic_canvas["thuoc frame"] != "NA":
            self.tt_canvas_1 = [["thuoc_frame",self.dic_canvas["thuoc frame"]],["name_img",self.dic_canvas["name img"]],["name_scrollbar",self.dic_canvas["name scrollbar"]]
                                ,["sticky2",self.dic_canvas["sticky2"]],["width_text_int",self.dic_canvas["width text"]]]
            self.tt_canvas_2 = [["column_int",self.dic_canvas["column"]],["row_int",self.dic_canvas["row"]],["ipadx_int",self.dic_canvas["ipadx"]]
                                ,["ipady_int",self.dic_canvas["ipady"]],["padx_int",self.dic_canvas["padx grid"]],["pady_int",self.dic_canvas["pady grid"]]
                                ,["rowspan_int",self.dic_canvas["rowspan"]],["columnspan_int",self.dic_canvas["columnspan"]],["sticky",self.dic_canvas["sticky"]]]
            self.tt_canvas_3 = [["background",self.dic_canvas["background"]],["closeenough",self.dic_canvas["closeenough"]],["insertbackground",self.dic_canvas["insertbackground"]]
                                ,["background",self.dic_canvas["background"]],["bd",self.dic_canvas["bd"]],["bg",self.dic_canvas["bg"]],["confine",self.dic_canvas["confine"]]
                                ,["border",self.dic_canvas["border"]],["borderwidth_int",self.dic_canvas["borderwidth"]],["insertborderwidth",self.dic_canvas["insertborderwidth"]]
                                ,["selectbackground",self.dic_canvas["selectbackground"]],["cursor",self.dic_canvas["cursor"]],["yscrollcommand",self.dic_canvas["yscrollcommand"]]
                                ,["yscrollincrement",self.dic_canvas["yscrollincrement"]],["offset",self.dic_canvas["offset"]],["scrollregion",self.dic_canvas["scrollregion"]]
                                ,["height_int",self.dic_canvas["height"]],["highlightbackground",self.dic_canvas["highlightbackground"]]
                                ,["highlightcolor",self.dic_canvas["highlightcolor"]],["highlightthickness_int",self.dic_canvas["highlightthickness"]]
                                ,["insertwidth",self.dic_canvas["insertwidth"]],["name",self.dic_canvas["name"]],["xscrollincrement",self.dic_canvas["xscrollincrement"]]
                                ,["insertofftime_int",self.dic_canvas["insertofftime"]],["insertontime_int",self.dic_canvas["insertontime"]],["relief",self.dic_canvas["relief"]]
                                ,["state",self.dic_canvas["state"]],["takefocus_int",self.dic_canvas["takefocus"]],["xscrollcommand",self.dic_canvas["xscrollcommand"]]
                                ,["selectforeground",self.dic_canvas["selectforeground"]],["width_int",self.dic_canvas["width canvas"]]
                                ,["selectborderwidth_int",self.dic_canvas["selectborderwidth"]]]
            self.tt_scrollbar = [["column",self.dic_canvas["column scrollbar"]],["row",self.dic_canvas["row scrollbar"]]
                                ,["sticky",self.dic_canvas["sticky scrollbar"]]]
            self.tt_button = [["font_button",self.dic_canvas["font button"]],["fontsize_button",self.dic_canvas["fontsize button"]],["width_button1",self.dic_canvas["width button1"]]          
                        ,["width_button2",self.dic_canvas["width button2"]],["bg_button1",self.dic_canvas["bg button1"]],["bg_button2",self.dic_canvas["bg button2"]]]
        return self.dic_canvas["name window"],self.tt_canvas_1,self.tt_canvas_2,self.tt_canvas_3,self.tt_scrollbar,self.tt_button,self.dic_canvas["new canvas"],self.dic_canvas["remove button"],self.dic_canvas["update button"]


class edit_frame_canvas:
    def __init__(self):
        self.ten_frame_canvas,self.thuoc_fame,self.column,self.row,self.ipadx,self.ipady,self.padx_grid,self.pady_grid,self.rowspan,self.columnspan,self.sticky = gan_du_lieu(11)
        self.dic_frame_canvas = {"name window":self.ten_frame_canvas,"thuoc frame":self.thuoc_fame,"column":self.column,"row":self.row,"ipadx":self.ipadx,"ipady":self.ipady
                                 ,"padx grid":self.padx_grid,"pady grid":self.pady_grid,"rowspan":self.rowspan,"columnspan":self.columnspan,"sticky":self.sticky}
        self.tt_frame_canvas_1 = [["thuoc_frame",self.dic_frame_canvas["thuoc frame"]]]
        self.tt_frame_canvas_2 = [["column_int",self.dic_frame_canvas["column"]],["row_int",self.dic_frame_canvas["row"]],["ipadx_int",self.dic_frame_canvas["ipadx"]]
                                  ,["ipady_int",self.dic_frame_canvas["ipady"]],["padx_int",self.dic_frame_canvas["padx grid"]]
                                  ,["pady_int",self.dic_frame_canvas["pady grid"]],["rowspan_int",self.dic_frame_canvas["rowspan"]]
                                  ,["columnspan_int",self.dic_frame_canvas["columnspan"]],["sticky",self.dic_frame_canvas["sticky"]]]
    def update_value(self,name="NA",value = "NA"): # input = "name_value"
        if value != "NA":
            try:
                self.dic_frame_canvas[name] = value
            except:
                print("không tồn tại dữ liệu frame_canvas "+ str(name))
        self.tt_frame_canvas_1 = [["thuoc_frame",self.dic_frame_canvas["thuoc frame"]]]
        self.tt_frame_canvas_2 = [["column_int",self.dic_frame_canvas["column"]],["row_int",self.dic_frame_canvas["row"]],["ipadx_int",self.dic_frame_canvas["ipadx"]]
                                ,["ipady_int",self.dic_frame_canvas["ipady"]],["padx_int",self.dic_frame_canvas["padx grid"]]
                                ,["pady_int",self.dic_frame_canvas["pady grid"]],["rowspan_int",self.dic_frame_canvas["rowspan"]]
                                ,["columnspan_int",self.dic_frame_canvas["columnspan"]],["sticky",self.dic_frame_canvas["sticky"]]]

        return self.dic_frame_canvas["name window"],self.tt_frame_canvas_1,self.tt_frame_canvas_2

class edit_text:
    def __init__(self):
        self.ten_text,self.thuoc_fame,self.font,self.font_size,self.net_chu,self.column,self.row,self.ipadx,self.ipady,self.padx_grid,self.pady_grid = gan_du_lieu(11)
        self.rowspan,self.columnspan,self.sticky,self.thong_tin = gan_du_lieu(4)

        self.dic_text_1 = {"name window":self.ten_text,"thuoc frame":self.thuoc_fame,"font":self.font,"font size":self.font_size,"net chu":self.net_chu,"column":self.column
                             ,"row":self.row,"ipadx":self.ipadx,"ipady":self.ipady,"padx gird":self.padx_grid,"pady gird":self.pady_grid
                             ,"rowspan":self.rowspan,"columnspan":self.columnspan,"sticky":self.sticky,"thong tin":self.thong_tin}
        self.tt_text_1 = [["thuoc_frame",self.dic_text_1["thuoc frame"]],["font",self.dic_text_1["font"]],["font_size",self.dic_text_1["font size"]]
                            ,["net_chu",self.dic_text_1["net chu"]],["thong_tin",self.dic_text_1["thong tin"]]]

        self.tt_text_2 = [["column",self.dic_text_1["column"]],["row_int",self.dic_text_1["row"]],["ipadx_int",self.dic_text_1["ipadx"]]
                            ,["ipady_int",self.dic_text_1["ipady"]],["padx_int",self.dic_text_1["padx gird"]],["pady_int",self.dic_text_1["pady gird"]]
                            ,["rowspan_int",self.dic_text_1["rowspan"]],["columnspan_int",self.dic_text_1["columnspan"]],["sticky",self.dic_text_1["sticky"]]]
    def update_value(self,name="NA",value = "NA"): # input = "name_value"
        if value != "NA":
            try:
                self.dic_text_1[name] = value
            except:
                print("không tồn tại dữ liệu text "+ str(name))
        self.tt_text_1 = [["thuoc_frame",self.dic_text_1["thuoc frame"]],["font",self.dic_text_1["font"]],["font_size",self.dic_text_1["font size"]]
                            ,["net_chu",self.dic_text_1["net chu"]],["thong_tin",self.dic_text_1["thong tin"]]]

        self.tt_text_2 = [["column",self.dic_text_1["column"]],["row_int",self.dic_text_1["row"]],["ipadx_int",self.dic_text_1["ipadx"]]
                            ,["ipady_int",self.dic_text_1["ipady"]],["padx_int",self.dic_text_1["padx gird"]],["pady_int",self.dic_text_1["pady gird"]]
                            ,["rowspan_int",self.dic_text_1["rowspan"]],["columnspan_int",self.dic_text_1["columnspan"]],["sticky",self.dic_text_1["sticky"]]]
        return self.dic_text_1["name window"],self.tt_text_1,self.tt_text_2


class edit_mylist:
    def __init__(self):
        self.ten_frame_mylist,self.thuoc_fame,self.column,self.row,self.ipadx,self.ipady,self.padx_grid,self.pady_grid,self.rowspan,self.columnspan,self.sticky = gan_du_lieu(11)
        self.fg,self.bg,self.text,self.font,self.font_size,self.net_chu,self.width,self.height,self.relief,self.anchor,self.wraplength,self.scrollbar = gan_du_lieu(12)
        self.listbox = gan_du_lieu(1)
        
        self.dic_frame_mylist = {"name window":self.ten_frame_mylist,"thuoc frame":self.thuoc_fame,"column":self.column,"row":self.row,"ipadx":self.ipadx,"ipady":self.ipady
                                 ,"padx grid":self.padx_grid,"pady grid":self.pady_grid,"rowspan":self.rowspan,"columnspan":self.columnspan,"sticky":self.sticky,
                                 "fg":self.fg,"bg":self.bg,"text":self.text,"font":self.font,"font size":self.font_size,"net chu":self.net_chu,"width":self.width,
                                 "height":self.height,"relief":self.relief,"anchor":self.anchor,"wraplength":self.wraplength,"scrollbar":self.scrollbar,"listbox":self.listbox}
        self.tt_frame_mylist_1 = [["thuoc_frame",self.dic_frame_mylist["thuoc frame"]],["font",self.dic_frame_mylist["font"]],["font_size",self.dic_frame_mylist["font size"]]
                            ,["net_chu",self.dic_frame_mylist["net chu"]]]
        self.tt_frame_mylist_2 = [["column_int",self.dic_frame_mylist["column"]],["row_int",self.dic_frame_mylist["row"]],["ipadx_int",self.dic_frame_mylist["ipadx"]]
                                  ,["ipady_int",self.dic_frame_mylist["ipady"]],["padx_int",self.dic_frame_mylist["padx grid"]]
                                  ,["pady_int",self.dic_frame_mylist["pady grid"]],["rowspan_int",self.dic_frame_mylist["rowspan"]]
                                  ,["columnspan_int",self.dic_frame_mylist["columnspan"]],["sticky",self.dic_frame_mylist["sticky"]]]
        self.tt_frame_mylist_3 = [["fg",self.dic_frame_mylist["fg"]],["bg",self.dic_frame_mylist["bg"]],["text",self.dic_frame_mylist["text"]],
                                  ["width",self.dic_frame_mylist["width"]],
                                ["height",self.dic_frame_mylist["height"]],["relief",self.dic_frame_mylist["relief"]],["anchor",self.dic_frame_mylist["anchor"]],
                                ["wraplength",self.dic_frame_mylist["wraplength"]]]
        self.tt_scrollbar = [["scrollbar",self.dic_frame_mylist["scrollbar"]]]
        self.listbox = [["listbox",self.dic_frame_mylist["listbox"]]]
    def update_value(self,name="NA",value = "NA"): # input = "name_value"
        if value != "NA":
            try:
                self.dic_frame_mylist[name] = value
            except:
                print("không tồn tại dữ liệu frame_canvas "+ str(name))
        self.tt_frame_mylist_1 = [["thuoc_frame",self.dic_frame_mylist["thuoc frame"]],["font",self.dic_frame_mylist["font"]],["font_size",self.dic_frame_mylist["font size"]]
                            ,["net_chu",self.dic_frame_mylist["net chu"]]]
        self.tt_frame_mylist_2 = [["column_int",self.dic_frame_mylist["column"]],["row_int",self.dic_frame_mylist["row"]],["ipadx_int",self.dic_frame_mylist["ipadx"]]
                                  ,["ipady_int",self.dic_frame_mylist["ipady"]],["padx_int",self.dic_frame_mylist["padx grid"]]
                                  ,["pady_int",self.dic_frame_mylist["pady grid"]],["rowspan_int",self.dic_frame_mylist["rowspan"]]
                                  ,["columnspan_int",self.dic_frame_mylist["columnspan"]],["sticky",self.dic_frame_mylist["sticky"]]]
        self.tt_frame_mylist_3 = [["fg",self.dic_frame_mylist["fg"]],["bg",self.dic_frame_mylist["bg"]],["text",self.dic_frame_mylist["text"]],
                                  ["width",self.dic_frame_mylist["width"]],
                                ["height",self.dic_frame_mylist["height"]],["relief",self.dic_frame_mylist["relief"]],["anchor",self.dic_frame_mylist["anchor"]],
                                ["wraplength",self.dic_frame_mylist["wraplength"]]]
        self.tt_scrollbar = [["scrollbar",self.dic_frame_mylist["scrollbar"]]]
        self.listbox = [["listbox",self.dic_frame_mylist["listbox"]]]

        return self.dic_frame_mylist["name window"],self.tt_frame_mylist_1,self.tt_frame_mylist_2,self.tt_frame_mylist_3,self.tt_scrollbar,self.listbox

class edit_combobox:
    def __init__(self):
        self.ten_frame_mylist,self.thuoc_fame,self.column,self.row,self.ipadx,self.ipady,self.padx_grid,self.pady_grid,self.rowspan,self.columnspan,self.sticky = gan_du_lieu(11)
        self.state, self.width, self.textvariable,self.ds_combobox, self.stringvar,self.font,self.font_size,self.net_chu = gan_du_lieu(8)
        self.dic_combobox = {"name window":self.ten_frame_mylist,"thuoc frame":self.thuoc_fame,"column":self.column,"row":self.row,"ipadx":self.ipadx,"ipady":self.ipady
                                 ,"padx grid":self.padx_grid,"pady grid":self.pady_grid,"rowspan":self.rowspan,"columnspan":self.columnspan,"sticky":self.sticky,
                                 "state":self.state,"width":self.width, "stringvar":self.stringvar, "textvariable":self.textvariable,"ds combobox":self.ds_combobox,
                                 "font":self.font,"font size":self.font_size,"net chu":self.net_chu}
        self.tt_combobox_1 = [["thuoc_frame",self.dic_combobox["thuoc frame"]],["font",self.dic_combobox["font"]],["font_size",self.dic_combobox["font size"]]
                            ,["net_chu",self.dic_combobox["net chu"]]]
        self.tt_combobox_2 = [["column_int",self.dic_combobox["column"]],["row_int",self.dic_combobox["row"]],["ipadx_int",self.dic_combobox["ipadx"]]
                                  ,["ipady_int",self.dic_combobox["ipady"]],["padx_int",self.dic_combobox["padx grid"]]
                                  ,["pady_int",self.dic_combobox["pady grid"]],["rowspan_int",self.dic_combobox["rowspan"]]
                                  ,["columnspan_int",self.dic_combobox["columnspan"]],["sticky",self.dic_combobox["sticky"]]]
        self.tt_combobox_3 = [["state",self.dic_combobox["state"]],["width",self.dic_combobox["width"]],["textvariable",self.dic_combobox["textvariable"]]
                                  ,["ds_combobox",self.dic_combobox["ds combobox"]],["stringvar",self.dic_combobox["stringvar"]]]
    def update_value(self,name="NA",value = "NA"): # input = "name_value"
        if value != "NA":
            try:
                self.dic_combobox[name] = value
            except:
                print("không tồn tại dữ liệu frame_canvas "+ str(name))
        self.tt_combobox_1 = [["thuoc_frame",self.dic_combobox["thuoc frame"]],["font",self.dic_combobox["font"]],["font_size",self.dic_combobox["font size"]]
                            ,["net_chu",self.dic_combobox["net chu"]]]
        self.tt_combobox_2 = [["column_int",self.dic_combobox["column"]],["row_int",self.dic_combobox["row"]],["ipadx_int",self.dic_combobox["ipadx"]]
                                  ,["ipady_int",self.dic_combobox["ipady"]],["padx_int",self.dic_combobox["padx grid"]]
                                  ,["pady_int",self.dic_combobox["pady grid"]],["rowspan_int",self.dic_combobox["rowspan"]]
                                  ,["columnspan_int",self.dic_combobox["columnspan"]],["sticky",self.dic_combobox["sticky"]]]
        self.tt_combobox_3 = [["state",self.dic_combobox["state"]],["width",self.dic_combobox["width"]],["textvariable",self.dic_combobox["textvariable"]]
                                  ,["ds_combobox",self.dic_combobox["ds combobox"]],["stringvar",self.dic_combobox["stringvar"]]]

        return self.dic_combobox["name window"],self.tt_combobox_1,self.tt_combobox_2,self.tt_combobox_3
class edit_scale:
    def __init__(self):
        self.ten_scale,self.thuoc_fame,self.column,self.row,self.ipadx,self.ipady,self.padx_grid,self.pady_grid = gan_du_lieu(8)
        self.rowspan,self.columnspan,self.sticky,self.from_, self.to, self.orient,self.sliderlength, self.label = gan_du_lieu(8)

        self.dic_scale_1 = {"name window":self.ten_scale,"thuoc frame":self.thuoc_fame,"column":self.column
                             ,"row":self.row,"ipadx":self.ipadx,"ipady":self.ipady,"padx gird":self.padx_grid,"pady gird":self.pady_grid
                             ,"rowspan":self.rowspan,"columnspan":self.columnspan,"sticky":self.sticky,"from":self.from_
                             , "to":self.to, "orient":self.orient, "sliderlength":self.sliderlength, "label":self.label }
        self.tt_scale_1 = [["thuoc_frame",self.dic_scale_1["thuoc frame"]]]

        self.tt_scale_2 = [["column",self.dic_scale_1["column"]],["row_int",self.dic_scale_1["row"]],["ipadx_int",self.dic_scale_1["ipadx"]]
                            ,["ipady_int",self.dic_scale_1["ipady"]],["padx_int",self.dic_scale_1["padx gird"]],["pady_int",self.dic_scale_1["pady gird"]]
                            ,["rowspan_int",self.dic_scale_1["rowspan"]],["columnspan_int",self.dic_scale_1["columnspan"]],["sticky",self.dic_scale_1["sticky"]]]
        self.tt_scale_3 = [["from_int",self.dic_scale_1["from"]],["to_int",self.dic_scale_1["to"]],["orient",self.dic_scale_1["orient"]]
                                  ,["sliderlength_int",self.dic_scale_1["sliderlength"]],["label",self.dic_scale_1["label"]]]
    def update_value(self,name="NA",value = "NA"): # input = "name_value"
        if value != "NA":
            try:
                self.dic_scale_1[name] = value
            except:
                print("không tồn tại dữ liệu text "+ str(name))
        self.tt_scale_1 = [["thuoc_frame",self.dic_scale_1["thuoc frame"]]]

        self.tt_scale_2 = [["column",self.dic_scale_1["column"]],["row_int",self.dic_scale_1["row"]],["ipadx_int",self.dic_scale_1["ipadx"]]
                            ,["ipady_int",self.dic_scale_1["ipady"]],["padx_int",self.dic_scale_1["padx gird"]],["pady_int",self.dic_scale_1["pady gird"]]
                            ,["rowspan_int",self.dic_scale_1["rowspan"]],["columnspan_int",self.dic_scale_1["columnspan"]],["sticky",self.dic_scale_1["sticky"]]]
        self.tt_scale_3 = [["from_int",self.dic_scale_1["from"]],["to_int",self.dic_scale_1["to"]],["orient",self.dic_scale_1["orient"]]
                                  ,["sliderlength_int",self.dic_scale_1["sliderlength"]],["label",self.dic_scale_1["label"]]]
        return self.dic_scale_1["name window"],self.tt_scale_1,self.tt_scale_2,self.tt_scale_3
class edit_all:
    def __init__(self,number=2000):
        self.list_name = []
        for i in range(0,number):
            globals()["self."+str(i)] = ""
            self.list_name.append("")
    def check_find_name_window(self,name_label):
        stt_ok_1 = 0
        stt_ok_0 = 0
        ok_1 = 0
        ok_0 = 0
        exist = 0
        for i in range(0,len(self.list_name)):
            if self.list_name[i] == "" and ok_0 == 0:
                ok_0 = 1
            if ok_0 == 0:
                stt_ok_0 = stt_ok_0 + 1
            if self.list_name[i] != name_label:
                stt_ok_1 = stt_ok_1 + 1
            else:
                ok_1 = 1
                break
        if ok_1 == 1:
            name_window = "self." +str(stt_ok_1)
            exist = 1
        else:
            name_window = "self." +str(stt_ok_0)
        return name_window,exist,stt_ok_0,stt_ok_1
    # def upload(self,tt_window):
    #     for i in range(0,len(tt_window)):
    #         if len(tt_window[i]) > 1:
    #             if len(tt_window[i][1]) > 0:
    #                 if tt_window[i][1][0] == "root":
    #                     name,tt = self.create_root(tt_window[i])
    #                 if tt_window[i][1][0] == "frame":
    #                     name,tt1,tt2,tt3 =self.create_frame(tt_window[i])
    #                 if tt_window[i][1][0] == "label":
    #                     name,tt1,tt2,tt3 = self.create_label(tt_window[i])
    #                 if tt_window[i][1][0] == "entry":
    #                     name,tt1,tt2,tt3 = self.create_entry(tt_window[i])
    #                 if tt_window[i][1][0] == "checkbutton":
    #                     name,tt1,tt2,tt3 = self.create_checkbutton(tt_window[i])
    #                 if tt_window[i][1][0] == "radiobutton":
    #                     name,tt1,tt2,tt3 = self.create_radiobutton(tt_window[i])
    #                 if tt_window[i][1][0] == "button":
    #                     name,tt1,tt2,tt3 = self.create_button(tt_window[i])
    #                 if tt_window[i][1][0] == "canvas":
    #                     name,tt1,tt2,tt3,tt_scrollbar,tt_button = self.create_canvas(tt_window[i])
    #                 if tt_window[i][1][0] == "frame canvas":
    #                     name,tt1,tt2 = self.create_frame_canvas(tt_window[i])
    def create_root(self,tt_window):
        name_window,exist,stt_ok_0,stt_ok_1 = self.check_find_name_window(tt_window[0][1])
        if exist == 0:
            globals()[name_window] = edit_root()
        for i2 in range(0,len(tt_window)):
            name,tt = globals()[name_window].update_value(tt_window[i2][0],tt_window[i2][1])
        return name,tt

    def create_frame(self,tt_window):
        name_window,exist,stt_ok_0,stt_ok_1 = self.check_find_name_window(tt_window[0][1])
        if exist == 0:
            globals()[name_window] = edit_frame()
        for i2 in range(0,len(tt_window)):
            name,tt1,tt2,tt3 = globals()[name_window].update_value(tt_window[i2][0],tt_window[i2][1])
        return name,tt1,tt2,tt3

    def create_label(self,tt_window):
        name_window,exist,stt_ok_0,stt_ok_1 = self.check_find_name_window(tt_window[0][1])
        if exist == 0:
            globals()[name_window] = edit_label()
        for i2 in range(0,len(tt_window)):
            name,tt1,tt2,tt3 = globals()[name_window].update_value(tt_window[i2][0],tt_window[i2][1])
        return name,tt1,tt2,tt3
    def create_button(self,tt_window):
        name_window,exist,stt_ok_0,stt_ok_1 = self.check_find_name_window(tt_window[0][1])
        if exist == 0:
            globals()[name_window] = edit_button()
        for i2 in range(0,len(tt_window)):
            name,tt1,tt2,tt3 = globals()[name_window].update_value(tt_window[i2][0],tt_window[i2][1])
        return name,tt1,tt2,tt3
    def create_entry(self,tt_window):
        name_window,exist,stt_ok_0,stt_ok_1 = self.check_find_name_window(tt_window[0][1])
        if exist == 0:
            globals()[name_window] = edit_entry()
        for i2 in range(0,len(tt_window)):
            name,tt1,tt2,tt3 = globals()[name_window].update_value(tt_window[i2][0],tt_window[i2][1])
        return name,tt1,tt2,tt3
    def create_checkbutton(self,tt_window):
        name_window,exist,stt_ok_0,stt_ok_1 = self.check_find_name_window(tt_window[0][1])
        if exist == 0:
            globals()[name_window] = edit_checkbutton()
        for i2 in range(0,len(tt_window)):
            name,tt1,tt2,tt3 = globals()[name_window].update_value(tt_window[i2][0],tt_window[i2][1])
        return name,tt1,tt2,tt3
    def create_radiobutton(self,tt_window):
        name_window,exist,stt_ok_0,stt_ok_1 = self.check_find_name_window(tt_window[0][1])
        if exist == 0:
            globals()[name_window] = edit_radiobutton()
        for i2 in range(0,len(tt_window)):
            name,tt1,tt2,tt3 = globals()[name_window].update_value(tt_window[i2][0],tt_window[i2][1])
        return name,tt1,tt2,tt3
    def create_canvas(self,tt_window):
        name_window,exist,stt_ok_0,stt_ok_1 = self.check_find_name_window(tt_window[0][1])
        if exist == 0:
            globals()[name_window] = edit_canvas()
        for i2 in range(0,len(tt_window)):
            name,tt1,tt2,tt3,tt_scrollbar,tt_button,new_canvas,remove_button,update_button = globals()[name_window].update_value(tt_window[i2][0],tt_window[i2][1])
        return name,tt1,tt2,tt3,tt_scrollbar,tt_button,new_canvas,remove_button,update_button
    def create_frame_canvas(self,tt_window):
        name_window,exist,stt_ok_0,stt_ok_1 = self.check_find_name_window(tt_window[0][1])
        if exist == 0:
            globals()[name_window] = edit_frame_canvas()
        for i2 in range(0,len(tt_window)):
            name,tt1,tt2 = globals()[name_window].update_value(tt_window[i2][0],tt_window[i2][1])
        return name,tt1,tt2
    def create_menu(self,tt_window):
        name_window,exist,stt_ok_0,stt_ok_1 = self.check_find_name_window(tt_window[0][1])
        if exist == 0:
            globals()[name_window] = menu()
        for i2 in range(0,len(tt_window)):
            tt = globals()[name_window].update_value(tt_window[i2][0],tt_window[i2][1])
        return tt
    def create_mylist(self,tt_window):
        name_window,exist,stt_ok_0,stt_ok_1 = self.check_find_name_window(tt_window[0][1])
        if exist == 0:
            globals()[name_window] = edit_mylist()
        for i2 in range(0,len(tt_window)):
            name,tt1,tt2,tt3,scrollbar,listbox = globals()[name_window].update_value(tt_window[i2][0],tt_window[i2][1])
        return name,tt1,tt2,tt3,scrollbar,listbox
    def create_combobox(self,tt_window):
        name_window,exist,stt_ok_0,stt_ok_1 = self.check_find_name_window(tt_window[0][1])
        if exist == 0:
            globals()[name_window] = edit_combobox()
        for i2 in range(0,len(tt_window)):
            name,tt1,tt2,tt3 = globals()[name_window].update_value(tt_window[i2][0],tt_window[i2][1])
        return name,tt1,tt2,tt3
    def create_text(self,tt_window):
        name_window,exist,stt_ok_0,stt_ok_1 = self.check_find_name_window(tt_window[0][1])
        if exist == 0:
            globals()[name_window] = edit_text()
        for i2 in range(0,len(tt_window)):
            name,tt1,tt2 = globals()[name_window].update_value(tt_window[i2][0],tt_window[i2][1])
        return name,tt1,tt2
    def create_scale(self,tt_window):
        name_window,exist,stt_ok_0,stt_ok_1 = self.check_find_name_window(tt_window[0][1])
        if exist == 0:
            globals()[name_window] = edit_scale()
        for i2 in range(0,len(tt_window)):
            name,tt1,tt2,tt3 = globals()[name_window].update_value(tt_window[i2][0],tt_window[i2][1])
        return name,tt1,tt2,tt3
        # 
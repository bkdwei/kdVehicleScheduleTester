'''
Created on 2019年6月12日

@author: bkd
'''
from tkinter.simpledialog import askstring

from kdGUI import *

from .data_handler import data_handler
from .exception_handler import set_global_callback
from .fileutil import load_josn_config, save_json_config


class kdVehicleScheduleTester(Window):
    
    def __init__(self):
        super().__init__()
        self.setTitle("车辆调度检测器")
        
        self.data_handler = data_handler()
        self._init_ui()
        self._bind_event()
        self.load_config()
        set_global_callback(self)
        self.run()

    def _init_ui(self):
        self.setGeometry(500, 300)
        
        self.setLayout(VERTICAL)
#         self = VerticalLayout("", self)
#         self.addWidget(self)
        
#         数据库配置
        self.hl_db = HorizontalLayout("数据库配置", self)
        self.addWidget(self.hl_db)
        self.lb_db_addr = Label("数据库地址", self.hl_db)
        self.le_db_addr = LineEdit("localhost;3306;car2018;kde#2018;carCheck", self.hl_db)
        self.le_db_addr.setHideInput("*")
        self.hl_db.addWidget(self.lb_db_addr)
        self.hl_db.addWidget(self.le_db_addr)
        
#         按钮配置
        self.hl_button = HorizontalLayout("", self)
        self.addWidget(self.hl_button)
        self.pb_add = PushButton("新增", self.hl_button)
        self.pb_del = PushButton("删除", self.hl_button)
        self.pb_edit = PushButton("更改", self.hl_button)
        self.pb_query = PushButton("查询", self.hl_button)
        self.pb_connect_db = PushButton("连接数据库", self.hl_button)
        self.hl_button.addWidget(self.pb_add)
        self.hl_button.addWidget(self.pb_del)
        self.hl_button.addWidget(self.pb_edit)
        self.hl_button.addWidget(self.pb_query)
        self.hl_button.addWidget(self.pb_connect_db)
        
#         车辆列表和检测项目
        self.hl_content = HorizontalLayout("", self)
        self.addWidget(self.hl_content, expand=YES)
        self.lw_cars = ListWidget(self.hl_content)
        self.hl_content.addWidget(self.lw_cars)
#         self.lw_cars.addItem("粤BKD034")
#         self.lw_cars.addItem("粤BKD035")
#         self.lw_cars.addItem("粤BKD036")
        
        self.gl_test_subitem = GridLayout("", self.hl_content)
        self.hl_content.addWidget(self.gl_test_subitem)
        
        self.cb_ground = CheckButton("地沟", self.gl_test_subitem)
        self.cb_speed = CheckButton("车速", self.gl_test_subitem)
        self.cb_left_out_far_lamp = CheckButton("左外远灯", self.gl_test_subitem)
        self.cb_right_out_far_lamp = CheckButton("右外远灯", self.gl_test_subitem)
        self.cb_left_out_near_lamp = CheckButton("左外近灯", self.gl_test_subitem)
        self.cb_right_out_near_lamp = CheckButton("右外近灯", self.gl_test_subitem)
        self.cb_slide = CheckButton("侧滑", self.gl_test_subitem)
        self.cb_first_weight = CheckButton("一轴", self.gl_test_subitem)
        self.cb_second_weight = CheckButton("二轴", self.gl_test_subitem)
        self.cb_first_brake = CheckButton("一制", self.gl_test_subitem)
        self.cb_second_brake = CheckButton("二制", self.gl_test_subitem)
        
        self.cb_ground.setData("ground")
        self.cb_speed.setData("speed")
        self.cb_left_out_far_lamp.setData("lahLamp")
        self.cb_right_out_far_lamp.setData("rahLamp")
        self.cb_left_out_near_lamp.setData("llLamp")
        self.cb_right_out_near_lamp.setData("rlLamp")
        self.cb_slide.setData("slide")
        self.cb_first_weight.setData("weight1")
        self.cb_second_weight.setData("weight2")
        self.cb_first_brake.setData("brake1")
        self.cb_second_brake.setData("brake2")
        
        self.gl_test_subitem.addWidget(self.cb_ground, 0, 0)
        self.gl_test_subitem.addWidget(self.cb_speed, 1, 0)
        self.gl_test_subitem.addWidget(self.cb_slide, 2, 0)
        self.gl_test_subitem.addWidget(self.cb_left_out_far_lamp, 0, 1)
        self.gl_test_subitem.addWidget(self.cb_right_out_far_lamp, 1, 1)
        self.gl_test_subitem.addWidget(self.cb_left_out_near_lamp, 2, 1)
        self.gl_test_subitem.addWidget(self.cb_right_out_near_lamp, 3, 1)
        self.gl_test_subitem.addWidget(self.cb_first_weight, 0, 2)
        self.gl_test_subitem.addWidget(self.cb_second_weight, 1, 2)
        self.gl_test_subitem.addWidget(self.cb_first_brake, 2, 2)
        self.gl_test_subitem.addWidget(self.cb_second_brake, 3, 2)

    def load_config(self):
        config = load_josn_config(self.__class__.__name__)
        print(self.__class__.__name__)
        if config:
            self.le_db_addr.setText(config["db_addr"])
            for car in config["cars"]:
                self.lw_cars.addItems(car)
            self.config = config
        else:
            self.config = {"db_addr":None, "cars":[]}

    def _bind_event(self):
        self.pb_add.click(self.add_car)
        self.pb_del.click(self.del_car)
        self.pb_connect_db.click(self.init_db_connection)
        self.pb_query.click(self.query_test_subitem)
        self.pb_edit.click(self.alter_subItem_list)

    def add_car(self):
        new_car = askstring("新增车辆", "请输入车牌号，'粤'字不用输入")
        if not new_car:
            return 
        if not "粤" in new_car:
            new_car = "粤" + new_car 
        self.lw_cars.addItem(new_car)
        self.config["cars"].append(new_car)
        save_json_config(self.__class__.__name__, self.config)

    def del_car(self):
        cur_cars = self.lw_cars.curselection()
        if cur_cars:
            item = self.lw_cars.currentItem()
            self.config["cars"].remove(self.lw_cars.currentItem())
            self.lw_cars.removeItemWidget(cur_cars[0], cur_cars[-1])
            save_json_config(self.__class__.__name__, self.config)

    def init_db_connection(self):
        db_addr = self.le_db_addr.text()
        if db_addr:
            self.data_handler.init_connect(db_addr.split(";"))
            self.config["db_addr"] = db_addr
            save_json_config(self.__class__.__name__, self.config)
            self.showMessage("连接数据成功")

    def query_test_subitem(self):
        cur_car = self.lw_cars.currentItem()
        if cur_car:
            sequence_code, subitem_list = self.data_handler.query_test_subitem(cur_car)
            self.showMessage("过线号:" + sequence_code)
            print(subitem_list)
            self.set_test_subitems(subitem_list)

    def set_test_subitems(self, item_list):
        children = self.gl_test_subitem.childrens()
        for child in children:
            child.setChecked(False)
        for item1 in item_list:
            item = item1[0]
            if item == "speed":
                self.cb_speed.setChecked(True)
            elif item == "ground":
                self.cb_ground.setChecked(True)
            elif item == "lahLamp":
                self.cb_left_out_far_lamp.setChecked(True)
            elif item == "rahLamp":
                self.cb_right_out_far_lamp.setChecked(True)
            elif item == "llLamp":
                self.cb_left_out_near_lamp.setChecked(True)
            elif item == "rlLamp":
                self.cb_right_out_near_lamp.setChecked(True)
            elif item == "weight1":
                self.cb_first_weight.setChecked(True)
            elif item == "weight2":
                self.cb_second_weight.setChecked(True)
            elif item == "slide":
                self.cb_slide.setChecked(True)
            elif item == "brake1":
                self.cb_first_brake.setChecked(True)
            elif item == "brake2":
                self.cb_second_brake.setChecked(True)

    def alter_subItem_list(self):
        vehicle_number = self.lw_cars.currentItem()
        item_list = []
        children = self.gl_test_subitem.childrens()
        for child in children:
            if child.isChecked():
                item_list.append(child.data())
        self.data_handler.alter_subItem(vehicle_number, item_list)
        self.showMessage("更改的'{}'检测项目成功".format(vehicle_number))
            

def main():
    root = kdVehicleScheduleTester()
    root.run()

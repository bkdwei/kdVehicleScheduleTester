'''
Created on 2019年6月12日

@author: bkd
'''
import uuid

import MySQLdb


class data_handler(object):
    '''
    操作数据库的类
    '''

    def __init__(self):
        '''
        '''
#         self.init_connect(confs)
        
    def init_connect(self, confs):
        self.db = MySQLdb.connect(host=confs[0], port=int(confs[1]), user=confs[2], passwd=confs[3], db=confs[4], charset='utf8')
        self.cursor = self.db.cursor()

    def query_test_subitem(self, vehile_number):
        self.cursor.execute("""
select
    sequence_code 
from
    vehicle_test_info a
where
    a.sequence_code like '{}%'
    and a.del_flag = 0

        """.format(vehile_number))
        sequence_code = self.cursor.fetchone()[0]
        print(sequence_code)
        self.cursor.execute("""
select
    a.subItem 
from
    vehicle_test_item a
where
    a.sequence_code = '{}'
    and a.del_flag = 0
order by
    a.test_times desc,a.bigItem,a.subItem
        """.format(sequence_code))
        return sequence_code, self.cursor.fetchall()
    
    def alter_subItem(self, vehicle_number, item_list):
        self.cursor.execute("""
select
    vehicle_id,
    test_times,
    test_code,
    sequence_code 
from
    vehicle_test_info a
where
    a.sequence_code like '{}%'
    and a.del_flag = 0
    order by test_times desc
    limit 1

        """.format(vehicle_number))
        test_info = self.cursor.fetchone()
        vehicle_id = test_info[0]
        test_times = test_info[1]
        test_code = str(test_info[2])
        sequence_code = str(test_info[3])
        
        # 更新上线标志
        self.cursor.execute(("""
update  
    vehicle_test_info
set
    up_line_flag = 1
where 
    sequence_code ='{}'
""").format(sequence_code))   
        self.cursor.execute(("""
delete from
    vehicle_test_item
where 
    sequence_code = '{}'
""").format(sequence_code))

        for item in item_list:
            bigItem = None
            if item == "ground" :
                bigItem = "ground"
            elif item == "speed":
                bigItem = "speed"
            elif item in ["lahLamp", "rahLamp", "llLamp", "rlLamp"]:
                bigItem = "light"
            elif item in ["weight1", "weight2"]:
                bigItem = "weight"
            elif item in ["brake1", "brake2"]:
                bigItem = "brake"
                
            insert_sql = ("""
insert
    into
        vehicle_test_item ( 
        id,
        vehicle_id,
        test_code,
        qcmt_flag,
        bigItem,
        bigItem_status,
        subItem,
        subItem_status,
        del_flag,
        test_times,
        sequence_code,
        create_date,
        update_date,
        police_status)
    values( '{}',
    '{}',
    '{}',
    1,
    '{}',
    3,
    '{}',
    3,
    '0',
    '{}',
    '{}',
    '2019-05-10 17:01:03',
    '2019-05-10 17:01:03',
    0);
""").format(str(uuid.uuid1()), vehicle_id, test_code, bigItem, item, test_times, sequence_code)
            print("insert_sql：" + insert_sql)
            self.cursor.execute(insert_sql)
        self.db.commit()

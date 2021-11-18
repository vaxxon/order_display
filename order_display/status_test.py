url = 'https://odoo13.btlps.com'
db = 'BTL_Master_V13'
username = 'vincent@btlps.com'
password = 'mush0WRIW2ceem.lil'

import xmlrpc.client
import pytz, datetime
import pprint

common = xmlrpc.client.ServerProxy('%s/xmlrpc/2/common' % url)
version = common.version() 
uid = common.authenticate(db, username, password, version)
models = xmlrpc.client.ServerProxy('%s/xmlrpc/2/object' % url)

# Convert Odoo standard UTC timezone to EST

def convert_utc_est(time):
    utc = pytz.timezone("UTC")
    eastern = pytz.timezone("US/Eastern")
    time_utc = utc.localize(time)
    time_est = time_utc.astimezone(eastern)
    
    return time_est

# Get today's date, convert to EST, & format

# Odoo filter lists

open_state = ['confirmed', 'assigned']
not_internal = [2, 3, 4]

# To Pick

# Create a list of orders with picks scheduled for today

# Collect information: name, partner, scheduled pickup time, scheduled pickup date, scheduled return date, salesperson, picking IDs.

#to_pick_data = models.execute_kw(db, uid, password,
#    'sale.order', 'search_read',
#    [[['picking_date', 'like', today]]],
#    {'fields': ['name', 'partner_id', 'picking_date','return_date', 'user_id', 'picking_ids']}
#)

# For each picking_id, collect priority, operation type, status of each operation in each operation type, number of each status of each operation type.

# Or go backwards... collect any ready or waiting picks, collect all documents in the procurement group, relate back to sales order, get information from that model.

today = convert_utc_est(datetime.datetime.now())
today_str = today.strftime("%Y-%m-%d%%")
this_year = today.strftime("%Y-%%-%%")
day_date = today.strftime("%A, %B %d, %Y • %I:%M:%S %p ")

receipt_data = models.execute_kw(db, uid, password,
    'stock.picking', 'search_read',
    [['&', ('scheduled_date', 'like', this_year), ('state', 'in', open_state), ('picking_type_id', '=', 1)]],
    {'fields': ['name', 'partner_id', 'scheduled_date', 'picking_type_id', 'origin', 'state', 'activity_ids', 'activity_type_id'], 'order': 'scheduled_date desc'}
)

activity_list = []
run_data = []

def str_to_dt(str):
    dateobj = datetime.datetime.strptime(str, '%Y-%m-%d %H:%M:%S')
    dateobj = convert_utc_est(dateobj).strftime('%a %b %d')
    return dateobj

def str_to_time(str):
    timeobj = datetime.datetime.strptime(str, '%Y-%m-%d %H:%M:%S')
    timeobj = convert_utc_est(timeobj).strftime('%I:%M %p')
    return timeobj

def fix_time(data):
    for x in data:
        x['time'] = str_to_time(x['scheduled_date'])
        x['scheduled_date'] = str_to_dt(x['scheduled_date'])

def status(data):
    
    # Fetch group_id and use it to match other picks with same group
    # Get their operation type, status
    # Add to dictionary...
    # pass to JS for formatting
    
    def str_to_dt(str):
        dateobj = datetime.datetime.strptime(str, '%Y-%m-%d %H:%M:%S')
        dateobj = dateobj.strftime('%a %b %d')
        return dateobj

    def str_to_time(str):
        timeobj = datetime.datetime.strptime(str, '%Y-%m-%d %H:%M:%S')
        timeobj = timeobj.strftime('%I:%M %p')
        return timeobj
    
    for x in data:
        if x['picking_type_id'][0] != 1:
            pro_group = x['group_id'][0]
            so_name = x['origin']
            waiting_picks = models.execute_kw(db, uid, password,
                'stock.picking', 'search_count',
                [['&', ('state', '=', 'confirmed'), ('group_id', '=', pro_group), ('picking_type_id', '=', 3)]])
            done_picks = models.execute_kw(db, uid, password,
                'stock.picking', 'search_count',
                [['&', ('state', '=', 'done'), ('group_id', '=', pro_group), ('picking_type_id', '=', 3)]])
            so_pu_date = models.execute_kw(db, uid, password,
                'sale.order', 'search_read',
                [[['name','=', so_name]]], {'fields': ['commitment_date']})
            so_ret_date = models.execute_kw(db, uid, password,
                'sale.order', 'search_read',
                [[['name','=', so_name]]], {'fields': ['return_date']})
            so_user = models.execute_kw(db, uid, password,
                'sale.order', 'search_read',
                [[['name','=', so_name]]], {'fields': ['user_id']})
                
            x['return_date'] = str_to_dt(so_ret_date[0]['return_date'])
            x['pickup_date'] = str_to_dt(so_pu_date[0]['commitment_date'])
            x['waiting_picks'] = waiting_picks
            x['done_picks'] = done_picks
            x['user_id'] = so_user
            x['scheduled_date'] = str_to_time(x['scheduled_date'])
            
            if x['activity_ids']:
                for i in x['activity_ids']:
                    activity_list.append([i, so_name, x['partner_id'][1]])
        else:
            so_name = x['origin']
            
            if x['activity_ids']:
                for i in x['activity_ids']:
                    activity_list.append([i, so_name, x['partner_id'][1]])

def fetch_activities(data):
    for x in data:
        l = models.execute_kw(db, uid, password,
            'mail.activity', 'search_read',
            [[('id', '=', x[0])]],
            {'fields': ['activity_type_id', 'res_name', 'note', 'user_id', 'x_studio_delivery_time'], 'order': 'x_studio_delivery_time desc'}
        )
        l[0]['origin'] = x[1]
        l[0]['partner_id'] = x[2]
        l[0]['time'] = str_to_time(l[0]['x_studio_delivery_time'])
        l[0]['scheduled_date'] = str_to_dt(l[0]['x_studio_delivery_time'])
        run_data.append(l[0])
        #print (l)
        
        
status(receipt_data)
fetch_activities(activity_list)

pprint.pprint(receipt_data)
pprint.pprint(activity_list)
pprint.pprint(run_data)
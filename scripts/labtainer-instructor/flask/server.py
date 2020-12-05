#!/usr/bin/env python3
'''
This software was created by United States Government employees at 
The Center for Cybersecurity and Cyber Operations (C3O) 
at the Naval Postgraduate School NPS.  Please note that within the 
United States, copyright protection is not available for any works 
created  by United States Government employees, pursuant to Title 17 
United States Code Section 105.   This software is in the public 
domain and is not subject to copyright. 
Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions
are met:
  1. Redistributions of source code must retain the above copyright
     notice, this list of conditions and the following disclaimer.
  2. Redistributions in binary form must reproduce the above copyright
     notice, this list of conditions and the following disclaimer in the
     documentation and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT,
INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.
'''
from flask import Flask, render_template, url_for, send_file, Response, request
import json
import sys
import os
import glob
import argparse
from flask_table import Table, Col, LinkCol, create_table, NestedTableCol

'''
Use the Flask framework to create dynamic web pages displaying student goals
and the intermediate results and raw artifacts.
'''

class HackLinkCol(LinkCol):
    def td_format(self, content):
        if ':' in content:
            return content.rsplit(':', 1)[1]
        else:
            return content
class HackCol(Col):
    def td_format(self, content):
        if ':' in content:
            return content.rsplit(':', 1)[1]
        else:
            return content

global raw_fpath
parser = argparse.ArgumentParser(description='Grade a Labtainers lab')
parser.add_argument('labname', help='The lab to grade')
parser.add_argument('-t', '--test', action='store_true', help='Use test directory.')
args = parser.parse_args()
lab = args.labname
app = Flask(__name__)
if args.test:
    data_dir = '/home/mike/tmp'
    lab_dir = os.path.join(data_dir, lab)
else:
    lab_dir = os.getenv('HOME')

tbl_options = dict(no_items='Empty',   border='1px solid black')

def getGoalDoc():
    retval = ''
    fname = '%s.grades.txt' % lab
    grade_file = os.path.join(lab_dir, fname)
    with open(grade_file) as fh:
        got_it = False
        for line in fh:
            if got_it:
                line = retval + line
            if line.startswith('What is automatically'):
                got_it = True
                retval = line
    return retval

@app.route('/grades')
def grades():

    json_fname = '%s.grades.json' % lab
    grade_json = os.path.join(lab_dir, json_fname)
    rows = []
    #TableCls = create_table('TableCls')\
    #        .add_column('name', Col('Name'))
    GoalTableCls = create_table('GoalTableCls', options=tbl_options)\
            .add_column('name', LinkCol('Name', 'student_select',
                   url_kwargs=dict(student_id='student_id'), attr='name'))

    goals_list = getGoalsList()
    with open(grade_json) as fh:
        grade_dict = json.load(fh)
        first_key = list(grade_dict.keys())[0]
        for goal in grade_dict[first_key]['grades']:
            if not goal.startswith('_') and not goal.startswith('cw_'):
                #GoalTableCls.add_column(goal, Col(goal))
                if goal in goals_list:
                    GoalTableCls.add_column(goal, HackLinkCol(goal, 'goal_select',
                       url_kwargs=dict(student_id='student_id', goal=goal, timestamp='timestamp'), attr=goal))
                else:
                    GoalTableCls.add_column(goal, HackLinkCol(goal, 'bool_result_select',
                       url_kwargs=dict(student_id='student_id', 
                       result=goal), attr=goal))
        for student in grade_dict:
            row = {}
            parts = student.split('_at_')
            row['name'] = parts[0]
            row['student_id'] = student
            row['timestamp'] = 'None'
            for key in grade_dict[student]['grades']:
                if not key.startswith('_') and not key.startswith('cw_'):
                    row[key] = '%s:%s' % (key, grade_dict[student]['grades'][key])
            rows.append(row)
        tbl = GoalTableCls(rows) 
            
        goal_doc = getGoalDoc()
    return render_template('grades.html', lab=lab, table=tbl, goal_doc=goal_doc, 
           goals_config=url_for('goals_config'))

def findTS(student_dir, student_id, container_list, ts, search_string):
    glob_mask = '*.%s' % ts
    sub_tbl = []
    student_dir = os.path.join(lab_dir, student_id)
    for container_id in container_list:
        result_dir = os.path.join(student_dir, container_id, '.local', 'result')
        ts_list = glob.glob(os.path.join(result_dir, glob_mask))
        container = container_id.split('.')[1]
        for ts_path in ts_list:
            if len(search_string) > 0:
                with open(ts_path) as fh:
                    data = fh.read()
                    if search_string not in data:
                        continue
                
            row = {}
            ts = os.path.basename(ts_path) 
            fname = ts.rsplit('.',1)[0]
            row['container'] = container
            row['container_id'] = container_id
            row['fname'] = fname
            row['timestamp'] = ts
            row['result_dir'] = result_dir
            row['student_id'] = student_id
            row['search_string'] = search_string
            sub_tbl.append(row)
    return sub_tbl

class RawSubTable(Table):
    container = Col('')
    fname = LinkCol('', 'raw_select',
               url_kwargs=dict(student_id='student_id',container_id='container_id',
                  ts='timestamp', fname='fname'), attr='fname')

def getTSTable(student_id, result_id):
    student_dir = os.path.join(lab_dir, student_id)
    student_inter_dir = os.path.join(student_dir, '.local','result')

    container_list = os.listdir(student_dir)
    
    TS_TableCls = create_table('TS_TableCls', options=tbl_options)\
            .add_column('timestamp', LinkCol('timestamp', 'ts_select',
                   url_kwargs=dict(ts='timestamp', student_id='student_id'), attr='timestamp'))
    if result_id is not None:
        #TS_TableCls.add_column('result_value', Col(result_id))
        TS_TableCls.add_column('result_value', HackLinkCol(result_id, 'result_select',
                   url_kwargs=dict(student_id='student_id', timestamp='timestamp', 
                   result='result_id'), attr='result_value'))

    TS_TableCls.add_column('raw_links', NestedTableCol('Raw artifacts', RawSubTable))
    search_string = request.form.get('search')
    if search_string is None:
        search_string = ''
    else: 
        search_string = search_string.strip()

    glob_mask = '%s.*' % lab 
    ts_list = glob.glob(os.path.join(student_inter_dir, glob_mask))
    ts_rows = []
    for ts in ts_list:
        base = os.path.basename(ts)
        ts_suffix = base.rsplit('.')[-1]
        raw_tbl = findTS(student_dir, student_id, container_list, ts_suffix, search_string)
        if len(raw_tbl) > 0:
            row = {}
            row['timestamp'] = ts_suffix
            if result_id is not None:
                ts_file = '%s.%s' % (lab, ts_suffix)
                ts_path = os.path.join(student_inter_dir, ts_file)
                with open(ts_path) as fh:
                    ts_json = json.load(fh)
                    if result_id in ts_json:
                        if len(ts_json[result_id].strip()) == 0 or ts_json[result_id]=="''":
                            row['result_value'] = 'empty'
                        else:
                            row['result_value'] = ts_json[result_id]
                        row['result_id'] = result_id
                    else:
                        continue
            row['raw_links'] = raw_tbl
            row['student_id'] = student_id
            ts_rows.append(row)
    if len(ts_rows) > 0:
        ts_tbl = TS_TableCls(ts_rows)
    else:
        ts_tbl = None
    return ts_tbl, search_string
            
@app.route('/grades/bool_result/<string:student_id>/<result>', methods=['GET', 'POST'])
def bool_result_select(student_id, result):
    if ':' in result:
        result_id = result.split(':')[0].strip() 
    else:
        result_id = result
    ts_tbl, search_string = getTSTable(student_id, result_id)
    student_email = student_id.rsplit('.', 1)[0]
    return render_template('bool_result.html', student_email=student_email, result_id=result, ts_table=ts_tbl, 
              search_string=search_string, back_grades=url_for('grades'))

@app.route('/grades/<string:student_id>', methods=['GET', 'POST'])
def student_select(student_id):

    ts_tbl, search_string = getTSTable(student_id, None)
    student_dir = os.path.join(lab_dir, student_id)

    hist_list = []
    container_list = os.listdir(student_dir)
    for full_container in container_list:
        if os.path.isfile(os.path.join(student_dir, full_container, '.bash_history')):
            container = full_container.split('.')[1]
            url = 'history/%s/%s' % (student_id, full_container)
            entry = [container, url]
            hist_list.append(entry)

    student_email = student_id.rsplit('.', 1)[0]
    return render_template('student.html', student_email=student_email, ts_table = ts_tbl, 
          hist_list = hist_list, search_string=search_string, back_grades=url_for('grades'),
          goals_json=url_for('goals_json', student_id=student_id))

@app.route('/grades/ts/<student_id>/<string:ts>')
def ts_select(student_id, ts):
    student_dir = os.path.join(lab_dir, student_id)
    student_inter_dir = os.path.join(student_dir, '.local','result')
    ts_file = '%s.%s' % (lab, ts)
    ts_path = os.path.join(student_inter_dir, ts_file)
    with open(ts_path) as fh:
        data = fh.read()
    
    student_email = student_id.rsplit('.', 1)[0]
    return render_template('ts.html', student_id=student_email, ts=ts, data = data, back_grades=url_for('grades'))
    
@app.route('/grades/<student_id>/goals_json')
def goals_json(student_id):
    student_dir = os.path.join(lab_dir, student_id)
    student_inter_dir = os.path.join(student_dir, '.local','result')
    goals_path = os.path.join(student_inter_dir, 'goals.json')
    with open(goals_path) as fh:
        data = fh.read()
    
    student_email = student_id.rsplit('.', 1)[0]
    return render_template('goals_json.html', student_id=student_email, data = data, back_grades=url_for('grades'))
    

@app.route('/grades/history/<student_id>/<container_id>')
def history(student_id, container_id):
   
    container_history = os.path.join(lab_dir, student_id, container_id, '.bash_history')
    with open(container_history) as fh:
        data = fh.read()
    
    student_email = student_id.rsplit('.', 1)[0]
    return render_template('history.html', student_id=student_email, data = data, back_grades=url_for('grades'))

@app.route('/grades/raw/<student_id>/<container_id>/<ts>/<fname>')
def raw_select(student_id, container_id, ts, fname):
    global raw_fpath
    print('IN raw select')
    result_dir = os.path.join(lab_dir, student_id, container_id, '.local', 'result')
    if ts == 'None':
        ts_fname = raw_fpath[1:]
        fname = raw_fpath
    else:
        ts_fname = '%s.%s' % (fname, ts)
    path = os.path.join(result_dir, ts_fname)
    with open(path) as fh:
        data = fh.read()
    
    container = container_id.split('.')[1]
    student_email = student_id.rsplit('.', 1)[0]
    return render_template('raw.html', lab=lab, student_id=student_email, timestamp=ts, fname=fname, 
          container=container,data = data, back_grades=url_for('grades'))


def getGoal(goals_json, goal_id):
    for goal_entry in goals_json:
        if goal_entry['goalid'] == goal_id:
            return goal_entry
    return None

def getBoolTable(student_id, student_inter_dir, goal_id, goals_json, bool_tbl_list, did_these):
    print('bool table')
    bool_json_file = 'bool_%s.json' % goal_id
    bool_json_path = os.path.join(student_inter_dir, bool_json_file)
    with open(bool_json_path) as fh:
        bool_json = json.load(fh)
    ''' list of all potential boolan goals/results for this goal'''
    bool_json_keys = []
    for ts in bool_json:
        for key in bool_json[ts]:
            if key not in bool_json_keys:
                bool_json_keys.append(key)

    ''' table for boolen expression values '''
    BoolExpTableCls = create_table('BoolExpTableCls', options = tbl_options)
    BoolExpTableCls.add_column('timestamp', Col('Timestamp'))

    ''' list (single column table) of boolean goals that have no results '''
    MissingBoolTableCls = create_table('MissingBoolTableCls', options = tbl_options)
    MissingBoolTableCls.add_column('missing goal results', HackLinkCol('Goals lacking results', 'goal_select',
                   url_kwargs=dict(student_id='student_id', goal='missing_goal', timestamp='timestamp'), attr='missing_goal'))
    missing_goal_rows = []

    goal_entry = getGoal(goals_json, goal_id) 
    bool_string = goal_entry['boolean_string'] 
    ''' hack to ensure whitespace before and after each item in expression '''
    the_string = bool_string.replace('(', ' ')
    the_string = the_string.replace(')', ' ')
    ''' order table based on order of items in the expression '''
    item_list = the_string.split(' ')
    ''' generate list of columns so we can exclude rows that lack corresponding values '''
    columns = []
    ''' Identify the tokens in expression that are goals/results '''
    for item in item_list:
        item = item.strip()
        print('item is %s' % item)
        if item in bool_json_keys:
            columns.append(item)
            goal_entry = getGoal(goals_json, item)
            if goal_entry is None:
                print(' is none')
                BoolExpTableCls.add_column(item, HackLinkCol(item, 'result_select',
                   url_kwargs=dict(student_id='student_id', timestamp='timestamp', 
                   result=item), attr=item))
            elif goal_entry['goaltype'] == 'boolean':
                print(' is boolean')
                BoolExpTableCls.add_column(item, HackCol(item))
            elif goal_entry['goaltype'] == 'matchany':
                print(' is matchany')
                BoolExpTableCls.add_column(item, HackLinkCol(item, 'goal_select',
                   url_kwargs=dict(student_id='student_id', goal=item, timestamp='timestamp'), attr=item))
            elif goal_entry['goaltype'] == 'time_during':
                print(' is time_during')
                BoolExpTableCls.add_column(item, HackLinkCol(item, 'goal_select',
                   url_kwargs=dict(student_id='student_id', goal=item, timestamp='timestamp'), attr=item))
                
            else:
                ''' not handled yet '''
                print(' goal type %s is not known' % goal_entry['goaltype'])
                BoolExpTableCls.add_column(item, HackCol(item))
        else:
            goal_entry = getGoal(goals_json, item)
            if goal_entry is not None:
                ''' boolean expression value is a goal that has no results '''
                row = {} 
                row['missing_goal'] = item 
                row['timestamp'] = 'None'
                row['student_id'] = student_id
                missing_goal_rows.append(row)
    ''' populate the rows of the tables '''
    missing_goal_table = None
    if len(missing_goal_rows) > 0:
        missing_goal_table = MissingBoolTableCls(missing_goal_rows) 
    bool_exp_tbl_rows = []
    for ts in bool_json:
        row = {}
        row['timestamp'] = ts
        row['student_id'] = student_id
        for item in bool_json[ts]:
            if (' %s ' % item) in the_string:
                row[item] = '%s:%s' % (item, bool_json[ts][item])
                print('added %s' % row[item])
        ''' exclude the row if it lacks any column '''
        skip_row = False
        for c in columns:
            if c not in row:
                skip_row = True
                print('row missing column %s, skip it' % c)
                break
        if not skip_row:
            bool_exp_tbl_rows.append(row)
    bool_exp_tbl = BoolExpTableCls(bool_exp_tbl_rows)
    bool_tbl_list.append([goal_id, bool_string, bool_exp_tbl, missing_goal_table])
    ''' look for bool elements that are themselves results of boolean expressions '''
    for sub_goal_id in bool_json_keys:
        if sub_goal_id in did_these:
            continue
        elif (' %s ' % sub_goal_id) not in the_string:
            continue
        else:
            did_these.append(sub_goal_id)
        goal_entry = getGoal(goals_json, sub_goal_id)
        if goal_entry is not None and goal_entry['goaltype'] == 'boolean':
            bool_tbl_list = getBoolTable(student_id, student_inter_dir, sub_goal_id, goals_json, bool_tbl_list, did_these)

    return bool_tbl_list
    
@app.route('/grades/goals/<student_id>/<goal>/<timestamp>')
def goal_select(student_id, goal, timestamp):
    global raw_fpath
    student_dir = os.path.join(lab_dir, student_id)
    student_inter_dir = os.path.join(student_dir, '.local','result')
    goals_json_file = os.path.join(student_inter_dir, 'goals.json')
    if '-' in timestamp:
        timestamp_start = timestamp.split('-')[0]
    else:
        timestamp_start = timestamp
    goal_id = goal.split(':')[0]
    bool_tbl_list = []
    result_rec = None
    ts_table = None
    student_email = student_id.rsplit('.', 1)[0]
    with open(goals_json_file) as fh:
        goals_json = json.load(fh)
    goal_entry = getGoal(goals_json, goal_id) 
    if goal_entry is None:
        print('no goal entry for %s' % goal_id)
        return ('no goal entry for %s' % goal_id)
    elif goal_entry['goaltype'] == 'time_during':
        goal1 = goal_entry['goal1tag'] 
        goal1_entry = getGoal(goals_json, goal1) 
        if goal1_entry is None:
            container, fname, expr = getResultFileName(student_id, goal1)
            container_id = '%s.%s.student' % (lab, container) 
            print('wt fname is %s' % fname)
            if fname.startswith('/'):
                raw_fpath = fname
                raw_url = url_for('raw_select', student_id=student_id, container_id=container_id, ts='None', fname='raw')
                result1_rec_list = [{'result_id' : goal1, 'expr' : expr, 'container' : container, 
                        'fname' : fname, 'raw_url' : raw_url}]
            else:
                result1_rec_list =  getResultTSRec(student_id, timestamp, goal1, container, fname, expr)
        
        goal2 = goal_entry['goal2tag'] 
        goal2_entry = getGoal(goals_json, goal2) 
        if goal2_entry is None:
            container, fname, expr = getResultFileName(student_id, goal2)
            container_id = '%s.%s.student' % (lab, container) 
            if fname.startswith('/'):
                raw_fpath = fname
                raw_url = url_for('raw_select', student_id=student_id, container_id=container_id, ts='None', fname='raw')
                result2_rec_list = [{'result_id' : goal2, 'expr' : expr, 'container' : container, 
                        'fname' : fname, 'raw_url' : raw_url}]
            else:
                result2_rec_list =  getResultTSRec(student_id, timestamp, goal2, container, fname, expr)


        return render_template('goal_during.html', lab=lab, student_email=student_email, goal = goal, 
               goal1=goal1, goal2=goal2, goal1_entry=goal1_entry, goal2_entry=goal2_entry, 
               result1_rec=result1_rec_list, result2_rec=result2_rec_list,
               timestamp=timestamp, back_grades=url_for('grades'))
    else:
        if goal_entry['goaltype'] == 'boolean':
            did_these = [goal_id]
            bool_tbl_list = getBoolTable(student_id, student_inter_dir, goal_id, goals_json, bool_tbl_list, did_these)
        elif goal_entry['goaltype'] == 'matchany':
            resulttag = goal_entry['resulttag']
            if resulttag.startswith('result.'):
                 result_id = resulttag.split('.')[1]
                 if timestamp is not None and timestamp != 'None':
                     result_rec = getResultTSRec(student_id, timestamp, result_id)
                 else:
                     ts_table, search_string = getTSTable(student_id, result_id)
                     if ts_table is None:
                         result_rec = {}
                         result_rec['fname'], result_rec['expr'] = getResultDef(result_id)
                         
        return render_template('goal.html', lab=lab, student_email=student_email, goal = goal, 
               bool_tbl_list=bool_tbl_list, goal_entry=goal_entry, result_rec=result_rec, 
               ts_table=ts_table, timestamp=timestamp_start, back_grades=url_for('grades'))

def getGoalsList():
    goals_file = os.path.join(lab_dir,'.local', 'instr_config', 'goals.config')
    retval = []
    with open(goals_file) as fh:
        for line in fh:
            if line.strip().startswith('#'):
                continue
            if '=' in line:
                goal, rest = line.split('=', 1)
                retval.append(goal.strip())
    return retval

def getResultDef(result_id):
    fname = None
    expr = None
    result_file = os.path.join(lab_dir,'.local', 'instr_config', 'results.config')
    with open(result_file) as fh:
        for line in fh:
            if line.strip().startswith('#'):
                continue
            if '=' in line:
                result, rest = line.split('=')
                if result.strip() == result_id:
                    fname, expr = rest.split(' : ', 1)
                    break
    return fname, expr

def getResultFileName(student_id, result_id):
    student_dir = os.path.join(lab_dir, student_id)
    target_file, expr = getResultDef(result_id)
    container = None
    if ':' in target_file:
        container, target_file = target_file.split(':')
    if container is None:
        glob_mask = '%s/*/' % student_dir
        dlist = glob.glob(glob_mask)
        if len(dlist) != 1:
            print('result_select expected on directory, got %s' % str(dlist))
            exit(1)
        container_id = os.path.basename(dlist[0][:-1])
        container = container_id.split('.')[1].strip()
    else:
        container = container.strip()
    return container, target_file, expr

def getResultTSRec(student_id, timestamp, result_id, container, fname, expr):
    retval_list = []
    student_dir = os.path.join(lab_dir, student_id)
    student_inter_dir = os.path.join(student_dir, '.local','result')
    goals_json_file = os.path.join(student_inter_dir, 'goals.json')
    container_id = '%s.%s.student' % (lab, container) 

    if '-' in timestamp:
        ts_start, ts_end = timestamp.split('-')
    else:
        ts_start = timestamp
        ts_end = timestamp
    glob_mask = '%s.*' % lab
    glob_path = os.path.join(student_inter_dir, glob_mask)
    glob_results = glob.glob(glob_path)
    for ts_results_file in glob_results:
        print('ts_results_file %s' % ts_results_file)
        file_ts = ts_results_file.rsplit('.', 1)[1]
        if file_ts >= ts_start and file_ts <= ts_end: 
            retval = {}
            with open(ts_results_file) as fh:
                tsr = json.load(fh)
            value = tsr[result_id]
           
            result_ts = '%s.%s' % (fname, file_ts)
            result_path = os.path.join(student_dir, container_id, '.local', 'result', result_ts)
            if not os.path.isfile(result_path):
                print('no raw file for ts %s, skip this result ts' % file_ts)
                continue
            with open(result_path) as fh:
                data = fh.read()
            retval['result_id'] = result_id
            retval['value'] = value
            retval['container'] = container
            retval['fname'] = fname
            retval['file_ts'] = file_ts
            retval['expr'] = expr
            retval['data'] = data
            retval['raw_url'] = url_for('raw_select', student_id=student_id, container_id=container_id, ts=file_ts, fname=fname)
            retval_list.append(retval)
    return retval_list
           
@app.route('/grades/results/ts/<student_id>/<timestamp>/<result>')
def result_select(student_id, timestamp, result):
    result_id = result.split(':')[0]
    container, fname, expr = getResultFileName(student_id, result)
    result_rec = getResultTSRec(student_id, timestamp, result_id, container, fname, expr)[0]
    student_email = student_id.rsplit('.', 1)[0]
    return render_template('result.html', student_id=student_email, result = result_rec['result_id'], 
             value=result_rec['value'], timestamp=timestamp, 
             fname=result_rec['fname'], container=result_rec['container'], expr=result_rec['expr'], 
             data=result_rec['data'], back_grades=url_for('grades'))

@app.route('/grades/goals_config')
def goals_config():
    result_file = os.path.join(lab_dir,'.local', 'instr_config', 'results.config')
    with open(result_file) as fh:
        results_data = fh.read()
    goals_file = os.path.join(lab_dir,'.local', 'instr_config', 'goals.config')
    with open(goals_file) as fh:
        goals_data = fh.read()
    return render_template('goals_config.html', lab=lab, results_data=results_data, goals_data=goals_data, back_grades=url_for('grades'))



@app.route('/form-example', methods=['GET', 'POST']) #allow both GET and POST requests
def form_example():
    if request.method == 'POST':  #this block is only entered when the form is submitted
        language = request.form.get('language')
        framework = request.form['framework']

        return '''<h1>The language value is: {}</h1>
                  <h1>The framework value is: {}</h1>'''.format(language, framework)

    return '''<form method="POST">
                  Language: <input type="text" name="language"><br>
                  Framework: <input type="text" name="framework"><br>
                  <input type="submit" value="Submit"><br>
              </form>'''
if __name__ == '__main__':
    app.run(debug=True, port=8008, host='0.0.0.0')
       

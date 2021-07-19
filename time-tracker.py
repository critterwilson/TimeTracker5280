import argparse
from datetime import datetime
import math
import os
from pathlib import Path
import pandas as pd

RECORD_PATH = Path(Path.home() / 'TimeTracker/timelog.csv')
ACCEPTED_DATES = ['%m-%d-%Y', '%d-%m-%Y', '%Y-%m-%d', '%Y%m%d']
ACCEPTED_TIMES = ['%H:%M', '%H:%M %p', '%H%M%S', '%H%M']
PARSE_DATETIMES = ['%Y-%m-%d %H:%M:%S.%f', '%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M', '%Y%m%d %H%M']

EDIT_PARSE_DATETIMES = [None, '', '%Y-%m-%d %H:%M:%S.%f', '%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M', '%Y%m%d %H%M']


def parse_date(date_str, formats):
	'''Parses a date string by comparing it to supplied list of formats'''
	# Compare the date_str to each format
	for fmt in formats:
		try:
			# return the first match
			return datetime.strptime(date_str, fmt)
		except:
			pass
	# raise error if nothing works
	raise ValueError('No valid date format supplied.')

def open_task(df, name=None, date=None, time=None):
	'''Creates a new task with status \'Open\''''
	# Check to see if non-default date/time is provided
	try:
		if date is not None:
			date = parse_date(date, ACCEPTED_DATES).date()
		else:
			date = datetime.now().date()
		if time is not None:
			time = parse_date(time, ACCEPTED_TIMES).time()
		else:
			time = datetime.now().time().replace(second=0, microsecond=0)
	# alert user if the provided dates don't work
	except Exception as e:
		print('Error getting date information.')
		print(e)

	# enter the task name if not provided
	if name is None:
		name = input("Enter task name: ")

	# add that data to the "db"
	df = df.append({'Start Time':datetime.combine(date, time), 'End Time':None,
		'Open/Closed':'Open', 'Task':name}, ignore_index = True)
	# overwrite the "db"
	df.to_csv(Path.home() / 'TimeTracker/timelog.csv', index=False)
	# Tell the user what happened
	print(f'You are now working on {name}. Thank you!')

def close_task(df, name=None, index=None, date=None, time=None):
	'''Change a task staus from \'Open\' to \'Close\''''
	# try to get the dates in the proper format
	if date is not None:
		date = parse_date(date, ACCEPTED_DATES).date()
	else:
		date = datetime.now().date()

	if time is not None:
		time = parse_date(time, ACCEPTED_TIMES).time()
	else:
		time = datetime.now().time().replace(second=0, microsecond=0)

	if index is not None and index.isdigit():
		index = int(index)

	if name is not None:
		# if the record name exists more than once, delete the first one
		try:
			index = df.index[df['Task'].str.lower() == name.lower()].tolist()[0]
		except Exception as e:
			print('Could not find a record with that name')
			print(e)
	# get input from the user
	elif index is None:
		print("Which task would you like to close?")
		show_all_records()	
		index = int(await_selection([str(x) for x in df.index.values.tolist()]))

	# overwrite the open entry to be close
	df.loc[index, 'Open/Closed'] = 'Closed'
	df.loc[index, 'End Time'] = datetime.combine(date, time)
	try:
		df.loc[index, 'Duration'] = get_time_in_quarter_hours(df.loc[index, 'Start Time'],
			df.loc[index, 'End Time'])
	except Exception as e:
		print('Error deleting record.')
		print(e)
		quit()

	# write the "db" again
	df.to_csv(Path.home() / 'TimeTracker/timelog.csv', index=False)

	# Tell the user what happened
	print(f'{df.loc[index, "Task"]} has been closed. You worked on that task for ' +
		f'{df.loc[index, "Duration"]} hours. Thank you!')

def edit_task(df, name=None, index=None):
	# name takes precedence over index
	if name is not None:
		# if the record name exists more than once, delete the first one
		try:
			index = df.index[df['Task'].str.lower() == name.lower()].tolist()[0]
		except Exception as e:
			print('Could not find a record with that name')
			print(e)
	# if name and index are not specified, prompt user for tax
	elif index is None or not index.isdigit():
		print("Which task would you like to edit?")
		show_all_records()
		index = int(await_selection([str(x) for x in df.index.values.tolist()]))
	index = int(index)

	name = input(f'Name ({df.loc[index, "Task"]}): ')
	print(f'name: {name}')
	if name in ['', None]:
		pass
	else:	
		df.loc[index, "Task"] = name

	print(f'index: {index}')
	start = parse_date(input(f'Start Time: ({df.loc[index, "Start Time"]}): '), EDIT_PARSE_DATETIMES)
	if start in ['', None, '1900-01-01 00:00:00']:
		pass
	else:	
		df.loc[index, "Start Time"] = start

	end = input(f'End Time: ({df.loc[index, "End Time"]}): ')
	if end in ['', None, '1900-01-01 00:00:00']:
		pass
	else:	
		end = parse_date(end, EDIT_PARSE_DATETIMES)
		df.loc[index, "End Time"] = end

	open_close = await_selection(['', None, 'Open', 'Closed'], f'Open/Closed ({df.loc[index, "Open/Closed"]}): ')
	if open_close in ['', None]:
		pass
	else:	
		df.loc[index, "Open/Closed"] = open_close

	df.loc[index, "Duration"] = get_time_in_quarter_hours(df.loc[index, "Start Time"], df.loc[index, "End Time"])
	# overwrite the "db"
	df.to_csv(Path.home() / 'TimeTracker/timelog.csv', index=False)
	# Tell the user what happened
	print(f'{df.loc[index, "Task"]} sucessfully edited')

def delete_record(df, name=None, index=None):
	'''Removes one record'''
	# name takes precedence over index
	if name is not None:
		# if the record name exists more than once, delete the first one
		try:
			index = df.index[df['Task'].str.lower() == name.lower()].tolist()[0]
		except Exception as e:
			print('Could not find a record with that name')
			print(e)
	# if name and index are not specified, prompt user for tax
	elif index is None or not index.isdigit():
		print("Which task would you like to close?")
		show_all_records()
		index = int(await_selection([str(x) for x in df.index.values.tolist()]))

	# Remove the record from the df and write to the "DB"
	try:
		df.drop(int(index), inplace=True)
		df.to_csv(Path.home() / 'TimeTracker/timelog.csv', index=False)
	except Exception as e:
		print('Error deleting the record')
		print(e)
		return
	print('Successfully deleted the record')

def await_selection(acceptable, prompt='Selection: '):
	'''Prompt user for a selection until the selection is in the acceptable list'''
	# repeat until we get it right
	while True:
		# see if the input is in our acceptable values list
		try:
			selection = input(prompt)
			if not selection in acceptable:
				raise ValueError
		# if it's not, try again
		except ValueError:
			print("Invalid selection. Try again.")
			continue
		# if it is, break out with the value
		else:
			return selection

def get_time_in_quarter_hours(start, end):
	'''Round a delta time to the nearest quarter hour (rounds up)'''
	# if start and end are not datetimes, convert them
	if isinstance(start, str):
		start = parse_date(start, PARSE_DATETIMES)
	if isinstance(end, str):
		end = parse_date(end, PARSE_DATETIMES)

	# our total duration in hours
	delta = (end - start)
	delta = delta.total_seconds() / 3600

	# return rounded to the nearest .25
	return math.ceil(delta*4) / 4

def clear_all_records():
	'''Removes the document containing all records'''
	# make sure the user actually wants to do this
	print('Are you sure you would like to delete all records? Y/n')
	selection = await_selection(['y', 'n', 'yes', 'no', 'Y', 'N', 'Yes', 'No'], 'Y/N: ')
	if selection.lower() in ['y', 'yes']:
		# delete the "DB"
		if RECORD_PATH.exists():
			try:
				os.remove(RECORD_PATH)
			except Exception as e:
				print('Error removing records. Terminating process.')
				print(e)
			else:
				print('Successfully removed records. Thank you!')
	else:
		return

def show_all_records():
	'''List all records, open or closed'''
	if RECORD_PATH.exists():
		df = pd.read_csv(RECORD_PATH)
		print(df.to_string(index = True))
	else:
		print('There is no record at required location.')

def handle_arguments():
	'''Process the arguments from the user'''
	parser = argparse.ArgumentParser()
	# start stop clear show delete arguments
	parser.add_argument('action', help='[Start]/[stop] a task\n' +
		'[clear] all previous records\n' +
		'[show] all records\n' +
		'[delete] a single record\n',
		choices=('start', 'open', 'stop', 'close', 'clear', 'show', 'delete', 'edit', 'sum'))
	# specify a date
	parser.add_argument('--date', '-d', action='store',
		help='Specify a time in the format mm-dd-yyyy')
	# specify a time
	parser.add_argument('--time', '-t', action='store',
		help='Specify a time for a task')
	# specify a task name
	parser.add_argument('--name', '-n', action='store',
		help='Specify the name of a task that you are starting')
	# specify a task index
	parser.add_argument('--index', '-i', action='store',
		help='Specify the index of a task that you are starting/stoping')
	args = parser.parse_args()

	# return the args as a dictionary
	return {'action':args.action, 'date':args.date, 'time':args.time, 'name':args.name, 'index':args.index}

def main():
	'''Main driver'''
	# initialize a blank dataframe
	df = pd.DataFrame(columns = ['Start Time', 'End Time', 'Open/Closed', 'Task', 'Duration'])

	# handle arguments
	try:
		args = handle_arguments()
	except:
		print('Incorrect arguments. Terminating process.')
		return

	## Check if we have a timelog file already
	if RECORD_PATH.exists():
		# if we do, read into pandas
		df = pd.read_csv(RECORD_PATH)

	# react to given arguments
	# start a new task
	if args['action'] in ['start', 'open']:
		open_task(df, args['name'], args['date'], args['time'])
	# stop a task
	elif args['action'] in ['stop', 'close', 'end']:
		close_task(df, args['name'], args['index'], args['date'], args['time'])
	# edit a task
	elif args['action'] in ['edit', 'adjust', 'change']:
		edit_task(df, args['name'], args['index'])
	# clear all records
	elif args['action'] == 'clear':
		clear_all_records()
	# show all records
	elif args['action'] == 'show':
		show_all_records()
	# delete one record
	elif args['action'] == 'delete':
		delete_record(df, args['name'], args['index'])
	elif args['action'] == 'sum':
		print(f'You\'ve worked a total of {df.Duration.sum()} hours today.')

# initiate driver
if __name__ == "__main__":
	main()

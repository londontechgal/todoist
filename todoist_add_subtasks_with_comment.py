import todoist
import csv, requests, uuid, json

your_token = '<your token here>'
api = todoist.TodoistAPI(your_token)

def get_task_id_by_content(content):
    api.sync()
    items = api.items.all()
    for item in items:
        if item['content'].startswith(content):
            return item['id']
        
# get parent task for subtask to be created under
parent_id = get_task_id_by_content("100 Days Of Code")

# csv in format 'subtask content','comment'  
csv_file = "path_to_file\subtask_comment.csv"

with open(csv_file) as f:
    csv_reader = csv.reader(f)
    for row in csv_reader:
        subtask_content = row[0]
        comment = row[1]
        # create subtask
        response = requests.post(
            "https://api.todoist.com/rest/v1/tasks",
            data=json.dumps({ 
                "content": subtask_content,
                "parent_id": parent_id
            }),
            headers={
                "Content-Type": "application/json",
                "X-Request-Id": str(uuid.uuid4()),
                "Authorization": "Bearer %s" % your_token
            }).json()
        task_id = response['id']
        # add comment to that subtask 
        requests.post(
            "https://api.todoist.com/rest/v1/comments",
            data=json.dumps({
                "task_id": task_id,
                "content": comment
            }),
            headers={
                "Content-Type": "application/json",
                "X-Request-Id": str(uuid.uuid4()),
                "Authorization": "Bearer %s" % your_token
            }).json()
        


![[tasks.jpg|banner]]

### Calendario Mensual de actividades


```dataview 
TABLE contenido, date
FROM "Calendario y tareas/Citas"
WHERE date >= date(today) 
SORT date ASC
LIMIT 5
```


```base
filters:
  or:
    - type == "sermon"
    - type == "enseñanza"
    - type == "seguimiento"
    - type == "discipulado"
views:
  - type: task-genius-inbox
    name: Table
    startDate: note.date
    rowHeight: medium
    viewMode: inbox
    taskContent: file.basename
    taskStatus: note.status
    taskPriority: note.priority
    taskProject: note.project
    taskTags: note.tags
    taskDueDate: note.dueDate
    taskStartDate: note.startDate
    taskCompletedDate: note.completionDate
    taskContext: note.context

```




---
publish: true
---
![[greektext.jpg|banner]]

```base
filters:
  and:
    - type == "sermon"
views:
  - type: table
    name: Table
    order:
      - file.name
      - date
      - related
    sort:
      - property: date
        direction: ASC

```

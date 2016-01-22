#EbbinghausGenerator
You can add learning records or generate learning plan from command line.
##Add learning records
```
python generator.py a
Date: 2016-01-01
Lessons: 123
```

OR you can:

```
python generator.py a
Date: today
Lessons: 123,124
```
##Generate learning plan
```
python generator.py g
Start date: 2016-01-05
End date: 2016-02-04
```

OR you can:

```
python generator.py g
Start date: today - 5
End date: today + 30
```

# Backend developer position challenge

## Setup

The first thing to do is to clone the repository:

```sh
$ git clone `https://github.com/donovan-vargas/dacodesCourses.git`
$ cd dacodes
```

Create a virtual environment to install dependencies in and activate it:

```sh
$ make
```
Once `pip` has finished downloading the dependencies:
```sh
bash server-wrapper.sh
```
And navigate to `http://127.0.0.1:8000/api/v1/`.

## Endpoints 
`http://127.0.0.1:8000/api/v1/courses/` Get a list of all courses, 
telling which ones the student can access

`http://127.0.0.1:8000/api/v1/lessons/` Get lessons for a course, 
telling which ones the student can access

`http://127.0.0.1:8000/api/v1/lessons/?course_id=1` Get lesson details by course id

`http://127.0.0.1:8000/api/v1/answers/?lesson_id=1` Get lesson details for answering its questions
Take a lesson (to avoid several requests, they asked to send all answers in one go)

Basic CRUD for courses, lessons and questions

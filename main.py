#!/usr/bin/env python
import secrets 

from school_web_forms import TeacherForm
from db_manipulate import db_connector

from db_manipulate.change_info import db_change_add_teacher

from db_manipulate.get_info import db_get_subject, \
        db_get_teacher, \
        db_get_cabinet_class, \
        db_get_teacher_classes, \
        db_get_timetable_class

from flask import Flask, render_template, request, session, redirect, flash
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
bootstrap = Bootstrap(app)

get_session_variable = lambda session_variable: \
        session[session_variable] if session_variable in session.keys() else None

@app.route("/change_info.html", methods=['GET', 'POST'])
def change_info():
    form_teacher = TeacherForm()

    if request.method == 'POST':
        #print(request.values)

        if form_teacher.validate_on_submit():
            res = db_change_add_teacher.add_teacher(form_teacher, DBWriter)

            form_teacher.first_name.data = ''
            form_teacher.second_name.data = ''
            form_teacher.third_name.data = ''
            form_teacher.lesson = ''
            form_teacher.cabinet_num = ''
            form_teacher.class_num = ''
            form_teacher.subclass = ''

        return redirect(request.url)

    return render_template('change_info.html', \
            form_teacher=form_teacher
    )

@app.route("/", methods=['GET', 'POST'])
def get_info():
    if request.method == 'POST':
        values_dict = request.values.to_dict()
        taked_subject = db_get_subject.handle_subject(values_dict, session, DBReader)
        taked_teacher = db_get_teacher.handle_teacher(values_dict, session, DBReader)
        taked_cabinet_class = db_get_cabinet_class.handle_cabinet_class(values_dict, session, DBReader)
        taked_teacher_classes = db_get_teacher_classes.handle_teacher_classes(values_dict, session, DBReader)
        taked_timetable_class = db_get_timetable_class.handle_timetable_class(values_dict, session, DBReader)
        
        if taked_subject:
            session['taked_subject'] = taked_subject

        if taked_teacher:
            session['taked_teacher'] = taked_teacher

        if taked_cabinet_class:
            session['taked_cabinet_class'] = taked_cabinet_class

        if taked_teacher_classes:
            session['taked_teacher_classes'] = taked_teacher_classes
        
        if taked_timetable_class:
            session['taked_timetable_class'] = taked_timetable_class

        return redirect('/')

    #print(session)
    return render_template('get_info.html', \
        subject_day_week=get_session_variable("subject_day_week"), \
        subject_lesson_num=get_session_variable("subject_lesson_num"), \
        subject_classes=get_session_variable("subject_classes"), \
        subject_class=get_session_variable("subject_class"), \
        subject_subclasses=get_session_variable("subject_subclasses"), \
        subject_subclass=get_session_variable("subject_subclass"), \
        taked_subject=get_session_variable("taked_subject"), \

        teacher_lessons=teacher_lessons, \
        teacher_lesson=get_session_variable("teacher_lesson"), \
        teacher_classes=get_session_variable("teacher_classes"), \
        teacher_class=get_session_variable("teacher_class"), \
        teacher_subclasses=get_session_variable("teacher_subclasses"), \
        teacher_subclass=get_session_variable("teacher_subclass"), \
        taked_teacher=get_session_variable("taked_teacher"), \

        cabinet_class_day_week=get_session_variable("cabinet_class_day_week"), \
        cabinet_class_lesson_num=get_session_variable("cabinet_class_lesson_num"), \
        cabinet_class_class=get_session_variable("cabinet_class_class"), \
        cabinet_class_classes=get_session_variable("cabinet_class_classes"), \
        cabinet_class_subclasses=get_session_variable("cabinet_class_subclasses"), \
        cabinet_class_subclass=get_session_variable("cabinet_class_subclass"), \
        taked_cabinet_class=get_session_variable("taked_cabinet_class"), \

        teacher_classes_first_names=db_get_teacher_classes.get_teachers_first_names(DBReader), \
        teacher_classes_first_name=get_session_variable("teacher_classes_first_name"), \
        teacher_classes_second_names=get_session_variable("teacher_classes_second_names"), \
        teacher_classes_second_name=get_session_variable("teacher_classes_second_name"), \
        teacher_classes_third_names=get_session_variable("teacher_classes_third_names"), \
        teacher_classes_third_name=get_session_variable("teacher_classes_third_name"), \
        teacher_classes_subjects=get_session_variable("teacher_classes_subjects"), \
        teacher_classes_subject=get_session_variable("teacher_classes_subject"), \
        taked_teacher_classes=get_session_variable("taked_teacher_classes"), \

        timetable_class_day_week=get_session_variable("timetable_class_day_week"), \
        timetable_class_classes=get_session_variable("timetable_class_classes"), \
        timetable_class_class=get_session_variable("timetable_class_class"), \
        timetable_class_subclasses=get_session_variable("timetable_class_subclasses"), \
        timetable_class_subclass=get_session_variable("timetable_class_subclass"), \
        taked_timetable_class=get_session_variable("taked_timetable_class")
    )

if __name__ == "__main__":
    DBReader = db_connector.DBFetcher(host="localhost", database="school", user="root", password="1234")
    DBWriter = db_connector.DBEditor(host="localhost", database="school", user="root", password="1234")
    teacher_lessons, teacher_subclasses = db_get_teacher.get_teacher_info(DBReader)
    app.run(host='0.0.0.0', debug=True)

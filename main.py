from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,  NavigationToolbar2Tk)
from matplotlib import pyplot as plt
from matplotlib.ticker import FuncFormatter, MaxNLocator

from numpy import *
from datetime import *
import pandas as pd
import shutil
import subprocess
from functools import partial  # Helps pass extra arguments to functions
import os


from tkinter import *
from tkinter import ttk, messagebox

from pandas import read_csv

import course_calendar
from create_total_file import create_total_file_function

from settings import *


# Global variable to store the canvas
canvas = None
toolbar = None
button_list = []



def which_week():
    # return the actual week based on the settings.py.

    today = datetime.today().strftime('%d/%m')
    for week_number in weeks.keys():
        if today in weeks[week_number]:
            print("We are in the week number: ", week_number)

            return week_number


def int_week(week):
    # Return the number of the week. If S in the week number we return the number,
    # else if blocus or exam week, we return the index of the week in the calendar.

    if week[0] == "S":
        int_week_number = int(week.split("S")[1])
        return int_week_number

    int_week_number = int(list(weeks.keys()).index(week))
    return int_week_number




def graph_work_quantity(course, actual_week_number, TPorCM, window):
    # THis function is used to make a graph of all the work (TP or CM) done
    # for one course.
    global canvas
    global toolbar

    if canvas:
        canvas.get_tk_widget().destroy()
        canvas = None
    if toolbar:
        toolbar.destroy()
        toolbar = None

    theoricalTP = []
    theoricalCM = []
    DoneTP = []
    DoneCM = []
    passed_week = []
    numberofTPTheorical = 0
    numberofCMTheorical = 0

    int_actual_week_number = int_week(actual_week_number)
    courseNEW = "".join(course.split(" "))
    file = initial_path + "/hours_done_" + actual_period + "/Done" + courseNEW + ".csv"
    df = pd.read_csv(file)


    for week_number in weeks.keys():
        week_number_temporary = int_week(week_number)
        if TPorCM == "TP" and week_number_temporary <= int_actual_week_number: # making all the sublists that allows to make the bar plot of the TP done during the past weeks
            DoneTP.append(sum(df["TP"][:week_number_temporary]))
            if TPorCM in getattr(course_calendar, courseNEW)[week_number]:
                numberofTPTheorical += getattr(course_calendar, courseNEW)[week_number].count("TP")
                theoricalTP.append(numberofTPTheorical)
                passed_week.append(week_number)
            else:
                theoricalTP.append(0)
                passed_week.append(week_number)
        if TPorCM == "CM/Théorie" and week_number_temporary <= int_actual_week_number :
            DoneCM.append(sum(df["CM"][:week_number_temporary]))
            if "CM" in getattr(course_calendar, courseNEW)[week_number]:
                numberofCMTheorical += getattr(course_calendar, courseNEW)[week_number].count("CM")
                theoricalCM.append(numberofCMTheorical)
                passed_week.append(week_number)
            else:
                theoricalCM.append(0)
                passed_week.append(week_number)

        elif week_number_temporary > int_actual_week_number:
            break

    bar_done = []
    bar_to_do = []
    x = arange(len(passed_week))  # the label locations
    width = 0.35  # the width of the bars


    if TPorCM == "CM/Théorie":
        bar_done = [x - width / 2, DoneCM, width, 'CM or Theory done']
        bar_to_do = [x + width / 2, theoricalCM, width, 'CM to do']
        title = 'Progress of CM in ' + course

    elif TPorCM == "TP":
        bar_done = [x - width / 2, DoneTP, width, 'TP done']
        bar_to_do = [x + width / 2, theoricalTP, width, 'TP to do']
        title = 'Progress of TP in ' + course


    fig, ax = plt.subplots()
    fig.subplots_adjust(hspace=0.6)
    ax.bar(bar_done[0], bar_done[1], bar_done[2], label=bar_done[3])
    ax.bar(bar_to_do[0], bar_to_do[1], bar_to_do[2], label=bar_to_do[3])

    ax.set_ylabel('#')
    ax.set_title(title)
    ax.set_xticks(x)
    ax.set_xticklabels(passed_week)
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))

    ax.legend()

    fig.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()

    # Create the toolbar
    toolbar = NavigationToolbar2Tk(canvas, window, pack_toolbar=False)
    toolbar.update()
    # Use grid to place the toolbar and canvas
    toolbar.grid(row=25, column=2, pady=10)
    canvas.get_tk_widget().grid(row=5, rowspan=20, column=2, padx=10, pady=10)


def time_from_beginning(window):
    # Gives the time since the beginning of the session

    now = datetime.now()
    with open(session_running_path, "r") as file:
        lines = []
        for line in file:
            lines.append(line)
    if "session_running = False\n" not in lines:
        start_time = datetime.strptime(lines[0].strip(), '%d/%m/%y %H:%M:%S')
        course = lines[1].strip()
        difference = now - start_time
        diffTime = Label(window, text="You've started a " + course + " session " + str(difference) + " ago", fg="red")
        diffTime.grid(row=6, column=0, columnspan=5)
        diffTime.after(2000, diffTime.destroy)
    else:
        diffTime = Label(window, text="You didn't start any course", fg="red")
        diffTime.grid(row=6, column=0, columnspan=4)
        diffTime.after(2000, diffTime.destroy)


def time_to_hms(seconds):
    #Convert seconds to HH:MM:SS format 
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"

def graph_Practical(course, window):
    global canvas
    global toolbar
    # If a previous canvas exists, destroy it before creating a new one
    if canvas:
        canvas.get_tk_widget().destroy()
        canvas = None
    if toolbar:
        #toolbar.destroy()
        toolbar = None


    file = initial_path + "/hours_done_" + actual_period + "/" + "".join(course.split(" ")) + ".csv"
    df = pd.read_csv(file)
    print(df)
    fig = Figure(figsize=(6, 6), dpi=100)
    fig.subplots_adjust(hspace=0.6)

    if "Delta" in df.columns:
        df["Delta"] = pd.to_timedelta(df["Delta"])
        df["Delta_seconds"] = df["Delta"].dt.total_seconds()
        df["Cumulative_Time"] = df["Delta"].cumsum()        # Convert timedelta to datetime, using midnight (00:00:00) as reference
        df["Cumulative_Time_seconds"] = df["Cumulative_Time"].dt.total_seconds()

    plot1 = fig.add_subplot(211)
    plot1.plot(df["Cumulative_Time_seconds"], label="Cumulative Time (seconds)")
    plot1.xaxis.set_major_locator(MaxNLocator(integer=True))
    plot1.yaxis.set_major_formatter(FuncFormatter(lambda x, _: time_to_hms(x)))
    plot1.set_title("Total study time for " + course)
    plot1.set_xlabel("Session #")
    plot1.set_ylabel("Time (HH:MM:SS)")

    plot2 = fig.add_subplot(212)
    plot2.plot(df["Delta_seconds"], label="Delta Time" )
    plot2.xaxis.set_major_locator(MaxNLocator(integer=True))
    plot2.yaxis.set_major_formatter(FuncFormatter(lambda x, _: time_to_hms(x)))
    plot2.set_title("Session study time for " + course)
    plot2.set_xlabel("Session #")
    plot2.set_ylabel("Time (HH:MM:SS)")



    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    # Create the toolbar
    toolbar = NavigationToolbar2Tk(canvas, window, pack_toolbar=False)
    toolbar.update()

    # Ensure the toolbar does not use `pack` (this is the issue)
    toolbar.pack_forget()  # Remove the default pack behavior

    # Use grid to place the toolbar and canvas
    toolbar.grid(row=24, column=0, pady=10)
    canvas.get_tk_widget().grid(row=4, rowspan=20, column=0, padx=10, pady=10)



def total_study_time(window):
    global canvas
    global toolbar
    # If a previous canvas exists, destroy it before creating a new one
    if canvas:
        canvas.get_tk_widget().destroy()
        canvas = None
    if toolbar:
        toolbar.destroy()
        toolbar = None

    fig, ax = plt.subplots()
    func = create_total_file_function()

    # Load the dataset
    file = hours_done_path + "/" + "TOTALSTUDY.csv"
    df = pd.read_csv(file)

    df['Delta'] = pd.to_timedelta(df['Delta']).dt.total_seconds() / 3600  # Convert to hours

    df['Line_Number'] = range(1, len(df) + 1)
    df = df.sort_values(by='Line_Number')

    for course, group in df.groupby('Course'):
        ax.plot(group['Line_Number'], group['Delta'].cumsum(), label=course, marker='o')

    df['Overall_Cumsum'] = df['Delta'].cumsum()
    ax.plot(df['Line_Number'], df['Overall_Cumsum'], label="Overall", linestyle='dashed', color='black', linewidth=2)

    # Customize plot
    ax.set_xlabel('Line Number')
    ax.set_ylabel('Cumulative Study Hours')
    ax.set_title('Cumulative Study Hours by Course')
    ax.legend()
    ax.grid(True)

    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    # Create the toolbar
    toolbar = NavigationToolbar2Tk(canvas, window, pack_toolbar=False)
    toolbar.update()

    # Ensure the toolbar does not use `pack` (this is the issue)
    toolbar.pack_forget()  # Remove the default pack behavior

    # Use grid to place the toolbar and canvas
    toolbar.grid(row=24, column=4, pady=10)
    canvas.get_tk_widget().grid(row=4, rowspan=20, column=4, padx=10, pady=10)


def start_session(combo_box_start, window):
    print("Start session")
    now = datetime.now().strftime('%d/%m/%y %H:%M:%S')
    selected_value = combo_box_start.get()  # Get the selected value
    print(f"Selected: {selected_value}")


    with open(session_running_path, "r+") as file:
        content = file.read()  # Read the entire file
        print(content)  # Debugging step to check file contents

        if "session_running = True" in content and "session_running = False" not in content:  # Check if the string exists
            print("Session is running!")
            messagebox.showerror("Attention", "You have already started a session running.")

        else:
            file.seek(0)  # Move to the beginning
            file.truncate()  # Remove all content
            file.write(now + "\n")
            file.write(combo_box_start.get() + "\n")
            file.write("session_running = True\n")
            print("You just started a " + combo_box_start.get() + " session at " + now)

            startText = Label(window, text= "You just started a " + combo_box_start.get() + " session at " + now, fg="green")
            startText.grid(row=6, column=0, columnspan=5)
            startText.after(3000, startText.destroy)

    return combo_box_start.get(), now, True


def end_session(combo_box_end):
    now = datetime.now()
    with open(session_running_path, "r+") as file:
        lines = []
        for line in file:
            lines.append(line)

        start_time = datetime.strptime(lines[0].strip(), '%d/%m/%y %H:%M:%S')
        file.write(now.strftime('%d/%m/%y %H:%M:%S') + "\n")
        file.write(combo_box_end + "\n")
        file.write("session_running = False\n")
        delta_time = now - start_time

    df = pd.DataFrame({'Start': [start_time.strftime('%d/%m/%y %H:%M:%S')],
                       'End': [now.strftime('%d/%m/%y %H:%M:%S')],
                       'Delta': [delta_time],})
    file_to_add = hours_done_path +'/' + "".join(combo_box_end.split(" ")) + ".csv"
    df.to_csv(file_to_add, mode='a', index=True, header=False)
    messagebox.showinfo("Great job", "You have been working on : \n" + lines[1] + " for \n" + str(delta_time))
    print("Course's duration is: ", delta_time)

    if not checkIfInFile(file_to_add, now.strftime('%d/%m/%y %H:%M:%S')):
        messagebox.showerror("Error", "Error while adding the session.")

    return combo_box_end, now, False

def checkIfInFile(file, end):
    df = read_csv(file)
    if end not in df["End"].values:
        print("The end time has not been correctly added to the file.")
        return False
    else:
        print("The end time has been correctly added to the file.")
        return True


def check(moment, value, window):
    print("Check runnning")
    with open(session_running_path, "r+") as file:
        lines = []
        for line in file:
            lines.append(line)
    if moment == "End":
        if len(lines) < 3 or "session_running = False\n" in lines:
            messagebox.showwarning("ATTENTION", "You didn't start any session.")
            return False
        if lines[1].strip() != value:
            print('You cannot close a session in a different course than: '+ lines[1])
            messagebox.showwarning("ATTENTION", 'You cannot close a session in a different course than: '+ lines[1])
            return False
    return True

def endSessionChecked(combo_box_end, window):
    selected_value = combo_box_end.get()
    print("Selected:", selected_value)

    if check("End", selected_value, window):  # Call check() and verify result
        end_session(selected_value)  # Call end_session() if valid


def reset_selections(TPorDone, type_var, course_var, label_result):
    #Reset the selections and update the label#
    if TPorDone == "Done":
        type_var.set(None)  # Reset the type variable
        course_var.set("None")  # Reset the course variable
        # Reset the label result to its initial message
        label_result.config(text="Please select both a Type and a Course.")

    if TPorDone == "TPCM":
        type_var.set(None)  # Reset the type variable
        course_var.set("None")  # Reset the course variable
        # Reset the label result to its initial message
        label_result.config(text="Please select a TP or a CM.")



def check_selection(type_var, course_var, label_result):
    currentweek = which_week()
    selected_type = type_var.get()
    selected_course = course_var.get()

    # Check if both selections are made
    if selected_course == "None" or selected_type == 0:  # Default checks
        label_result.config(text="Please select both a Type and a Course.", fg="red")
        return


    label_result.config(text=f"Selected: {selected_course} - {selected_type}", fg="green")
    label_result.after(1000, lambda: reset_selections("Done",type_var, course_var, label_result))

    doneCourse = "Done" + selected_course
    print(f"Updating: {doneCourse}, type: {selected_type}, week: {currentweek}")

    file = hours_done_path + "".join(doneCourse.split(" ")) + ".csv"
    df = pd.read_csv(file, index_col=0)
    df.at[currentweek, selected_type] += 1
    print(df)
    df.to_csv(file, mode='w', index=True, header=True)

def goodJobWindow(master):
    goodJobWindow = Toplevel(master)
    goodJobWindow.title("Good Job Window")
    Label(goodJobWindow, text="Welcome to the window where you can put your work done").grid(row=0, column=0, columnspan=4)
    Label(goodJobWindow, text="What did you just complete? ").grid(row=1, column=0, columnspan=4)

    type_var = StringVar()
    course_var = StringVar()
    type_var.set("None")
    course_var.set("None")  # Default value

    Label(goodJobWindow, text="Select Type:").grid(row=2, column=0, columnspan=2, sticky="w", padx=10, pady=5)

    Radiobutton(goodJobWindow, text='CM/Théorie', variable=type_var, value="CM").grid(row=3, column=1, sticky="w", padx=5, pady=2)
    Radiobutton(goodJobWindow, text='TP', variable=type_var, value="TP").grid(row=4, column=1, sticky="w", padx=5, pady=2)

    Label(goodJobWindow, text="Select Course:").grid(row=2, column=2, columnspan=2, sticky="w", padx=20, pady=5)

    label_result = Label(goodJobWindow, text="Please select both a Type and a Course.")
    label_result.grid(row=9, column=0, columnspan=4, pady=10)

    column = 3
    row = 3
    for courses in getattr(course_calendar, "Course_list_" + actual_period):
        Radiobutton(goodJobWindow, text=courses, variable=course_var, value=courses).grid(row=row, column=column, sticky="w", padx=5, pady=2)
        row += 1

    confirmButton = Button(goodJobWindow, text="Confirm", command=lambda: check_selection(type_var, course_var, label_result))
    confirmButton.grid(row= row, column=0, columnspan=4, padx=5, pady=2)

    # Update course and type when either is selected
    for widget in goodJobWindow.winfo_children():
        print("Widgets = ", goodJobWindow.winfo_children())
        if isinstance(widget, Button):
            print("isinstance", isinstance(widget, Radiobutton))
            widget.config(command=partial(check_selection, type_var, course_var, label_result))

    goodJobWindow.mainloop()

def confirm():
    confirmed = messagebox.askquestion("Reset the data", "Are you sure to reset the data? \nThis action cannot be undone.", icon='warning')
    if confirmed == "yes":
        shutil.rmtree(hours_done_path)
    else:
        messagebox.showinfo('Return', 'Returning to main application')


def update_graph1(event, window, course_combobox):
    selected_course = course_combobox.get()
    print(f"Selected course: {selected_course}")  # Debugging output
    graph_Practical(selected_course, window)

def update_graph2(event, window, TPorCM, workDonecombobox):
    workDonecourse = workDonecombobox.get()
    print(f"Selected course: {workDonecourse}")  # Debugging output
    graph_work_quantity(workDonecourse, which_week(), TPorCM, window)

def choosedTPorCM(window, TPorCM):
    workDonecombobox = ttk.Combobox(window, values=getattr(course_calendar, "Course_list_" + actual_period))
    workDonecombobox.grid(row=4, column=2, sticky="w")
    workDonecombobox.bind("<<ComboboxSelected>>", lambda event: update_graph2(event, window, TPorCM, workDonecombobox))


def getText(inputText): #### Need to maybe edit this function
    course_name = inputText.get()
    print(f'{course_name=!r}')
    course_name_file = course_name + ".csv"
    if course_name_file in os.listdir(hours_done_path):
        messagebox.showwarning("ATTENTION", "Course " + str(course_name) + " already exists.\n Please choose a different course.")
    else:
        mydataset = {'Start': [],
                     'End': [],
                     'Delta': []}
        myvar = pd.DataFrame(mydataset)
        path = "/Users/thibaultvanni/PycharmProjects/Study/hours_done/" + str(course_name) + ".csv"
        myvar.to_csv(path, mode='w', index=True, header=True) ###

def on_button_click(course, name):
    print(f"Button {name} in {course}")
    print(f"Setting the {name} done")

    file = pd.read_csv(initial_path + "/TPCMNUMBERS.csv")

    file.loc[(file["Course"] == course) & (file["Session"] == name), "Done"] = "YES"
    file.to_csv(initial_path + "/TPCMNUMBERS.csv", mode='w', index=False, header=True)



def clear_buttons():
    #Remove all existing buttons from the window.
    for btn in button_list:
        btn.destroy()
    button_list.clear()


def TPCMconfirmation(session_var, course_var, label_result):

    selected_work = session_var.get()
    selected_course = course_var.get()
    print(f"Selected course: {selected_course}")



def showTPandCM(event, window, course):
    clear_buttons()
    #session_var = StringVar()#
    #course_var = StringVar()
    #session_var.set("None")
    #course_var.set("None")  # Default value

    file = pd.read_csv(initial_path + "/TPCMNUMBERS.csv")
    course = "".join(course.split(" "))


    cm_count = 0
    tp_count = 0
    row_index = 0
    col_index = 0
    for index, (row_key, row) in enumerate(file[(file["Course"] == course)].iterrows()):
        print(f"Row Key: {index}")  # row[0] contains the value
        if "CM" in row["Type"] and row["Done"] == "NO":
            col_index = 1
            row_index = cm_count  # CM has its own row index
            cm_count += 1
        elif "TP" in row["Type"] and row["Done"] == "NO":
            row_index = tp_count  # TP has its own row index
            tp_count += 1

        if row_index > 0:
            btn = Button(window, text=row['Session'], command=lambda name=row['Session']: on_button_click(course, name), width=10, height=2)
            btn.grid(row=2+row_index, column=col_index, padx=0, pady=0)  # Use grid layout
            button_list.append(btn)
    if tp_count == 0 and cm_count == 0:
        Label(window, text="You're up to date.", fg="green").grid(row=row_index+2, column=0, columnspan = 4, padx=0, pady=0)

    biggest_index = tp_count if tp_count > cm_count else cm_count
    label_result = Label(window, text="Please select a Type and a Course.")
    label_result.grid(row=2+biggest_index+1, column=0, columnspan=4, pady=10)
    #button = Button(window, text="Confirm", command=TPCMconfirmation(session_var, course_var, label_result))
    #button.grid(row=2+row_index+2, column=0, columnspan=4, padx=5, pady=2)
    #button_list.append(button)

def TODOWindow(master):
    TODOWindow = Toplevel(master)
    TODOWindow.title("TODO in the courses")

    labels = Label(TODOWindow, text="Select the course you just finished a TP or a CM").grid(column=0, row=0, columnspan=2)

    courseValidation = ttk.Combobox(TODOWindow, values=getattr(course_calendar, "Course_list_" + actual_period))
    courseValidation.grid(column=0, row=1, columnspan=2)
    courseValidation.bind("<<ComboboxSelected>>",lambda event: showTPandCM(event, TODOWindow, courseValidation.get()))

    TODOWindow.mainloop()


def graph_window(master):
    global canvas
    graphWindow = Toplevel(master)
    graphWindow.title("Graph Window")
    Label(graphWindow, text="Welcome to the graph window").grid(row=1, column=0, columnspan=4)

    back_button = Button(graphWindow, text="Go back", command=graphWindow.destroy)
    back_button.grid(row=0, column=0, columnspan=4, sticky="w")

    Label(graphWindow, text="Do you want to see the work hours? ").grid(row=2, column=0, columnspan=2, sticky="w")
    course_combobox = ttk.Combobox(graphWindow, values=getattr(course_calendar, "Course_list_" + actual_period))
    course_combobox.grid(row=3, column=0, sticky="w")
    course_combobox.bind("<<ComboboxSelected>>", lambda event: update_graph1(event, graphWindow, course_combobox))

    Label(graphWindow, text="Do you want to see the work done? ").grid(row=2, column=2, columnspan=2, sticky="w")
    CMorTPcombobox = ttk.Combobox(graphWindow, values=["CM/Théorie", "TP"])
    CMorTPcombobox.grid(row=3, column=2, sticky="w")
    CMorTPcombobox.bind("<<ComboboxSelected>>",lambda event: choosedTPorCM(graphWindow, CMorTPcombobox.get()))

    Button(graphWindow, text="Total amount of study", command=lambda:total_study_time(graphWindow)).grid(row=3, column=4, columnspan=2, sticky="w")


def newCourseWindow(master):
    newCourseWindow = Toplevel(master)
    newCourseWindow.title("New course window")
    Label(newCourseWindow, text="Here you can enter a new course. \nFirst enter the course name, then select the calendar of the course").grid(column=0, row=0, columnspan=4)

    Label(newCourseWindow, text="Insert the course name:").grid(column=0, row=3)

    inputText = Entry(newCourseWindow, width=30)
    inputText.grid(column=1, row=3)

    Button(newCourseWindow, text="Enter", command=lambda:getText(inputText)).grid(column=2, row=3)




def main():
    home_window = Tk()
    home_window.title("Study Statistics")
    
    #The actual dimensions of the window are: 
    #columns = 5
    #lines = 5
    

    Label(home_window, text='Welcome to this app. Here you can set your work sessions.').grid(row=0, column=0, columnspan = 5)

    Label(home_window, text=f'We actually are in {which_week()}').grid(row=1, column=0, columnspan = 5)

    Label(home_window, text='Do you want to start a session?').grid(row=2, column=0, columnspan=2, sticky="w")

    combo_box_start = ttk.Combobox(home_window, values=getattr(course_calendar, "Course_list_" + actual_period))
    combo_box_start.grid(row=3, column=0, sticky="w")
    combo_box_start.bind("<<ComboboxSelected>>", lambda event: start_session(combo_box_start, home_window))

    endText = Label(home_window, text='Do you want to end a session?')
    endText.grid(row=2, column=2, columnspan=2, sticky="w")
    combo_box_end = ttk.Combobox(home_window, values=getattr(course_calendar, "Course_list_" + actual_period))
    combo_box_end.grid(row=3, column=2, sticky="w")
    combo_box_end.bind("<<ComboboxSelected>>", lambda event: endSessionChecked(combo_box_end, home_window))

    sessionRunning = ttk.Button(home_window, text="Session running", command= lambda: time_from_beginning(home_window))
    sessionRunning.grid(row=3, column=4, sticky="w")



    graphButton = Button(home_window, text='Show graphs', command= lambda: graph_window(home_window))
    graphButton.grid(row=4, column=0)

    workButton = Button(home_window, text='Work done', command=lambda: goodJobWindow(home_window))
    workButton.grid(row=4, column=1)

    closeButton = Button(home_window, text='Close', command=home_window.destroy)
    closeButton.grid(row=4, column=2)

    reset_button = Button(home_window, text="Reset all", command=confirm)
    reset_button.grid(row=4, column=3)

    Button(home_window, text="New course", command=lambda: newCourseWindow(home_window)).grid(row=5, column=0)

    Button(home_window, text="TODO", command=lambda: TODOWindow(home_window)).grid(row=5, column=1)

    home_window.mainloop()



main()












































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

# Global variable to store the canvas
canvas = None
toolbar = None



def which_week():
    weeks = {"S1": ["03/02", "04/02", "05/02", "06/02", "07/02", "08/02", "09/02"],
             "S2": ["10/02", "11/02", "12/02", "13/02", "14/02", "15/02", "16/02"],
             "S3": ["17/02", "18/02", "19/02", "20/02", "21/02", "22/02", "23/02"],
             "S4": ["24/02", "25/02", "26/02", "27/02", "28/02", "01/03", "02/03"],
             "S5": ["03/03", "04/03", "05/03", "06/03", "07/03", "08/03", "09/03"],
             "S6": ["10/03", "11/03", "12/03", "13/03", "14/03", "15/03", "16/03"],
             "S7": ["17/03", "18/03", "19/03", "20/03", "21/03", "22/03", "23/03"],
             "S8": ["24/03", "25/03", "26/03", "27/03", "28/03", "29/03", "30/03"],
             "S9": ["31/03", "01/04", "02/04", "03/04", "04/04", "05/04", "06/04"],
             "S10": ["07/04", "08/04", "09/04", "10/04", "11/04", "12/04", "13/04"],
             "S11": ["14/04", "15/04", "16/04", "17/04", "18/04", "19/04", "20/04"],
             "S12": ["05/05", "06/05", "07/05", "08/05", "09/05", "10/05", "11/05"],
             "S13": ["12/05", "13/05", "14/05", "15/05", "16/05", "17/05", "18/05"],}

    today = datetime.today().strftime('%d/%m')
    for week_number in weeks.keys():
        if today in weeks[week_number]:
            print("We are in the week number: ", week_number)
            int_week_number = int(week_number.split("S")[1])
            return int_week_number


def graph_work_quantity(course, actual_week_number, TPorCM, window):
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
    courseNEW = "".join(course.split(" "))
    file = "/Users/thibaultvanni/PycharmProjects/Study/hours_done/Done" + courseNEW + ".csv"
    df = pd.read_csv(file)
    passed_week = []
    numberofTPTheorical = 0
    numberofCMTheorical = 0
    numberofTPDone = 0
    numberofCMDone = 0
    print(TPorCM)

    for week_number in getattr(course_calendar, courseNEW).keys():
        week_number_temporary = int(week_number.split("S")[1])
        if TPorCM == "TP" and week_number_temporary <= actual_week_number:
            DoneTP.append(sum(df["TP"][:week_number_temporary]))
            if TPorCM in getattr(course_calendar, courseNEW)[week_number]:
                numberofTPTheorical += getattr(course_calendar, courseNEW)[week_number].count("TP")
                theoricalTP.append(numberofTPTheorical)
                passed_week.append(week_number)
            else:
                theoricalTP.append(0)
                passed_week.append(week_number)
        if TPorCM == "CM/Théorie" and week_number_temporary <= actual_week_number :
            DoneCM.append(sum(df["CM"][:week_number_temporary]))
            if "CM" in getattr(course_calendar, courseNEW)[week_number]:
                numberofCMTheorical += getattr(course_calendar, courseNEW)[week_number].count("CM")
                theoricalCM.append(numberofCMTheorical)
                passed_week.append(week_number)
            else:
                theoricalCM.append(0)
                passed_week.append(week_number)
        elif week_number_temporary > actual_week_number:
            break

    x = arange(len(passed_week))  # the label locations
    width = 0.35  # the width of the bars
    if TPorCM == "CM/Théorie":
        fig, ax = plt.subplots()
        fig.subplots_adjust(hspace=0.6)
        ax.bar(x - width / 2, DoneCM, width, label='CM or Theory done')
        ax.bar(x + width / 2, theoricalCM, width, label='CM to do')

        ax.set_ylabel('#')
        ax.set_title('Progress of CM in ' + course)
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

    elif TPorCM == "TP":
        fig, ax = plt.subplots()
        ax.bar(x - width / 2, DoneTP, width, label='TP done')
        ax.bar(x + width / 2, theoricalTP, width, label='TP to do')

        ax.set_ylabel('#')
        ax.set_title('Progress of TP in ' + course)
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
    now = datetime.now()
    with open("/Users/thibaultvanni/PycharmProjects/Study/session_running", "r") as file:
        lines = []
        for line in file:
            lines.append(line)
    if "session_running = False\n" not in lines:
        start_time = datetime.strptime(lines[0].strip(), '%d/%m/%y %H:%M:%S')
        course = lines[1].strip()
        difference = now - start_time
        diffTime = Label(window, text="You've started a " + course + " session " + str(difference) + " ago", fg="red")
        diffTime.grid(row=5, column=0, columnspan=4)
        diffTime.after(2000, diffTime.destroy)
    else:
        diffTime = Label(window, text="You didn't start any course", fg="red")
        diffTime.grid(row=5, column=0, columnspan=4)
        diffTime.after(2000, diffTime.destroy)


def time_to_hms(seconds):
    """ Convert seconds to HH:MM:SS format """
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


    file = "/Users/thibaultvanni/PycharmProjects/Study/hours_done/" + "".join(course.split(" ")) + ".csv"
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
    subprocess.run(['python3', '/Users/thibaultvanni/PycharmProjects/Study/create_total_file.py'])

    # Load the dataset
    file = "/Users/thibaultvanni/PycharmProjects/Study/hours_done/TOTALSTUDY.csv"
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


    with open("/Users/thibaultvanni/PycharmProjects/Study/session_running", "r+") as file:
        content = file.read()  # Read the entire file
        print(content)  # Debugging step to check file contents

        if "session_running = True" in content and "session_running = False" not in content:  # Check if the string exists
            print("Session is running!")
            messagebox.showerror("Attention", "You have already started a session running.")

        else:
            print(True)
            file.seek(0)  # Move to the beginning
            file.truncate()  # Remove all content
            file.write(now + "\n")
            file.write(combo_box_start.get() + "\n")
            file.write("session_running = True\n")
            print("You just started a " + combo_box_start.get() + " session at " + now)

            startText = Label(window, text= "You just started a " + combo_box_start.get() + " session at " + now, fg="green")
            startText.grid(row=5, column=0, columnspan=5)
            startText.after(3000, startText.destroy)

    return combo_box_start.get(), now, True


def end_session(combo_box_end):
    now = datetime.now()
    with open("/Users/thibaultvanni/PycharmProjects/Study/session_running", "r+") as file:
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
    file_to_add = '/Users/thibaultvanni/PycharmProjects/Study/hours_done/' + "".join(combo_box_end.split(" ")) + ".csv"
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
    with open("/Users/thibaultvanni/PycharmProjects/Study/session_running", "r+") as file:
        lines = []
        for line in file:
            lines.append(line)
    print("lines: ", lines)
    print("Value end session = ", value)
    print(len(lines))
    if moment == "End":
        if len(lines) < 3 or "session_running = False\n" in lines:
            print(True)
            messagebox.showwarning("ATTENTION", "You didn't start any session.")
            return False
        if lines[1].strip() != value:
            print('You cannot close a session in a different course than: '+ lines[1])
            messagebox.showwarning("ATTENTION", 'You cannot close a session in a different course than: '+ lines[1])
            return False
    if moment == "Start":
        pass
    return True

def endSessionChecked(combo_box_end, window):
    selected_value = combo_box_end.get()
    print("Selected:", selected_value)

    if check("End", selected_value, window):  # Call check() and verify result
        end_session(selected_value)  # Call end_session() if valid


def reset_selections(type_var, course_var, label_result):
    """Reset the selections and update the label"""
    type_var.set(None)  # Reset the type variable
    course_var.set("None")  # Reset the course variable

    # Reset the label result to its initial message
    label_result.config(text="Please select both a Type and a Course.")


def check_selection(type_var, course_var, label_result):
    currentweek = which_week()
    selected_type = type_var.get()
    selected_course = course_var.get()

    # Check if both selections are made
    if selected_course == "None" or selected_type == 0:  # Default checks
        label_result.config(text="Please select both a Type and a Course.", fg="red")
        return


    label_result.config(text=f"Selected: {selected_course} - {selected_type}", fg="green")
    label_result.after(1000, lambda: reset_selections(type_var, course_var, label_result))

    doneCourse = "Done" + selected_course
    print(f"Updating: {doneCourse}, type: {selected_type}, week: S{currentweek}")

    file = "/Users/thibaultvanni/PycharmProjects/Study/hours_done/" + "".join(doneCourse.split(" ")) + ".csv"
    df = pd.read_csv(file, index_col=0)
    df.at["S"+str(currentweek), selected_type] += 1
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

    Radiobutton(goodJobWindow, text="Thermodynamique", variable=course_var, value="Thermodynamique").grid(row=3, column=3, sticky="w", padx=5, pady=2)
    Radiobutton(goodJobWindow, text="Mécanique des Milieux Continus", variable=course_var, value="Mécanique des Milieux Continus").grid(row=4, column=3, sticky="w", padx=5, pady=2)
    Radiobutton(goodJobWindow, text="Fabrication Mécanique", variable=course_var, value="Fabrication Mécanique").grid(row=5, column=3, sticky="w", padx=5, pady=2)
    Radiobutton(goodJobWindow, text="Télécommunications", variable=course_var, value="Télécommunications").grid(row=6, column=3,  sticky="w", padx=5, pady=2)
    Radiobutton(goodJobWindow, text="TEST", variable=course_var, value="TEST").grid(row=7, column=3, sticky="w", padx=5, pady=2)

    confirmButton = Button(goodJobWindow, text="Confirm", command=lambda: check_selection(type_var, course_var, label_result))
    confirmButton.grid(row=8, column=0, columnspan=4, padx=5, pady=2)

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
        shutil.rmtree("/Users/thibaultvanni/PycharmProjects/Study/hours_done")
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
    workDonecombobox = ttk.Combobox(window, values=["Mécanique des Milieux Continus", "Thermodynamique", "Fabrication Mécanique", "Télécommunications", "TEST"])
    workDonecombobox.grid(row=4, column=2, sticky="w")
    workDonecombobox.bind("<<ComboboxSelected>>", lambda event: update_graph2(event, window, TPorCM, workDonecombobox))


def getText(inputText):
    course_name = inputText.get()
    print(f'{course_name=!r}')
    course_name_file = course_name + ".csv"
    if course_name_file in os.listdir("/Users/thibaultvanni/PycharmProjects/Study/hours_done"):
        messagebox.showwarning("ATTENTION", "Course " + str(course_name) + " already exists.\n Please choose a different course.")
    else:
        mydataset = {'Start': [],
                     'End': [],
                     'Delta': []}
        myvar = pd.DataFrame(mydataset)
        path = "/Users/thibaultvanni/PycharmProjects/Study/hours_done/" + str(course_name) + ".csv"
        myvar.to_csv(path, mode='w', index=True, header=True)



def graph_window(master):
    global canvas
    graphWindow = Toplevel(master)
    graphWindow.title("Graph Window")
    Label(graphWindow, text="Welcome to the graph window").grid(row=1, column=0, columnspan=4)

    back_button = Button(graphWindow, text="Go back", command=graphWindow.destroy)
    back_button.grid(row=0, column=0, columnspan=4, sticky="w")

    Label(graphWindow, text="Do you want to see the work hours? ").grid(row=2, column=0, columnspan=2, sticky="w")
    course_combobox = ttk.Combobox(graphWindow, values=["Mécanique des Milieux Continus", "Thermodynamique", "Fabrication Mécanique", "Télécommunications", "TEST"])
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
    """
    The actual dimensions of the window are: 
    columns = 5
    lines = 4
    """

    hometext = Label(home_window, text='Welcome to this app. Here you can set your work sessions.')
    hometext.grid(row=0, column=0, columnspan = 5)

    weektext = Label(home_window, text=f'We actually are in S{which_week()}').grid(row=1, column=0, columnspan = 5)

    startText = Label(home_window, text='Do you want to start a session?')
    startText.grid(row=2, column=0, columnspan=2, sticky="w")
    combo_box_start = ttk.Combobox(home_window, values=["Mécanique des Milieux Continus", "Thermodynamique", "Fabrication Mécanique", "Télécommunications", "TEST"])
    combo_box_start.grid(row=3, column=0, sticky="w")
    combo_box_start.bind("<<ComboboxSelected>>", lambda event: start_session(combo_box_start, home_window))

    endText = Label(home_window, text='Do you want to end a session?')
    endText.grid(row=2, column=2, columnspan=2, sticky="w")
    combo_box_end = ttk.Combobox(home_window, values=["Mécanique des Milieux Continus", "Thermodynamique", "Fabrication Mécanique", "Télécommunications", "TEST"])
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

    home_window.mainloop()



main()












































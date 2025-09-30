# Study

This is a personal project designed to track and manage information about my university classes.  
It provides an interface to monitor study sessions, visualize progress, and keep track of completed work.

---

## Features

### 📌 Homepage
The homepage displays:
- The current **week number**.
- A small **welcome message**.
- A set of **main buttons** for navigation and actions.

### 🎛 Main Buttons
- **Start a session**  
  Select a course and begin a study session. This will reset the session file and record:
  - Start time  
  - Course name  
  - Other useful metadata  

- **End a session**  
  Stops the current session. The program checks if the course matches the one that was started and then logs the study time in the file specific to that course.

- **Session running**  
  Displays the course currently being studied and the elapsed time since the session started.

- **Show graphs**  
  Opens a menu that provides access to graphs and statistics (see below).

- **Work done**  
  Opens a menu to log and review completed work (see below).

- **Close**  
  Exits the application and terminates tasks.  
  ⚠️ Note: This does **not** end a running session.

- **Reset all**  
  Resets all saved files and data.

- **New course** and **TODO**  
  Features under development.

---

## 📊 Graphs
In the **Graphs** window, you can view statistics such as:
- Hours per course  
- Breakdown of **TP** (practical work) vs **CM** (lectures)  
- Total study time across all courses  

---

## ✅ Work Done
The **Work Done** window allows you to:
- Select a course and specify **TP** or **CM**  
- Track how many TP and CM sessions you have completed  

---

## 🚀 Usage

1. **Start a session**
   - On the homepage, click **Start a session**.
   - Choose the course you want to work on.  
   - The program will log the start time and prepare the tracking file.

2. **Work on the course**
   - While the session is running, you can check the **Session running** button to see:
     - The current course  
     - The elapsed time since the start  

3. **End the session**
   - When you finish studying, click **End a session**.  
   - The program will validate that the course matches and add your study time to the corresponding course log.

4. **View progress**
   - Use **Show graphs** to see statistics about your study time.  
   - Use **Work done** to log completed TP/CM and check how many you’ve done so far.

5. **Reset or close**
   - **Close** ends the program (but not an ongoing session).  
   - **Reset all** clears all files and resets your progress.  

---

## 🚧 Status
Some features are still under development and may change in the future.
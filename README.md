# PrioritizeProcess

A Python-based application that automatically adjusts CPU core affinity to optimize process performance.

## Features
* **OS Support:** Windows 10 and Windows 11 only.
* **Automated Configuration:** Easy first-time setup that guides you through the process.
* **Smart CPU Adjustment:** Automatically manages and prioritizes CPU cores for your target applications.

---

## How to Use

### Method 1: Using the Pre-compiled Executable (`.exe`)
1. Download the latest `PrioritizeProcess.zip` from the **Releases** section.
2. Unzip the downloaded file.
3. Locate and run `app.exe`.

### Method 2: Running via Python
*Note: This project was built using **Python 3.12**. It is highly recommended to use this version.*

1. **Download the Repository**
   * **Via Git:**
     ```bash
     git clone [https://github.com/matthew-teh/PrioritizeProcess.git](https://github.com/matthew-teh/PrioritizeProcess.git)
     ```
   * **Via ZIP:** Download the latest source code from the **Releases** section and extract it.

2. **Create a Virtual Environment (Optional but Recommended)**
   * Open **Command Prompt (CMD)**.
   * Navigate to the project directory.
   * Run the following command:
     ```cmd
     python -m venv .venv
     ```

3. **Run the Application**
   * Execute the main script using your virtual environment:
     ```cmd
     .venv\Scripts\python.exe main.py
     ```

4. Follow the on-screen prompts to complete the setup.

---

## How It Works

### First-Time Launch
* The application automatically generates a configuration file named `config.yaml`.
* It will ask you a few questions to complete the initial setup.

### Subsequent Launches
The app detects the current state of your system and toggles the optimization:
* **If the target process is already prioritized:** It resets all programs back to their normal CPU allocations.
* **If the target process is NOT prioritized:** It instantly applies the optimized CPU core priority to the target process.
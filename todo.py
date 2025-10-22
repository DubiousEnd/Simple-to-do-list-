
FILENAME = "tasks.txt"

def _strip_mark(s: str) -> str:
    s = str(s).strip()
    if s.startswith("[x] "): return s[4:]
    if s.startswith("[ ] "): return s[4:]
    return s

def load_tasks():
    tasks=[]
    try:
        with open(FILENAME,"r") as f:
            for raw in f:
                line = raw.strip()
                if not line:
                    continue

                if "|" in line:
                    left, text = line.split("|", 1)
                    mark = "[x]" if left.strip() == "1" else "[ ]"
                    tasks.append(f"{mark} {text}")
                    continue
                
                if line.startswith("[x] ") or line.startswith("[ ] "):
                    tasks.append(line)
                    continue

                # Fallback: treat as not-done task text
                tasks.append(f"[ ] {line}")
    except FileNotFoundError:
        pass
    return tasks

def save_tasks(tasks):
    with open(FILENAME, "w", encoding="utf-8") as f:
        for t in tasks:
            if isinstance(t, dict):
                # safer default = not done
                mark = "[x]" if t.get("done", False) else "[ ]"
                text = t.get("text", "")
                line = f"{mark} {text}"
            else:
                line = str(t)
            f.write(line.rstrip("\n") + "\n")

def show_tasks(tasks):
    if not tasks:
        print("⁉️ No tasks yet.")
        return
    print("\nYour To-Do List:")
    for i, t in enumerate(tasks, start =1):
       print(f"{i}. {t}")
    print()

def main():
    tasks = load_tasks()

    while True:
        print("Menu:")
        print("1. View Tasks")
        print("2. Add Task")
        print("3. Mark Task as Done")
        print("4. Remove Task")
        print("5. Exit")
        choice = input("Enter your choice (1-5): ")

        if choice == "1":
            show_tasks(tasks)
        
        elif choice == "2":
            text = input("Enter new Task: ")
            tasks.append(f"[ ] {_strip_mark(text)}")   # <- store as string
            save_tasks(tasks)
            print("✅ Task added successfully! \n")

        elif choice == "3":
            show_tasks(tasks)
            if not tasks:
                continue
            try:
                num = int(input("Enter task number to mark as done: "))
                if 1 <= num <= len(tasks):
                    raw = tasks[num - 1]
                    text_only = _strip_mark(raw)
                    tasks[num - 1] = f"[x] {text_only}"  # <- force done
                    save_tasks(tasks)
                    print("✔ Task marked as done!\n")
                else:
                    print("❌ Invalid task number.\n")
            except ValueError:
                print("❌ Please enter a valid number.\n")
                
        elif choice == "4":
            show_tasks(tasks)
            if not tasks:
                continue
            try:
                num = int(input("Enter task number to remove: "))
                if 1 <= num <= len(tasks):
                    removed = tasks.pop(num - 1)           
                    save_tasks(tasks)
                    print(f"🗑 Removed: {removed}\n")       
                else:
                    print("❌ Invalid task number.\n")
            except ValueError:
                print("❌ Please enter a valid number.\n")

        elif choice == "5":
            print("👋🏾 Goodbye!")
            break
        else:
            print("❌ Please enter a valid choice from 1-5 \n")

if __name__ == "__main__":
    main()

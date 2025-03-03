---

# 📌 INFO-5940

Welcome to the **INFO-5940** repository! This guide will help you set up the development environment using **Docker** in **VS Code**, configure the **OpenAI API key**, manage Git branches, and run Jupyter notebooks for assignments.  

---

## 🛠️ Prerequisites  

Before starting, ensure you have the following installed on your system:  

- [Docker](https://www.docker.com/get-started) (Ensure Docker Desktop is running)  
- [VS Code](https://code.visualstudio.com/)  
- [VS Code Remote - Containers Extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)  
- [Git](https://git-scm.com/)  
- OpenAI API Key  

---

## 🚀 Setup Guide  

### 1️⃣ Clone the Repository  

Open a terminal and run:  

```bash
git clone https://github.com/AyhamB/INFO-5940.git
cd INFO-5940
```

---

### 2️⃣ Open in VS Code with Docker  

1. Open **VS Code**, navigate to the `INFO-5940` folder.  
2. Open the Command Palette (`Ctrl+Shift+P` or `Cmd+Shift+P` on Mac) and search for:  
   ```
   Remote-Containers: Reopen in Container
   ```
3. Select this option. VS Code will build and open the project inside the container.  

📌 **Note:** If you don’t see this option, ensure that the **Remote - Containers** extension is installed.  

---

### 3️⃣ Configure OpenAI API Key  

Since `docker-compose.yml` expects environment variables, follow these steps:  

#### ➤ Option 1: Set the API Key in `.env` (Recommended)  

1. Inside the project folder, create a `.env` file:  

   ```bash
   touch .env
   ```

2. Add your API key and base URL:  

   ```plaintext
   OPENAI_API_KEY=your-api-key-here
   OPENAI_BASE_URL=https://api.ai.it.cornell.edu/
   TZ=America/New_York
   ```

3. Modify `docker-compose.yml` to include this `.env` file:  

   ```yaml
   version: '3.8'
   services:
     devcontainer:
       container_name: info-5940-devcontainer
       build:
         dockerfile: Dockerfile
         target: devcontainer
       environment:
         - OPENAI_API_KEY=${OPENAI_API_KEY}
         - OPENAI_BASE_URL=${OPENAI_BASE_URL}
         - TZ=${TZ}
       volumes:
         - '$HOME/.aws:/root/.aws'
         - '.:/workspace'
       env_file:
         - .env
   ```

4. Restart the container:  

   ```bash
   docker-compose up --build
   ```

Now, your API key will be automatically loaded inside the container.  

---

## 🔀 Managing Git Branches in VS Code  

Since you may need to switch between different branches for assignments, here’s how to manage Git branches in **VS Code** efficiently.  

### **Option 1: Using the Git Panel (Easiest)**
1. Open **VS Code**.
2. Click on the **Source Control** panel on the left (`Ctrl+Shift+G` / `Cmd+Shift+G` on Mac).
3. Click on the **branch name** (bottom-left corner of VS Code).
4. A dropdown will appear with all available branches.
5. Select the branch you want to switch to.  

### **Option 2: Using Command Palette**
1. Open **VS Code**.
2. Press `Ctrl+Shift+P` (`Cmd+Shift+P` on Mac) to open the **Command Palette**.
3. Type **"Git: Checkout to..."** and select it.
4. Pick the branch you want to switch to.

### **Option 3: Using the Terminal**
If you prefer the command line inside the container, use:

```bash
git branch   # View all branches
git checkout branch-name   # Switch to a branch
git pull origin branch-name   # Update the branch (recommended)
```

📌 **Tip:** If you are working on a new feature, create a new branch before making changes:

```bash
git checkout -b new-feature-branch
```

---

## 🏃 Running Jupyter Notebook From Outside VS Code

Once inside the **VS Code Dev Container**, you should be able to run the notebooks from the IDE but you can also launch the Jupyter Notebook server:  

```bash
jupyter notebook --ip 0.0.0.0 --port=8888 --no-browser --allow-root
```

---

### 5️⃣ Access Jupyter Notebook  

When the notebook starts, it will output a URL like this:  

```
http://127.0.0.1:8888/?token=your_token_here
```

Copy and paste this link into your browser to access the Jupyter Notebook interface.  

---

## 🛠️ Troubleshooting  

### **Container Fails to Start?**  
- Ensure **Docker Desktop is running**.  
- Run `docker-compose up --build` again.  
- If errors persist, delete existing containers with:  

  ```bash
  docker-compose down
  ```

  Then restart:  

  ```bash
  docker-compose up --build
  ```

### **Cannot Access Jupyter Notebook from outside VS Code?**  
- Ensure you’re using the correct port (`8888`).  
- Run `docker ps` to check if the container is running.  

### **OpenAI API Key Not Recognized?**  
- Check if `.env` is correctly created.  
- Ensure `docker-compose.yml` includes `env_file: - .env`.  
- Restart the container after making changes (`docker-compose up --build`).  

---

## 🎯 Next Steps  

- Complete assignments using the Jupyter Notebook.  
- Use the **OpenAI API** inside Python scripts within the container.  
- Switch between **Git branches** as needed for different assignments.  

Happy coding! 🚀

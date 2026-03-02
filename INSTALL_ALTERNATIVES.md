# 🚀 Installation Alternatives (No Docker Desktop)

If you cannot install Docker Desktop due to company policies, here are several alternatives:

## Option 1: Podman Desktop (Recommended - Most Compatible)

**Podman** is a daemonless, open-source container engine that's Docker-compatible and **doesn't require admin privileges**.

### Installation Steps

1. **Download Podman Desktop:**
   - Visit: https://podman-desktop.io/downloads
   - Download Windows installer (no admin required)
   - Or use Chocolatey: `choco install podman-desktop`

2. **Install Podman:**
   ```powershell
   # Run the installer (user-level install, no admin needed)
   # Follow the wizard
   ```

3. **Start Podman:**
   ```powershell
   podman machine init
   podman machine start
   ```

4. **Enable Docker Compatibility:**
   ```powershell
   # Podman has built-in Docker compatibility
   # Create alias for docker commands
   Set-Alias -Name docker -Value podman
   Set-Alias -Name docker-compose -Value podman-compose
   
   # Or install podman-compose
   pip install podman-compose
   ```

5. **Run the Demo:**
   ```powershell
   # Use podman instead of docker
   podman-compose up -d
   
   # Or with alias
   docker compose up -d  # (will use podman)
   ```

### Update Scripts for Podman

The demo will automatically detect Podman:
```powershell
.\start-podman.ps1 up
```

---

## Option 2: WSL2 + Docker Engine (No Desktop)

Install Docker Engine directly in WSL2 without Docker Desktop.

### Installation Steps

1. **Enable WSL2:**
   ```powershell
   # In PowerShell (may need admin for first-time setup)
   wsl --install
   # Restart if prompted
   ```

2. **Install Ubuntu in WSL2:**
   ```powershell
   wsl --install -d Ubuntu
   ```

3. **Install Docker Engine in WSL2:**
   ```bash
   # Inside WSL2 Ubuntu terminal
   
   # Update packages
   sudo apt-get update
   
   # Install prerequisites
   sudo apt-get install -y \
       ca-certificates \
       curl \
       gnupg \
       lsb-release
   
   # Add Docker's official GPG key
   sudo mkdir -m 0755 -p /etc/apt/keyrings
   curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
   
   # Set up repository
   echo \
     "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
     $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
   
   # Install Docker Engine
   sudo apt-get update
   sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
   
   # Start Docker service
   sudo service docker start
   
   # Add your user to docker group (optional)
   sudo usermod -aG docker $USER
   
   # Test installation
   docker --version
   docker compose version
   ```

4. **Run Demo from WSL2:**
   ```bash
   # Navigate to project (Windows drives are at /mnt/)
   cd /mnt/c/Users/julio.sanchez/agentic-vscode-demo
   
   # Start the demo
   docker compose up -d
   ```

5. **Auto-start Docker (optional):**
   ```bash
   # Add to ~/.bashrc
   echo 'sudo service docker start' >> ~/.bashrc
   ```

---

## Option 3: Development Mode (No Containers) ⭐ Easiest

Run the demo **without any containers** using pure Python. Perfect for testing the agent logic without Docker.

### Setup

1. **Install Python Dependencies:**
   ```powershell
   cd C:\Users\julio.sanchez\agentic-vscode-demo
   pip install -r requirements.txt
   ```

2. **Run the Demo:**
   ```powershell
   # Start everything in development mode
   .\start-demo.ps1 all
   ```

   This will:
   - ✅ Start MCP server (Python process)
   - ✅ Run agent orchestrator (Python)
   - ✅ Execute demos (Python scripts)
   - ⚠️ Skip containerization (no isolation)
   - ⚠️ Skip observability stack (optional)

3. **Run Specific Demos:**
   ```powershell
   # Terminal 1: Start MCP server
   .\start-demo.ps1 server
   
   # Terminal 2: Run laptop demo
   .\start-demo.ps1 laptop
   
   # Or run manually
   python examples/laptop_refresh.py
   python examples/k8s_diagnostics.py
   ```

### What You Get

✅ **Available:**
- Full agent orchestration logic
- MCP tool integration
- Task decomposition
- Multi-step workflows
- All demo scenarios

❌ **Not Available:**
- Container isolation
- Resource limits
- Scalability features
- Production deployment patterns
- Full observability stack

**Great for:** Learning, development, testing agent logic, demos without Docker

---

## Option 4: Rancher Desktop

Open-source alternative to Docker Desktop with Kubernetes support.

### Installation

1. **Download Rancher Desktop:**
   - Visit: https://rancherdesktop.io/
   - Download Windows installer

2. **Install and Configure:**
   - Choose "dockerd (moby)" as container runtime
   - Enable Kubernetes (optional)

3. **Run Demo:**
   ```powershell
   docker compose up -d
   ```

---

## Comparison Matrix

| Option | Admin Required | Docker Compatible | Best For |
|--------|----------------|-------------------|----------|
| **Podman Desktop** | ❌ No | ✅ Yes | Most compatible, no admin |
| **WSL2 + Docker** | ⚠️ First time only | ✅ Yes | Full Docker, Linux-based |
| **Development Mode** | ❌ No | ❌ N/A | Quick testing, no Docker |
| **Rancher Desktop** | ✅ Yes | ✅ Yes | Kubernetes included |

---

## Quick Decision Guide

**Choose Podman if:**
- ✅ You have no admin access
- ✅ Want container features
- ✅ Need Docker compatibility

**Choose WSL2 + Docker if:**
- ✅ You can enable WSL2 (one-time admin)
- ✅ Want native Docker experience
- ✅ Comfortable with Linux

**Choose Development Mode if:**
- ✅ You just want to test the demo quickly
- ✅ Don't need containers right now
- ✅ Focus on agent logic, not deployment

---

## Next Steps

Pick your option above, then:

1. **Install your chosen solution**
2. **Verify installation:**
   ```powershell
   docker --version  # or podman --version
   ```

3. **Run the demo:**
   ```powershell
   # With containers (Podman/Docker)
   docker compose up -d
   # Or
   .\start-podman.ps1 up
   
   # Without containers (Development)
   .\start-demo.ps1 all
   ```

---

## Troubleshooting

### Podman: Machine won't start
```powershell
podman machine stop
podman machine rm
podman machine init
podman machine start
```

### WSL2: Docker service won't start
```bash
sudo service docker status
sudo service docker start

# If fails, check logs
sudo journalctl -u docker
```

### Development Mode: Module not found
```powershell
pip install -r requirements.txt --upgrade
python --version  # Should be 3.12+
```

---

**Ready to start?** Pick an option above and let's get you running! 🚀
